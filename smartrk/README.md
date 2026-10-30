# Smart Rajakaluve: drain and lake command centre

One system for drain flooding and lake pollution in the Bellandur catchment, Bengaluru:
**Detect** (Sentinel-2 sky view) → **Locate** (sensor nodes compare neighbours) → **Treat** (biofilter at each lake inlet).
GBA and the city corporations, BWSSB, KSPCB and KTCDA work from one dashboard, and each alert has an owner and action steps.

```
firmware/  ESP32 node: level, turbidity, TDS, pH, temperature -> JSON -> backend
server/    FastAPI backend: stores readings (SQLite), runs detection, serves the dashboard
sentinel/  Sentinel-2 NDTI over Bellandur from Microsoft Planetary Computer -> backend
web/       dashboard source (index.html)   dist/  built single-file dashboard
build.py   inlines Leaflet + Three.js into dist/index.html (works offline)
```

## 1. Run the dashboard alone (simulation)
Open `dist/index.html` in Chrome. With internet it loads OpenStreetMap and Sentinel-2 cloudless base maps and live Open-Meteo weather; offline it uses the schematic map and sample weather. Use the scenario buttons on the left to inject a blockage, dumping, sewage leak, heavy rain, a sensor fault or a satellite pass.

## 2. Run with the backend (live mode)
```bash
cd server
pip install -r requirements.txt
SRK_API_KEY=change-me uvicorn app:app --host 0.0.0.0 --port 8000
# open http://<laptop-ip>:8000  -> badge shows LIVE + SIM
python fake_nodes.py --scenario dump     # test without hardware: normal | block | dump
```
Live readings replace the simulated values of the mapped nodes (`server/config.json`). The demo rig maps nodes A, B, C, D to the Agara–HSR drain (AG-1, AG-2, AG-3, AG-T). The remaining nodes stay simulated and are labelled SIM.

API: `POST /api/readings` (header `X-API-Key`), `GET /api/state`, `GET /api/history/{node}`, `POST /api/actions`, `POST /api/sentinel`, `GET /api/health`.

## 3. Flash the nodes
Open `firmware/smart_rajakaluve_node/smart_rajakaluve_node.ino` in the Arduino IDE (board: ESP32 Dev Module; libraries: OneWire, DallasTemperature, ArduinoJson). Set Wi-Fi, `API_URL`, `API_KEY` and a unique `HW_ID` per node. Calibrate pH with pH 4 and 7 buffers, and turbidity in clear and muddy water. For the demo set `SLEEP_SECONDS = 10`.

**Demo rig:** gutter → A → B → (sponge goes here for a blockage) → C → filter box (gravel, sand, charcoal) → D. Mount the ultrasonic sensors 30 cm above the gutter floor; `level_scale` in config.json converts rig centimetres to full-size drain centimetres.

## 4. Sentinel-2 sky view
```bash
pip install pystac-client planetary-computer rasterio numpy shapely requests
python sentinel/ndti_bellandur.py --post http://localhost:8000 --key change-me
```
This picks the latest scene under 60% cloud, masks clouds (SCL), floating vegetation (NDVI > 0.3) and non-water (NDWI ≤ 0), grids NDTI to about 130 m cells and ranks the four inlets. Run it daily (cron); a new usable scene appears about every 5 days.

## Detection rules (same in dashboard and backend; tune in config.json)
| Alert | Trigger | Routed to |
|---|---|---|
| Blockage | upstream level > 55 cm and downstream/upstream < 0.55 | GBA / corporation |
| Overflow risk | level > 85% of drain depth | GBA / corporation |
| Industrial discharge | turbidity +70 NTU or TDS +300 ppm between neighbours, pH outside 6–9 | KSPCB |
| Sewage ingress | same jump, pH near neutral | BWSSB + KSPCB |
| Treatment underperforming | inlet biofilter removes < 40% turbidity | KTCDA |
| Sensor fault | no change for 6 readings | Operations |
| Satellite hotspot | worst inlet NDTI > 0.08 on a clear pass | KSPCB + KTCDA |

Every rule must hold for 2 readings in a row before an alert is raised.

## What is real and what is simulated
- Real: detection logic, backend, firmware, Sentinel-2 processing, Open-Meteo weather (when online).
- Simulated: drain hydraulics for nodes without hardware, the treatment-unit removal model, sponge (42% runoff held) and virtual-lake (30%) effects. These are illustrative design values, not measured results.
- Approximate: lake outlines, drain alignments and valley shapes are schematic, not surveyed. Replace them with GBA drain GIS data before a real pilot.
- Wetland sizing must come from a published constructed-wetland design method.

Map data © OpenStreetMap contributors. Sentinel-2 cloudless by EOX IT Services GmbH (contains modified Copernicus Sentinel data). Weather: Open-Meteo.
