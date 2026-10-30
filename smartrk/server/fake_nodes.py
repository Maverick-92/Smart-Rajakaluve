"""Pretend to be the four rig nodes (A, B, C, D) so the live pipeline can be tested without hardware.
Usage: python fake_nodes.py --url http://localhost:8000 --scenario dump   (normal | block | dump)"""
import argparse, random, time, requests

ap = argparse.ArgumentParser()
ap.add_argument("--url", default="http://localhost:8000")
ap.add_argument("--key", default="change-me")
ap.add_argument("--scenario", default="normal", choices=["normal", "block", "dump"])
a = ap.parse_args()

while True:
    # distance from a sensor mounted 30 cm above the gutter floor; smaller distance = higher water
    dist = {"NODE-A": 26.5, "NODE-B": 26.0, "NODE-C": 25.5, "NODE-D": 25.8}
    turb = {"NODE-A": 40, "NODE-B": 44, "NODE-C": 48, "NODE-D": 16}
    ph = {k: 7.2 for k in dist}
    if a.scenario == "block":      # sponge between B and C: B backs up, C runs low
        dist["NODE-B"] = 21.0; dist["NODE-C"] = 28.5
    if a.scenario == "dump":       # muddy, acidic water poured in after A
        for k in ("NODE-B", "NODE-C"): turb[k] += 170; ph[k] = 5.2
        turb["NODE-D"] = 70
    for hw in dist:
        body = {"hw_id": hw, "distance_cm": dist[hw] + random.gauss(0, 0.1), "turbidity_ntu": turb[hw] + random.gauss(0, 2),
                "tds_ppm": 650 + random.gauss(0, 8) + (450 if a.scenario == "dump" and hw in ("NODE-B", "NODE-C") else 0),
                "ph": ph[hw] + random.gauss(0, 0.03), "temp_c": 27 + random.gauss(0, 0.1), "battery": 88}
        r = requests.post(a.url + "/api/readings", json=body, headers={"X-API-Key": a.key}, timeout=10)
        print(hw, r.status_code, r.json().get("level_cm"))
    time.sleep(5)
