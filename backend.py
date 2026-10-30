import math
import numpy as np
import pandas as pd

# Keep these identical to REPORT.md
PARAMS = {
    "turbidity": {"k": 0.819213, "cstar": 5.0, "unit": "NTU"},
    "bod":       {"k": 0.620857, "cstar": 5.0, "unit": "mg/L"},
    "nitrate":   {"k": 0.403779, "cstar": 1.0, "unit": "mg/L"},
    "phosphate": {"k": 0.322179, "cstar": 0.5, "unit": "mg/L"},
}
def indices(grid):
    b3, b4, b5, b8 = grid["b3"], grid["b4"], grid["b5"], grid["b8"]
    water = (b3 - b8) / (b3 + b8) > 0        # NDWI water mask
    ndti = (b4 - b3) / (b4 + b3)             # turbidity index
    ndci = (b5 - b4) / (b5 + b4)             # algae/nutrient index
    return water, ndti, ndci

def pollution_map(grid):
    """Per-pixel pollution score; land pixels are NaN so they show blank."""
    water, ndti, ndci = indices(grid)
    score = ndti + ndci
    return np.where(water, score, np.nan)

def inlet_scores(grid, inlets, radius=8):
    water, ndti, ndci = indices(grid)
    rows = []
    for inlet in inlets:
        x, y = inlet["x"], inlet["y"]
        ys = slice(max(y - radius, 0), y + radius)
        xs = slice(max(x - radius, 0), x + radius)
        m = water[ys, xs]
        t = ndti[ys, xs][m].mean()
        c = ndci[ys, xs][m].mean()
        # demo coefficients, to be calibrated with field samples
        turb = 20 + 400 * t
        bod = 15 + 300 * t + 200 * c
        nit = 2 + 10 * t + 20 * c
        phos = 0.2 + t + 3 * c
        score = turb / 180 + bod / 140 + nit / 12 + phos / 2.5
        rows.append(dict(name=inlet["name"], turbidity=turb, bod=bod,
                         nitrate=nit, phosphate=phos, score=score))
    return pd.DataFrame(rows).sort_values("score", ascending=False).reset_index(drop=True)

def find_dump(nodes, min_jump=40, ratio=2.0):
    best = None
    for prev, cur in zip(nodes, nodes[1:]):
        jump = cur["bod"] - prev["bod"]
        if jump >= min_jump and cur["bod"] >= ratio * prev["bod"]:
            if best is None or jump > best[1]:
                best = (f"{prev['name']}-{cur['name']}", jump)
    return best

def treat(c_in, param, area_m2, flow_mld):
    q = (flow_mld * 1000) / area_m2          # hydraulic loading, m/day
    p = PARAMS[param]
    c_out = p["cstar"] + (c_in - p["cstar"]) * math.exp(-p["k"] * area_m2 / (flow_mld * 1000))
    return c_out, (1 - c_out / c_in) * 100

def display_value(x):
    return round(x)                     # 39.6 -> 39, 44.8 -> 44

