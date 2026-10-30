import numpy as np
import plotly.graph_objects as go
from backend import pollution_map

# Approximate coordinates (lat, lon, zoom). Tweak if a pin looks off.
PLACES = {
    "Bellandur Lake":        (12.9350, 77.6700, 13.3),
    "HAL / old airport":     (12.9500, 77.6680, 14.0),
    "Indiranagar":           (12.9784, 77.6408, 14.0),
    "Koramangala":           (12.9352, 77.6245, 14.0),
    "Agaram":                (12.9330, 77.6270, 14.5),
    "Iblur":                 (12.9238, 77.6612, 14.5),
    "HSR Layout":            (12.9116, 77.6389, 14.0),
    "Silk Board":            (12.9177, 77.6233, 14.5),
    "Varthur Lake":          (12.9390, 77.7450, 13.5),
    "Bengaluru (overview)":  (12.9500, 77.6500, 11.0),
}

# Simulated grid footprint, placed over the lake (approximate)
S, N, W, E = 12.918, 12.952, 77.652, 77.688

def px_to_ll(x, y, size):
    lat = N - (y / size) * (N - S)
    lon = W + (x / size) * (E - W)
    return lat, lon

def lake_mask(size):
    yy, xx = np.mgrid[0:size, 0:size]
    c = size / 2
    return ((xx - c) / (size * 0.485)) ** 2 + ((yy - c) / (size * 0.44)) ** 2 <= 1

def render_map(grid, df, inlets, nodes, base, layers, place):
    size = grid["b4"].shape[0]
    worst = df.iloc[0]["name"]
    fig = go.Figure()

    if "Pollution heat (simulated Sentinel-2)" in layers:
        pm = pollution_map(grid)
        pm = np.where(lake_mask(size), pm, np.nan)
        ys, xs = np.where(~np.isnan(pm))
        lat, lon = px_to_ll(xs, ys, size)
        fig.add_trace(go.Scattermap(
            lat=lat, lon=lon, mode="markers", hoverinfo="skip", name="Pollution",
            marker=dict(size=11, opacity=0.55, color=pm[ys, xs],
                        colorscale="RdYlGn_r",
                        colorbar=dict(title="Pollution index"))))

    if "Landmarks" in layers:
        names = [k for k in PLACES if k != "Bengaluru (overview)"]
        fig.add_trace(go.Scattermap(
            lat=[PLACES[k][0] for k in names], lon=[PLACES[k][1] for k in names],
            mode="markers+text", name="Landmarks", text=names,
            textposition="bottom right", textfont=dict(size=12, color="white"),
            marker=dict(size=9, color="deepskyblue")))

    if "Inlets" in layers:
        pts = [px_to_ll(i["x"], i["y"], size) for i in inlets]
        fig.add_trace(go.Scattermap(
            lat=[p[0] for p in pts], lon=[p[1] for p in pts],
            mode="markers+text", name="Inlets",
            text=[i["name"] for i in inlets], textposition="top right",
            textfont=dict(size=13, color="white"),
            marker=dict(size=[20 if i["name"] == worst else 12 for i in inlets],
                        color=["red" if i["name"] == worst else "white" for i in inlets])))

    if "Drain nodes" in layers:
        w = next(i for i in inlets if i["name"] == worst)
        lat0, lon0 = px_to_ll(w["x"], w["y"], size)
        step = 0.0045   # about 500 m in latitude
        fig.add_trace(go.Scattermap(
            lat=[lat0 + k * step for k in range(len(nodes))],
            lon=[lon0] * len(nodes),
            mode="lines+markers+text", name="Drain nodes",
            text=[f"Node {n['name']}" for n in nodes], textposition="middle right",
            textfont=dict(size=13, color="white"),
            line=dict(width=3, color="cyan"),
            marker=dict(size=12,
                        color=["red" if n["bod"] > 100 else "yellow" if n["bod"] > 60 else "lime"
                               for n in nodes])))

    sat = [dict(below="traces", sourcetype="raster", sourceattribution="Esri World Imagery",
                source=["https://server.arcgisonline.com/ArcGIS/rest/services/"
                        "World_Imagery/MapServer/tile/{z}/{y}/{x}"])]
    lat, lon, zoom = PLACES[place]
    fig.update_layout(
        height=650, margin=dict(l=0, r=0, t=0, b=0), uirevision=place,
        legend=dict(bgcolor="rgba(0,0,0,0.5)", font=dict(color="white")),
        map=dict(style="white-bg" if base == "Satellite" else "open-street-map",
                 layers=sat if base == "Satellite" else [],
                 center=dict(lat=lat, lon=lon), zoom=zoom))
    return fig
