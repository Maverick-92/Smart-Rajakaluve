# LakeGuard: Detect, Locate, Treat

**Track 02, Challenge C4: Heal the Lakes | Bellandur Lake, Bengaluru**

A software prototype that connects three decisions into one chain:

1. **Detect:** Sentinel-2 water-colour indices (NDWI mask, NDTI turbidity, NDCI chlorophyll) rank the lake inlets and flag the worst one (Northwest HAL / Indiranagar K100 feeder drain).
2. **Locate:** four sensor nodes (A to D, 500 m apart) along that drain. The first reach with a persistent jump in turbidity and BOD is flagged as the probable discharge zone (B to C).
3. **Treat:** an inlet treatment simulator sizes a constructed wetland + floating treatment wetland with a first-order plug-flow k-C* model and reports removal of turbidity, BOD, nitrate and phosphate.

> **All satellite and sensor data in this prototype is simulated.** Treatment coefficients are fitted to the challenge targets and must be calibrated with field data in a pilot. See `REPORT.md` for assumptions and limits.

## Run the dashboard

    pip install -r requirements.txt
    streamlit run app.py

Tabs: **1. Detect** (layered map with Satellite or Street base, Landmarks, Inlets, Drain nodes, Pollution heat, and a "Jump to" menu), **2. Locate** (dump toggle shows the B to C alert), **3. Treat** (area and flow sliders with live removal metrics).

## Reference case (10 MLD, 20,000 m2)

| Indicator | Inlet | Treated | Removal |
|---|---|---|---|
| Turbidity | 180 NTU | 39 NTU | 78% |
| BOD | 140 mg/L | 44 mg/L | 68% |
| Nitrate | 38.0 mg/L | 17.5 mg/L | 54% |
| Phosphate | 12.5 mg/L | 6.8 mg/L | 46% |

Model: `C_out = C* + (C_in - C*) * exp(-k_A * A / Q)`, A in m2 and Q in m3/day.

## Smart Rajakaluve command centre

`smartrk/` holds the companion city dashboard: sensor network, 3D drain simulation, Sentinel-2 sky view, alerts by department (GBA, BWSSB, KSPCB, KTCDA) and ESP32 node firmware. Open `smartrk/dist/index.html` in a browser (needs internet for map tiles).

## Files

| Path | Purpose |
|---|---|
| `app.py` | Streamlit dashboard |
| `backend.py` | Band indices, inlet ranking, dump finder, treatment model |
| `data_store.py` | Simulated lake grid, inlets, sensor readings |
| `map_layers.py` | Layered map |
| `REPORT.md` | Full technical report |
| `smartrk/` | Command centre, server, firmware, Sentinel script |

## Limits

- Sentinel-2 is a screening tool, not a measurement of BOD, nitrate or phosphate.
- A flagged drain reach means "inspect here", not proof of illegal dumping.
- Wetland performance depends on pretreatment, hydraulics and maintenance. These are scenario results, not field results.
