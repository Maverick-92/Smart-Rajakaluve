"""
Smart Rajakaluve backend
- Receives readings from ESP32 sensor nodes (HTTP POST, directly or via a LoRa gateway)
- Stores every reading in SQLite
- Runs the same neighbour-comparison detection rules as the dashboard
- Serves the dashboard (dist/index.html) so it opens in LIVE mode
- Accepts Sentinel-2 sky-view results from sentinel/ndti_bellandur.py

Run:  pip install -r requirements.txt
      SRK_API_KEY=change-me uvicorn app:app --host 0.0.0.0 --port 8000
"""
import json
import os
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

BASE = Path(__file__).resolve().parent
DB_PATH = os.environ.get("SRK_DB", str(BASE / "srk.db"))
API_KEY = os.environ.get("SRK_API_KEY", "change-me")
DASHBOARD = BASE.parent / "dist" / "index.html"
CONFIG = json.loads((BASE / "config.json").read_text())

# hardware id -> dashboard node id, and drain geometry used by detection
HW_MAP = CONFIG["hardware_map"]
DRAINS = CONFIG["drains"]
RULES = CONFIG["rules"]

app = FastAPI(title="Smart Rajakaluve API", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


with db() as con:
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS readings(
          id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, hw_id TEXT, node_id TEXT,
          level_cm REAL, turbidity_ntu REAL, tds_ppm REAL, ph REAL, temp_c REAL,
          battery REAL, rssi REAL, raw TEXT);
        CREATE INDEX IF NOT EXISTS ix_readings_node_ts ON readings(node_id, ts);
        CREATE TABLE IF NOT EXISTS actions(
          id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, alert_key TEXT, alert_id TEXT, step TEXT, dept TEXT);
        CREATE TABLE IF NOT EXISTS alerts(
          key TEXT PRIMARY KEY, type TEXT, drain TEXT, a INTEGER, b INTEGER, dept TEXT,
          status TEXT, created TEXT, last_seen TEXT, detail TEXT);
        CREATE TABLE IF NOT EXISTS sky(id INTEGER PRIMARY KEY CHECK (id = 1), payload TEXT);
        """
    )


class Reading(BaseModel):
    hw_id: str = Field(..., description="ID burned into the node firmware, e.g. NODE-A")
    level_cm: Optional[float] = None
    distance_cm: Optional[float] = Field(None, description="raw ultrasonic distance; level = mount_height - distance")
    turbidity_ntu: Optional[float] = None
    tds_ppm: Optional[float] = None
    ph: Optional[float] = None
    temp_c: Optional[float] = None
    battery: Optional[float] = None
    rssi: Optional[float] = None
    ts: Optional[str] = None


class Action(BaseModel):
    alert_key: str
    alert_id: Optional[str] = None
    step: str
    dept: str
    ts: Optional[str] = None


def now_iso():
    return datetime.now(timezone.utc).isoformat()


@app.post("/api/readings")
def post_reading(r: Reading, x_api_key: str = Header(default="")):
    if x_api_key != API_KEY:
        raise HTTPException(401, "bad api key")
    m = HW_MAP.get(r.hw_id)
    if not m:
        raise HTTPException(404, f"unknown hw_id {r.hw_id}; add it to config.json hardware_map")
    level = r.level_cm
    if level is None and r.distance_cm is not None:
        level = max(0.0, m["mount_height_cm"] - r.distance_cm)
    if level is not None:
        level = level * m.get("level_scale", 1)
    # basic range checks: reject impossible values instead of storing them
    if level is not None and not (0 <= level <= 400):
        raise HTTPException(422, "level out of range")
    if r.turbidity_ntu is not None and not (0 <= r.turbidity_ntu <= 4000):
        raise HTTPException(422, "turbidity out of range")
    if r.ph is not None and not (0 <= r.ph <= 14):
        raise HTTPException(422, "pH out of range")
    ts = r.ts or now_iso()
    with db() as con:
        con.execute(
            "INSERT INTO readings(ts,hw_id,node_id,level_cm,turbidity_ntu,tds_ppm,ph,temp_c,battery,rssi,raw) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (ts, r.hw_id, m["node_id"], level, r.turbidity_ntu, r.tds_ppm, r.ph, r.temp_c, r.battery, r.rssi, r.model_dump_json()),
        )
    run_detection()
    return {"ok": True, "node_id": m["node_id"], "level_cm": level}


def latest():
    out = {}
    with db() as con:
        rows = con.execute(
            "SELECT r.* FROM readings r JOIN (SELECT node_id, MAX(id) mid FROM readings GROUP BY node_id) x ON r.id = x.mid"
        ).fetchall()
    for row in rows:
        out[row["node_id"]] = dict(row)
    return out


def history(node_id, n):
    with db() as con:
        rows = con.execute("SELECT * FROM readings WHERE node_id=? ORDER BY id DESC LIMIT ?", (node_id, n)).fetchall()
    return [dict(r) for r in rows][::-1]


def run_detection():
    """Same rules as the dashboard: compare neighbouring live nodes."""
    now = latest()
    found = []
    for d in DRAINS:
        ids = d["nodes"]
        for i, nid in enumerate(ids):
            a = now.get(nid)
            if not a:
                continue
            h = history(nid, RULES["stuckTicks"])
            if len(h) >= RULES["stuckTicks"] and all(x["level_cm"] == h[0]["level_cm"] and x["turbidity_ntu"] == h[0]["turbidity_ntu"] for x in h):
                found.append(("SENSOR", d["id"], i, i, ["OPS"], {}))
            if a["level_cm"] is not None and a["level_cm"] > RULES["overflowFrac"] * d["cap"]:
                found.append(("OVERFLOW", d["id"], i, i, ["GBA"], {"level": a["level_cm"]}))
            if i == len(ids) - 1:
                continue
            b = now.get(ids[i + 1])
            if not b:
                continue
            through_treatment = i + 1 == len(ids) - 1
            if not through_treatment and a["level_cm"] and b["level_cm"] is not None:
                if a["level_cm"] > RULES["blockMinLevel"] and b["level_cm"] / a["level_cm"] < RULES["blockRatio"]:
                    found.append(("BLOCKAGE", d["id"], i, i + 1, ["GBA"], {"up": a["level_cm"], "down": b["level_cm"]}))
            if not through_treatment and a["turbidity_ntu"] is not None and b["turbidity_ntu"] is not None:
                dT = b["turbidity_ntu"] - a["turbidity_ntu"]
                dS = (b["tds_ppm"] or 0) - (a["tds_ppm"] or 0)
                if dT > RULES["turbJump"] or dS > RULES["tdsJump"]:
                    ph = b["ph"] if b["ph"] is not None else 7
                    if ph < RULES["phLow"] or ph > RULES["phHigh"]:
                        found.append(("DISCHARGE", d["id"], i, i + 1, ["KSPCB"], {"dT": dT, "dS": dS, "ph": ph}))
                    else:
                        found.append(("SEWAGE", d["id"], i, i + 1, ["BWSSB", "KSPCB"], {"dT": dT, "dS": dS, "ph": ph}))
            if through_treatment and a["turbidity_ntu"] and b["turbidity_ntu"] is not None:
                eff = (a["turbidity_ntu"] - b["turbidity_ntu"]) / max(1, a["turbidity_ntu"])
                if eff < RULES["treatMin"]:
                    found.append(("TREATMENT", d["id"], i, i + 1, ["KTCDA"], {"eff": eff}))
    ts = now_iso()
    with db() as con:
        for t, drain, a, b, dept, detail in found:
            key = f"{t}:{drain}:{a}-{b}"
            con.execute(
                """INSERT INTO alerts(key,type,drain,a,b,dept,status,created,last_seen,detail) VALUES(?,?,?,?,?,?,?,?,?,?)
                   ON CONFLICT(key) DO UPDATE SET last_seen=excluded.last_seen, detail=excluded.detail,
                   status=CASE WHEN alerts.status='RESOLVED' THEN 'NEW' ELSE alerts.status END""",
                (key, t, drain, a, b, json.dumps(dept), "NEW", ts, ts, json.dumps(detail)),
            )
    return found


@app.get("/api/state")
def state():
    sky = None
    with db() as con:
        row = con.execute("SELECT payload FROM sky WHERE id=1").fetchone()
        if row:
            sky = json.loads(row["payload"])
        alerts = [dict(r) for r in con.execute("SELECT * FROM alerts ORDER BY created DESC LIMIT 200")]
    return {"server_time": now_iso(), "nodes": latest(), "alerts": alerts, "sky": sky}


@app.get("/api/history/{node_id}")
def get_history(node_id: str, n: int = 200):
    return history(node_id, min(n, 5000))


@app.post("/api/actions")
def post_action(a: Action):
    status = "RESOLVED" if a.step.lower().startswith(("mark cleared", "outlet closed", "close", "media cleaned", "sensor fixed")) else "IN PROGRESS"
    with db() as con:
        con.execute("INSERT INTO actions(ts,alert_key,alert_id,step,dept) VALUES(?,?,?,?,?)", (a.ts or now_iso(), a.alert_key, a.alert_id, a.step, a.dept))
        con.execute("UPDATE alerts SET status=? WHERE key=?", (status, a.alert_key))
    return {"ok": True}


@app.get("/api/actions")
def get_actions(limit: int = 200):
    with db() as con:
        return [dict(r) for r in con.execute("SELECT * FROM actions ORDER BY id DESC LIMIT ?", (limit,))]


@app.post("/api/sentinel")
def post_sentinel(payload: dict, x_api_key: str = Header(default="")):
    if x_api_key != API_KEY:
        raise HTTPException(401, "bad api key")
    with db() as con:
        con.execute("INSERT INTO sky(id,payload) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload", (json.dumps(payload),))
    return {"ok": True, "cells": len(payload.get("cells", []))}


@app.get("/api/health")
def health():
    nodes = latest()
    stale = [k for k, v in nodes.items() if time.time() - datetime.fromisoformat(v["ts"].replace("Z", "+00:00")).timestamp() > 900]
    return {"ok": True, "nodes_reporting": len(nodes), "stale_over_15min": stale}


@app.get("/")
def index():
    if DASHBOARD.exists():
        return FileResponse(DASHBOARD)
    return JSONResponse({"error": "dashboard not built; run build.py"}, status_code=404)
