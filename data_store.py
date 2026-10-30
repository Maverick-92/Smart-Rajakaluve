import numpy as np

# Corrected contract: nodes every 500 m, K100 is the target inlet
INLETS = [
    {"name": "Northwest HAL/Indiranagar K100", "x": 14, "y": 18},
    {"name": "Koramangala valley drain",       "x": 46, "y": 10},
    {"name": "HSR layout drain",               "x": 52, "y": 46},
    {"name": "Bellandur village drain",        "x": 16, "y": 50},
]

def get_lake_grid(size=64, seed=7):
    rng = np.random.default_rng(seed)
    base = rng.normal(0.08, 0.005, (size, size))
    grid = {"b3": base.copy(), "b4": base.copy(), "b5": base.copy(), "b8": base * 0.4}
    yy, xx = np.mgrid[0:size, 0:size]
    # K100 gets the strongest pollution signal
    for inlet, strength in zip(INLETS, [0.10, 0.05, 0.04, 0.02]):
        blob = np.exp(-(((xx - inlet["x"]) ** 2 + (yy - inlet["y"]) ** 2) / 80))
        grid["b4"] += strength * blob
        grid["b5"] += strength * 1.6 * blob
    return grid

def get_nodes(dump=False):
    nodes = [
        {"name": "A", "ntu": 15, "bod": 12, "dist_m": 0},
        {"name": "B", "ntu": 18, "bod": 15, "dist_m": 500},
        {"name": "C", "ntu": 20, "bod": 16, "dist_m": 1000},
        {"name": "D", "ntu": 22, "bod": 18, "dist_m": 1500, "flow_mld": 10},
    ]
    if dump:
        nodes[2].update(ntu=180, bod=140)
        nodes[3].update(ntu=175, bod=136)
    return nodes
