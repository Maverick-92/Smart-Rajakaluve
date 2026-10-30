"""
Sentinel-2 sky view for Bellandur Lake.

Finds the latest clear Sentinel-2 L2A scene (Microsoft Planetary Computer, free, no account),
computes per-pixel water-quality indices over the lake, grids them to ~130 m cells,
ranks the four monitored inlets, and posts the result to the backend for the dashboard.

  NDTI = (B04 red - B03 green) / (B04 + B03)   higher = more suspended sediment / sewage
  NDWI = (B03 - B08) / (B03 + B08)             > 0 means open water
  NDVI = (B08 - B04) / (B08 + B04)             > 0.3 means floating vegetation (hyacinth), masked
  SCL  scene classification: clouds / shadows masked

Install: pip install pystac-client planetary-computer rasterio numpy shapely requests
Run:     python ndti_bellandur.py --post http://localhost:8000 --key change-me
"""
import argparse
import json
from datetime import datetime, timedelta, timezone

import numpy as np
import planetary_computer
import rasterio
import requests
from pystac_client import Client
from rasterio.warp import transform_bounds, transform
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from shapely.geometry import Point, Polygon

# Approximate lake outline (lat, lon). Replace with a surveyed boundary when available.
BELLANDUR = [(12.9445, 77.6430), (12.9462, 77.6500), (12.9445, 77.6580), (12.9422, 77.6660), (12.9385, 77.6740),
             (12.9335, 77.6800), (12.9292, 77.6792), (12.9282, 77.6722), (12.9310, 77.6642), (12.9330, 77.6562),
             (12.9332, 77.6492), (12.9360, 77.6442), (12.9400, 77.6420)]
INLETS = {"KV": (12.9410, 77.6424), "AG": (12.9338, 77.6462), "IB": (12.9286, 77.6705), "CH": (12.9455, 77.6516)}
BBOX = (77.640, 12.926, 77.682, 12.948)   # lon/lat
CLOUD_SCL = {3, 8, 9, 10}                  # shadow, cloud medium, cloud high, cirrus
CELL = 0.0012                              # degrees, ~130 m


def latest_item(days):
    cat = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1", modifier=planetary_computer.sign_inplace)
    end = datetime.now(timezone.utc)
    search = cat.search(collections=["sentinel-2-l2a"], bbox=BBOX,
                        datetime=f"{(end - timedelta(days=days)).date()}/{end.date()}",
                        query={"eo:cloud_cover": {"lt": 60}}, sortby=[{"field": "properties.datetime", "direction": "desc"}])
    items = list(search.items())
    if not items:
        raise SystemExit("No Sentinel-2 scene under 60% cloud in the window; try --days 60")
    return items[0]


def read_band(item, key, ref=None):
    href = item.assets[key].href
    with rasterio.open(href) as src:
        b = transform_bounds("EPSG:4326", src.crs, *BBOX)
        win = from_bounds(*b, transform=src.transform)
        if ref is None:
            arr = src.read(1, window=win).astype("float32")
            return arr, src.window_transform(win), src.crs
        # resample 20 m bands (SCL) to the 10 m grid shape
        arr = src.read(1, window=win, out_shape=ref, resampling=Resampling.nearest)
        return arr, None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--post", default=None, help="backend base URL")
    ap.add_argument("--key", default="change-me")
    ap.add_argument("--out", default="sky_bellandur.json")
    a = ap.parse_args()

    item = latest_item(a.days)
    print("Scene", item.id, item.datetime, "cloud", item.properties.get("eo:cloud_cover"))
    red, tr, crs = read_band(item, "B04")
    green, _, _ = read_band(item, "B03")
    nir, _, _ = read_band(item, "B08")
    scl, _, _ = read_band(item, "SCL", ref=red.shape)

    eps = 1e-6
    ndti = (red - green) / (red + green + eps)
    ndwi = (green - nir) / (green + nir + eps)
    ndvi = (nir - red) / (nir + red + eps)

    lake = Polygon([(lon, lat) for lat, lon in BELLANDUR])
    rows, cols = np.indices(red.shape)
    xs, ys = rasterio.transform.xy(tr, rows.ravel(), cols.ravel())
    lons, lats = transform(crs, "EPSG:4326", xs, ys)
    lons = np.array(lons).reshape(red.shape)
    lats = np.array(lats).reshape(red.shape)

    cloud_mask = np.isin(scl, list(CLOUD_SCL))
    cloud_frac = float(cloud_mask.mean())

    cells = {}
    for (r, c), v in np.ndenumerate(ndti):
        p = Point(lons[r, c], lats[r, c])
        if not lake.contains(p) or cloud_mask[r, c]:
            continue
        key = (round(lats[r, c] / CELL), round(lons[r, c] / CELL))
        veg = ndvi[r, c] > 0.3
        water = ndwi[r, c] > 0
        cell = cells.setdefault(key, {"ndti": [], "veg": 0, "n": 0})
        cell["n"] += 1
        if veg:
            cell["veg"] += 1
        elif water:
            cell["ndti"].append(float(v))

    out_cells = []
    for (ky, kx), c in cells.items():
        veg = c["veg"] > c["n"] / 2
        val = float(np.median(c["ndti"])) if c["ndti"] else 0.0
        out_cells.append({"ll": [ky * CELL, kx * CELL], "ndti": round(val, 4), "veg": bool(veg or not c["ndti"])})

    ranking = []
    for drain, (la, lo) in INLETS.items():
        near = [c["ndti"] for c in out_cells if not c["veg"] and np.hypot((c["ll"][0] - la) * 111, (c["ll"][1] - lo) * 108.5) < 0.45]
        ranking.append({"drain": drain, "ndti": round(float(np.mean(near)), 4) if near else 0.0, "cells": len(near)})
    ranking.sort(key=lambda r: r["ndti"], reverse=True)

    payload = {
        "t": int(item.datetime.timestamp() * 1000),
        "scene": item.id,
        "cloud": round(cloud_frac * 100),
        "usable": cloud_frac < 0.7 and len(out_cells) > 20,
        "cells": out_cells,
        "ranking": ranking,
        "source": f"Sentinel-2 L2A {item.id} via Microsoft Planetary Computer",
    }
    with open(a.out, "w") as f:
        json.dump(payload, f)
    print(f"{len(out_cells)} cells, worst inlet {ranking[0]['drain']} NDTI {ranking[0]['ndti']}; saved {a.out}")
    if a.post:
        r = requests.post(a.post.rstrip("/") + "/api/sentinel", json=payload, headers={"X-API-Key": a.key}, timeout=30)
        print("posted:", r.status_code, r.text)


if __name__ == "__main__":
    main()
