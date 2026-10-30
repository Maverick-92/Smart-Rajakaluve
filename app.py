import streamlit as st
import plotly.graph_objects as go
from data_store import INLETS, get_lake_grid, get_nodes
from backend import (pollution_map, inlet_scores, find_dump, treat,
                     display_value, PARAMS)
from map_layers import render_map, PLACES

st.set_page_config(page_title="LakeGuard", layout="wide")
st.title("LakeGuard: Detect, Locate, Treat")
st.caption("Track 02, Challenge C4: Heal the Lakes | Bellandur Lake | "
           "prototype with simulated satellite and sensor data")

tab1, tab2, tab3 = st.tabs(["1. Detect (Sentinel-2)",
                            "2. Locate (Smart Rajakaluve nodes)",
                            "3. Treat (Simulator)"])

# ---------------- Dot 1: Detect ----------------
with tab1:
    grid = get_lake_grid()
    df = inlet_scores(grid, INLETS)
    worst = df.iloc[0]["name"]

    st.error(f"Worst inlet: {worst}")

    c1, c2 = st.columns([1, 2])
    place = c1.selectbox("Jump to", list(PLACES.keys()), index=0)
    base = c2.radio("Base layer", ["Satellite", "Street map"], horizontal=True)
    layers = st.multiselect(
        "Layers",
        ["Landmarks", "Inlets", "Drain nodes", "Pollution heat (simulated Sentinel-2)"],
        default=["Landmarks", "Inlets"])
    st.plotly_chart(
        render_map(grid, df, INLETS, get_nodes(False), base, layers, place),
        use_container_width=True, config={"scrollZoom": True})
    st.caption("Simulated Sentinel-2 bands (B3, B4, B5, B8). Water mask: NDWI. "
               "Colour: NDTI + NDCI. Land is blank.")

    with st.expander("Pixel view (raw index map)"):
        pmap = pollution_map(grid)
        fig = go.Figure(go.Heatmap(z=pmap, colorscale="RdYlGn_r",
                                   colorbar=dict(title="Pollution index")))
        for i in INLETS:
            is_worst = i["name"] == worst
            fig.add_trace(go.Scatter(
                x=[i["x"]], y=[i["y"]], mode="markers+text", text=[i["name"]],
                textposition="top center", showlegend=False,
                marker=dict(size=16, color="black" if is_worst else "white",
                            line=dict(width=2, color="black"))))
        fig.update_yaxes(autorange="reversed", scaleanchor="x")
        fig.update_layout(height=500, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Inlet ranking")
    st.dataframe(df.round(2), use_container_width=True)

# ---------------- Dot 2: Locate ----------------
with tab2:
    dump = st.toggle("Simulate illegal dump", value=False)
    nodes = get_nodes(dump)
    cols = st.columns(len(nodes))
    for col, n in zip(cols, nodes):
        icon = "🔴" if n["bod"] > 100 else "🟡" if n["bod"] > 60 else "🟢"
        col.metric(f"{icon} Node {n['name']} ({n['dist_m']} m)",
                   f"{n['bod']} mg/L BOD", f"{n['ntu']} NTU",
                   delta_color="off")
    line = go.Figure(go.Scatter(x=[n["dist_m"] for n in nodes],
                                y=[n["bod"] for n in nodes],
                                mode="lines+markers"))
    line.update_layout(height=300, xaxis_title="Distance along drain (m)",
                       yaxis_title="BOD (mg/L)", margin=dict(t=20))
    st.plotly_chart(line, use_container_width=True)
    result = find_dump(nodes)
    if result:
        st.error(f"Pollution spike on segment {result[0]} "
                 f"(+{result[1]} mg/L BOD). Probable dump zone.")
    else:
        st.success("No anomaly detected along the drain.")
    st.caption("Sensor readings are simulated. BOD shown is a proxy estimated "
               "from turbidity and conductivity, confirmed by lab samples.")

# ---------------- Dot 3: Treat ----------------
with tab3:
    c1, c2 = st.columns(2)
    area = c1.slider("Wetland area (m²)", 5000, 25000, 20000, 1000)
    flow = c2.slider("Inlet flow (MLD)", 1.0, 20.0, 10.0, 0.5)
    inputs = {"turbidity": 180, "bod": 140, "nitrate": 38.0, "phosphate": 12.5}
    cols = st.columns(4)
    for col, (p, c_in) in zip(cols, inputs.items()):
        c_out, rem = treat(c_in, p, area, flow)
        unit = PARAMS[p]["unit"]
        shown = display_value(c_out) if c_in >= 100 else round(c_out, 1)
        col.metric(p.capitalize(), f"{shown} {unit}",
                   f"-{rem:.0f}% (inlet {c_in})")
    st.caption("Model: first-order plug-flow, "
               "C_out = C* + (C_in - C*)·exp(-k/q), q = Q/A. "
               "k values are fitted to the C4 target removals and must be "
               "calibrated in the pilot.")

