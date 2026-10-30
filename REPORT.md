# LakeGuard: Detect, Trace, Treat — Satellite-Guided Pollution Tracing & Inlet Wetland Design

**Track:** Track 02  
**Challenge:** C4 — "Heal the Lakes"  
**Target:** Bellandur Lake, Bengaluru  
**Intervention:** Northwest Inlet — HAL / Indiranagar K100 Rajakaluve feeder drain  
**Submission type:** Technical design report for a software-based simulation prototype

**Project proposition:** Use satellite observations to prioritize a polluted inlet, a simulated upstream monitoring network to localize an anomalous drain segment, and a transparent wetland sizing model to estimate treatment at the lake gate. The decision chain is **Detect → Trace → Treat**.

**Evidence boundary:** The named site, comparative inlet condition, sensor readings, and nominal removal targets are supplied challenge assumptions. This report does not claim a verified satellite scene, installed sensors, completed software, agency notifications, or field-demonstrated treatment. It specifies the prototype and its engineering model so judges can distinguish the demonstration from deployment evidence. The required storyline in Section 3 is reproduced verbatim; the accompanying technical explanations define its scientific and operational limits.

---

## SECTION 1: AREA CHOSEN (Named Class E Lake & Specific Inlet)

### 1.1 Target and intervention boundary

| Item | Selected scope | Significance |
|---|---|---|
| Target lake | **Bellandur Lake, Bengaluru** | A severely polluted urban lake serving a large upstream catchment and discharging toward the downstream lake system. |
| Challenge classification | **Class E**, as specified in the brief | CPCB's designated-best-use Class E concerns irrigation, industrial cooling, and controlled waste disposal. It is a use category, not a universal numerical severity score. A current official classification must be checked before deployment. |
| Lake area | **900 acres / approximately 360 hectares** | 900 acres converts to approximately 364 hectares; 360 hectares is the rounded figure used in the brief. |
| Specific intervention site | **Northwest Inlet — HAL / Indiranagar K100 Rajakaluve stormwater and sewage feeder drain** | The challenge-designated gateway for upstream tracing and inlet treatment. |
| Upstream tracing reach | Four virtual nodes across **1.5 km**, at **500 m** intervals | Supports segment-level anomaly localization rather than a lake-wide sensor grid. |
| Design inlet flow | **10 MLD** | A simulated treatment design flow; it is not a measured estimate of total Bellandur inflow. |
| Initial treatment footprint | **20,000 m²**, with a **5,000–25,000 m²** simulator range | Equivalent to 2 hectares at the reference setting; availability and hydraulic suitability require site survey. |

The HAL / Indiranagar / K100 naming and Northwest inlet association are adopted from the challenge brief. Surveyed coordinates, drain connectivity, asset ownership, and inlet orientation must be reconciled with authoritative drainage maps before selecting land or attributing a discharge.

### 1.2 Why this inlet and why satellite targeting?

Bellandur Lake spans approximately **900 acres**, making comprehensive hardware coverage at fine spatial spacing physically impractical and financially prohibitive for this prototype. Sentinel-2 provides freely available imagery at **10 m–20 m spatial resolution** for the relevant bands, allowing lake-wide screening of water color, suspended-material patterns, and algal-bloom proxies.

The demonstration represents the Northwest corner as the strongest pollution-plume hotspot and the South inlet as relatively cleaner. This supplies a clear targeting hypothesis: concentrate the drain investigation and treatment design at the Northwest gateway. A real deployment must establish this ranking from dated, quality-controlled scenes and corroborating water samples.

| Comparison | Northwest inlet in the demonstration | South inlet in the demonstration | Decision |
|---|---|---|---|
| Relative turbidity-index pattern | Strong plume signature | Lower index response | Prioritize Northwest for inspection. |
| Algal-bloom proxy | Elevated response in affected water | Lower relative response | Check nutrient enrichment through sampling. |
| Upstream tracing | Node B–C jump represented in the scenario | No equivalent tracing evidence supplied | Investigate the Northwest feeder reach first. |
| Treatment action | Size interception and wetland treatment at its mouth | Retain as a monitoring comparison | Allocate effort using evidence and update priorities over time. |

A green map color is a display convention and does not establish that water is safe or chemically clean. Sentinel-2 can identify surface patterns; it cannot directly measure sewage volume, BOD, nitrate, phosphate, pathogens, or industrial toxicity.

---

## SECTION 2: THE CORE PROBLEM STATEMENT

LakeGuard addresses three connected gaps that can undermine Bengaluru lake rejuvenation: **no macro-targeting, no upstream source accountability, and no engineering sizing at the inlet gate**. These are the project's problem framing, rather than a claim that every agency project fails for the same reasons.

| Root problem | Present operational failure | Why rejuvenation underperforms | LakeGuard's response |
|---|---|---|---|
| **1. Blind Lake-Wide Spending (No Macro-Targeting)** | Civic agencies can deploy floating wetlands or aerators across massive lakes without knowing which inlet is currently delivering the highest turbidity, sewage, and nutrient load. | Treatment can miss the active entry plume while recurring upstream pollution overwhelms improvements. | Use lake-wide satellite screening to prioritize inlet inspections, then confirm loads with flow and water-quality measurements. |
| **2. Untraced Upstream Dumping (No Source Accountability)** | Untreated sewage and industrial effluents enter Bellandur and Varthur through multiple hidden points along upstream rajakaluves. Pollution becomes visible after mixing in the lake. | A lake sample cannot identify which specific **500 m drain stretch** introduced the discharge, delaying inspection and repair. | Compare neighboring drain nodes and identify the reach where a persistent, travel-time-aligned pollution increase first appears. |
| **3. Unquantified Inlet Treatment (No Engineering Sizing at the Gate)** | Identifying a drain does not stop its flow while enforcement proceeds. Treatment planning lacks a rapid, transparent link from flow in **MLD** and pollution indicators in **NTU / BOD** to wetland area and predicted removal. | Undersized or poorly placed interventions cannot reliably intercept the load entering the lake. | Convert inlet measurements into concentrations, daily loads, modeled wetland outputs, and **area required per MLD**, with explicit assumptions. |

**Core problem statement:** Bengaluru needs a connected decision workflow that first identifies the priority inlet, then narrows the upstream investigation to a responsible drain segment, and finally quantifies treatment at the gate while source-control action proceeds.

A satellite hotspot alone is not a pollution mass-load ranking. A measured load needs both concentration and flow, and suspected dumping needs inspection and laboratory evidence before legal attribution.

---

## SECTION 3: THE SOLUTION — HOW THE 3 DOTS CONNECT (THE STORYLINE)

### How the 3 Dots Connect (The Storyline)

#### Dot 1: SEE IT FROM SPACE (Sentinel-2 Vision)
- **What happens:** You cannot put sensors in every inch of a 900-acre lake. So, our system starts with a Sentinel-2 Satellite View of Bellandur Lake.
- **What it shows:** Sentinel-2 looks at the water color (using Band 4/Band 3 for NDTI Turbidity and Band 5/Band 4 for NDCI Chlorophyll/Algal Blooms) and spots a massive bright red pollution plume spreading from the Northwest corner (the HAL / Indiranagar drain inlet), while the South inlet looks mostly green/clean.
- **Why it matters:** Without spending a single rupee on hardware, Sentinel-2 just told us which inlet is killing the lake right now.

#### Dot 2: TRACE THE CULPRIT UPSTREAM ("Pollution Detective" Network)
- **What happens:** Now that Sentinel-2 pointed to the Northwest inlet, the user clicks on that inlet on the map to zoom into the feeder drain (rajakaluve) coming into that corner.
- **What it shows:** Along this drain, the map shows 4 virtual sensor nodes (Node A, Node B, Node C, Node D) spaced 500 meters apart. Since this is a software-based simulation prototype, the software simulates live readings from these nodes:
  * **Node A (0.0 km):** Turbidity = 15 NTU, BOD = 12 mg/L (Normal)
  * **Node B (0.5 km):** Turbidity = 18 NTU, BOD = 15 mg/L (Normal)
  * **Node C (1.0 km):** Turbidity = 180 NTU, BOD = 140 mg/L (CRITICAL SPIKE! )
  * **Node D (1.5 km - Lake Inlet Gate):** Turbidity = 175 NTU, BOD = 136 mg/L, Flow = 10 MLD (Entering Lake)
- **Why it matters:** Because pollution jumped suddenly between Node B and Node C, the system highlights that exact 500m stretch of drain in red and alerts KSPCB/BWSSB: *"Illegal sewage/industrial discharge detected between Node B & C!"*

#### Dot 3: HEAL THE INLET (What the C4 Challenge Rubric Demands)
- **What happens:** While authorities go to fine the culprit between Node B and C, that toxic water is still flowing down the drain toward the lake! We have to stop it at the lake gate.
- **What it shows:** At the bottom of the screen, the system opens the "Inlet Treatment Simulator." Since the sensors at Node C & D already measured how much water is flowing (10 MLD) and how dirty it is (Turbidity = 180 NTU, BOD = 140 mg/L), the system automatically recommends building a Constructed Wetland + Floating Treatment Wetland right at the Northwest inlet mouth.
- **Interactive Sliders for the Judges:** We provide interactive parameters to adjust the size of the wetland (from 5,000 m² to 25,000 m², calibrated at 20,000 m²) and pick the plant type (Canna / Typha / Vetiver). As adjusted, the model outputs the exact numbers on the C4 grading sheet:
  * **Turbidity Removed:** 78% (Drops from 180 NTU to 39 NTU)
  * **BOD Removed:** 68% (Drops from 140 mg/L to 44 mg/L)
  * **Nitrate & Phosphate Removed:** 54% & 46% (Nitrate drops from 38.0 mg/L to 17.5 mg/L; Phosphate drops from 12.5 mg/L to 6.8 mg/L)
  * **Area Required per MLD:** 2,000 m²/MLD (20,000 m² total area for 10 MLD flow)

### 3.1 Technical explanation and table — Dot 1: Sentinel-2 vision

**Observation method.** Use Sentinel-2 Level-2A surface reflectance, a surveyed lake boundary, and polygons around mapped inlets. Mask clouds, cloud shadows, land, shoreline vegetation, foam, and invalid pixels before evaluating water indices. Prefer repeatable comparisons across scenes with similar processing and record the acquisition date.

The normalized-difference indices are:

**NDTI = (B4 − B3) / (B4 + B3)**  
**NDCI = (B5 − B4) / (B5 + B4)**

The storyline's “Band 4/Band 3” and “Band 5/Band 4” identify band pairs; the actual computations above are normalized differences, not simple band ratios.

| Element | Technical specification | Output and interpretation |
|---|---|---|
| B3 — green | Approximately 560 nm; native **10 m** pixels | Supports the visible water-color contrast in NDTI. |
| B4 — red | Approximately 665 nm; native **10 m** pixels | Used in both indices. |
| B5 — red edge | Approximately 705 nm; native **20 m** pixels | Provides the red-edge contrast used in NDCI. |
| Spatial alignment | Aggregate B4 to the B5 **20 m** grid for NDCI | Resampling B5 to 10 m would not create additional native spatial detail. |
| NDTI layer | Dimensionless suspended-material proxy | Relative turbidity screening; converting to NTU requires local paired samples. |
| NDCI layer | Dimensionless chlorophyll-related proxy | Bloom screening; converting to chlorophyll concentration requires calibration. |
| Inlet prioritization | Compare valid-water index distributions, plume extent, and change from baseline around each inlet | Produce a ranked investigation list with scene date and confidence. |
| Map styling | A documented red-to-green relative-index scale | Red highlights stronger proxy response; green indicates lower response within the chosen scale. |
| Update cadence | New usable satellite acquisitions | Sentinel-2 is not a continuous live feed; Bengaluru cloud cover can leave gaps. |

**Quality safeguards.** Very turbid, optically shallow, foam-covered, or vegetated water can distort interpretation. Mixed pixels are especially important at inlet mouths. The system must display “insufficient valid observations” when imagery is unusable rather than force a hotspot ranking. A dated historical scene must retain its historical timestamp.

**Practical value.** Satellite screening covers the lake without purchasing a dense hardware grid. Data preparation, hosting, interpretation, field sampling, and subsequent sensor deployment still have costs.

### 3.2 Technical explanation and table — Dot 2: upstream pollution tracing

**Network direction.** Chainage increases downstream: **A → B → C → D → lake**. Each node records time, position, source type, quality flags, turbidity, and available water-quality measurements. Node D supplies the simulated **10 MLD** flow. Node C supplies the conservative concentration envelope used for sizing.

| Node | Downstream chainage | Turbidity (NTU) | BOD (mg/L) | Flow (MLD) | Scenario interpretation |
|---|---:|---:|---:|---:|---|
| A | 0.0 km | 15 | 12 | Not supplied | Upstream baseline; “normal” is a scenario label, not a clean-water standard. |
| B | 0.5 km | 18 | 15 | Not supplied | Small increase above A. |
| C | 1.0 km | 180 | 140 | Not supplied | Critical concentration spike after B. |
| D | 1.5 km — lake inlet gate | 175 | 136 | 10 | Pollution persists to the lake entrance. |

| Adjacent reach | Turbidity change | BOD change | Interpretation |
|---|---:|---:|---|
| A → B | +3 NTU; **1.20×** BOD | +3 mg/L | Small baseline fluctuation in this scenario. |
| **B → C** | **+162 NTU; 10× turbidity** | **+125 mg/L; 9.33× BOD** | Strongest anomalous reach; highlight the **500 m segment** for inspection. |
| C → D | −5 NTU | −4 mg/L | Minor decline; pollution remains high at the inlet. |

**Detection logic.** The prototype compares adjacent-node changes against an upstream baseline and measurement uncertainty. It requires persistence across several readings and alignment for water travel time. Ratios alone are insufficient when upstream concentrations approach zero; absolute changes are also needed. Real deployments must account for tributaries, rainfall, dilution, resuspension, backwater, and sensor faults.

**Measurements and accountability.** Turbidity and suitable flow measurements can be collected continuously. BOD is normally determined through a laboratory incubation test; an online BOD estimate would require a locally validated surrogate and must be labeled as estimated. Nitrate and phosphate values in this report are simulated or laboratory inputs. No claim is made that Sentinel-2 or a low-cost turbidity sensor directly measures them.

The required alert text is preserved in the storyline. In an operational system, it should accompany the status **“suspected discharge anomaly; inspection required”**, rather than constitute proof of illegal activity. The network narrows the search to B–C; it cannot identify a specific premises or distinguish sewage from industrial effluent without further evidence.

| Investigation packet | Contents | Action enabled |
|---|---|---|
| Segment map | Surveyed B and C positions, drain connectivity, and highlighted reach | Dispatch an inspection team to the relevant 500 m stretch. |
| Time-series evidence | Synchronized readings, baseline, spike magnitude, persistence, and quality flags | Separate a recurring event from transient noise. |
| Field sampling plan | Upstream, discharge-point, downstream, and inlet samples | Confirm chemistry and potential source type. |
| Compliance record | Inspection findings, laboratory results, photographs, and chain of custody | Support enforcement under applicable procedures. |
| Repair referral | Confirmed sewer defect location and responsible asset owner | Enable BWSSB repair and subsequent verification. |

The prototype can display a draft incident packet. Agency alerts are a proposed integration; no actual messages or enforcement actions are claimed in this submission.

### 3.3 Technical explanation and table — Dot 3: inlet treatment design

**Treatment concept.** Route the design flow through accessible screening, grit removal, flow measurement, and a solids-management forebay before a **Constructed Wetland (CW)** and a hydraulically connected **Floating Treatment Wetland (FTW)** polishing cell. Provide maintenance access, controlled distribution, sampling points, and a defined high-flow route.

CW treatment combines settling or filtration, biofilm-mediated organic removal, and suitable aerobic/anoxic processes. FTWs add root-associated biofilm and plant uptake where appropriate. Phosphorus retention needs suitable media or solids removal, and plant-associated nutrients must be exported through harvesting. Pollutants are not removed simply by placing plants on open water.

| Simulator input | Reference setting | Role and constraint |
|---|---|---|
| Inlet flow | **10 MLD = 10,000 m³/day** | Controls hydraulic loading and pollutant mass loads. |
| Conservative turbidity | **180 NTU** | Node C concentration used for sizing; D is 175 NTU. |
| Conservative BOD | **140 mg/L** | Node C concentration used for sizing; D is 136 mg/L. |
| Nitrate | **38.0 mg/L** | Supplied scenario input; reporting basis must be fixed before field use. |
| Phosphate | **12.5 mg/L** | Supplied scenario input; reporting basis must be fixed before field use. |
| Total treatment area | **20,000 m²**, adjustable **5,000–25,000 m²** | Combined treatment footprint in the simplified model. |
| Plant selector | **Canna / Typha / Vetiver** | Supports planting-plan comparisons; removal differences need species- and site-specific evidence. |
| Model parameters | Pollutant-specific areal rate and background concentration | Fitted scenario coefficients, not measured Bellandur treatment constants. |

**Conservative design rule.** Use the larger of the contemporaneous C and D concentrations together with D's flow for provisional sizing. This combines an upstream concentration envelope with the inlet flow; it is not a measured mass balance at C. A deployment should replace it with representative, flow-weighted inlet sampling and peak-flow analysis.

**Plant choices.**

| Plant | Potential role | Design condition |
|---|---|---|
| Canna | Planted wetland cells and suitably supported FTW modules | Verify local suitability, root establishment, harvesting, and survival. |
| Typha | Emergent wetland zones | Manage spreading, accumulated biomass, and access for maintenance. |
| Vetiver | Bank stabilization and engineered root-zone modules | Use an appropriate locally accepted cultivar and validate performance in the proposed configuration. |

The plant selector must not invent removal advantages. Until pilot data support separate coefficients, all three options retain the same reference treatment outputs and change the planting plan. A future validated species option may update coefficients with documented uncertainty.

**Hydraulic feasibility.** At 20,000 m² and 10 MLD, hydraulic loading is **0.50 m/day**, and the incoming BOD loading is **70 g/m²/day**. These are demanding conditions for passive treatment of raw wastewater. At an illustrative 0.6 m operating depth, ideal free-water residence time is only **1.2 days**; a subsurface configuration with effective porosity 0.35 would have approximately **0.42 days** under the same simplified geometry. Actual hybrid residence time depends on cell allocation, porosity, short-circuiting, and water level.

Consequently, the recommended footprint is a **scenario sizing result**, subject to pretreatment, pilot validation, land survey, storm-flow management, and possible expansion or flow diversion. The aggregate model does not count CW and FTW removal twice.

### 3.4 Connected architecture and judge demonstration

| Stage | Input | Processing | Reviewable output |
|---|---|---|---|
| Detect | Sentinel-2 reflectance, lake mask, inlet polygons | Quality filtering, index calculation, inlet comparison | Dated hotspot map with an explicit imagery-confidence indicator. |
| Trace | Simulated A–D readings and mapped drain reach | Adjacent-node anomaly analysis | Highlighted B–C segment and draft investigation packet. |
| Treat | D flow, C/D concentration envelope, nutrient inputs, chosen area | First-order wetland model and mass-load calculation | Treated concentrations, removal percentages, area/MLD, and feasibility indicators. |
| Audit | Input values, units, timestamps, source flags, model version | Provenance and validation checks | Reproducible explanation of each recommendation. |

**Judge walkthrough:** Inspect the Northwest plume scenario; select that inlet; review the four simulated nodes; observe the B–C spike; open the treatment simulator; adjust area and plant choice; check the reference case against Section 4. The map, virtual sensor stream, alert packet, and sliders describe intended prototype behavior rather than verified implemented features.

**Novelty:** LakeGuard connects a broad satellite screening decision to a specific upstream investigation and then to a quantified inlet intervention. The contribution is this evidence-to-action workflow, with transparent boundaries between observation, inference, and treatment prediction.

---

## SECTION 4: C4 RUBRIC SUMMARY TABLE & ENGINEERING MODEL

### 4.1 Reference-case C4 summary

The following table evaluates the outputs requested in the supplied C4 brief. It is not an independently verified official scoring sheet or a treatment-compliance certification.

| C4 metric | Baseline inlet/design input at C/D | Post-wetland modeled output | Calculated removal | Required storyline label | Area per MLD |
|---|---:|---:|---:|---:|---:|
| Turbidity | **180 NTU**; conservative C value | **39 NTU** | **78.33%** | **78%** | **2,000 m²/MLD** |
| BOD | **140 mg/L**; conservative C value | **44 mg/L** | **68.57%** | **68%** | **2,000 m²/MLD** |
| Nitrate | **38.0 mg/L**; supplied scenario input | **17.5 mg/L** | **53.95%** | **54%** | **2,000 m²/MLD** |
| Phosphate | **12.5 mg/L**; supplied scenario input | **6.8 mg/L** | **45.60%** | **46%** | **2,000 m²/MLD** |
| Design flow | **10 MLD** | **10 MLD**, assuming no net water loss or bypass | Not a removal metric | **10 MLD** | **20,000 m² / 10 MLD** |
| Total treatment footprint | **20,000 m² = 2 ha** | Same installed area | Not applicable | **20,000 m²** | **2,000 m²/MLD** |

**Numerical consistency:** The required storyline's 78%, 68%, 54%, and 46% are retained as nominal labels. Exact arithmetic for its stated concentration endpoints gives the percentages above. In particular, 140 → 44 mg/L equals **68.57%**, not exactly 68%; an exact 68% reduction would produce **44.8 mg/L**. Similarly, an exact 78% reduction from 180 NTU would produce **39.6 NTU**. The model below is fitted to the stated concentration endpoints.

### 4.2 First-order plug-flow k–C* model

For each modeled pollutant or indicator:

**C_out = C* + (C_in − C*) × exp(−k_A × A / Q)**

**Removal (%) = 100 × (C_in − C_out) / C_in**

**A_required = (Q / k_A) × ln[(C_in − C*) / (C_target − C*)]**

**Area per MLD = A / Q_MLD**

| Symbol | Meaning | Unit or condition |
|---|---|---|
| C_in | Design influent concentration or turbidity indicator | mg/L or NTU, consistently for each row |
| C_out | Predicted treated concentration or indicator | Same unit as C_in |
| C* | Residual/background concentration assumed by the model | Same unit; target must exceed C* |
| k_A | Effective areal first-order removal coefficient | **m/day** |
| A | Combined effective treatment footprint | **m²** |
| Q | Flow through the treatment cells | **m³/day**; 1 MLD = 1,000 m³/day |
| Q_MLD | Flow expressed in million litres per day | **MLD** |

The exponent is dimensionless: **(m/day × m²) / (m³/day) = 1**. This areal form must not be confused with a volumetric rate constant in day⁻¹, which requires residence time.

The simplified model assumes steady flow, approximate plug flow, constant effective rate coefficients, and a represented residual background. It omits temperature variation, shock toxicity, media saturation, water losses, bypass, and detailed oxygen balances. Applying exponential decay to NTU is an empirical indicator model; turbidity is not a conserved chemical concentration.

### 4.3 Explicit reference calibration

At **Q = 10,000 m³/day** and **A = 20,000 m²**, choose the following demonstration background values and calculate:

**k_A = (Q / A) × ln[(C_in − C*) / (C_out − C*)]**

| Parameter | C_in | Fitted C_out | Assumed C* | Calibrated k_A (m/day) | Evidence status |
|---|---:|---:|---:|---:|---|
| Turbidity | 180 NTU | 39 NTU | 5 NTU | **0.819213** | Empirical scenario fit. |
| BOD | 140 mg/L | 44 mg/L | 5 mg/L | **0.620857** | Scenario fit; requires pilot validation. |
| Nitrate | 38.0 mg/L | 17.5 mg/L | 1.0 mg/L | **0.403779** | Scenario fit; nitrogen basis and process conditions need validation. |
| Phosphate | 12.5 mg/L | 6.8 mg/L | 0.5 mg/L | **0.322179** | Scenario fit; media capacity and harvest regime need validation. |

These coefficients are reverse-calculated to reproduce the brief's endpoint concentrations. They demonstrate a consistent simulator, not independently predictive performance. Real coefficients must be estimated from paired flow-weighted influent/effluent data and tested on separate observations.

### 4.4 Pollutant-load interpretation

For a constituent reported in mg/L:

**Load (kg/day) = concentration (mg/L) × flow (MLD)**

| Constituent | Conservative design load at 10 MLD | Modeled outlet load | Modeled load reduction |
|---|---:|---:|---:|
| BOD | **1,400 kg/day** | **440 kg/day** | **960 kg/day** |
| Nitrate, on the same stated analytical basis | **380 kg/day** | **175 kg/day** | **205 kg/day** |
| Phosphate, on the same stated analytical basis | **125 kg/day** | **68 kg/day** | **57 kg/day** |
| Turbidity | **180 NTU** | **39 NTU** | **141 NTU decrease**; cannot be converted to kg/day without a local solids relationship. |

“Nitrate” may be reported as NO₃⁻ or as nitrogen, and “phosphate” as PO₄³⁻ or as phosphorus. Because the supplied brief does not specify the basis, this report preserves its labels and makes no conversion to elemental N or P. Field data must declare the basis consistently.

At the actual simulated D concentrations, BOD entering the lake is **136 × 10 = 1,360 kg/day**. The **1,400 kg/day** design value intentionally uses C's larger concentration. Node C flow is unavailable, so an exact incremental B–C pollution mass load cannot be calculated.

### 4.5 Area-slider sensitivity

The table varies area while holding flow, influent, background values, and calibrated coefficients constant. Outlet concentrations are rounded for display.

| Total area (m²) | Area/MLD (m²/MLD) | Hydraulic loading (m/day) | Turbidity out (NTU) | BOD out (mg/L) | Nitrate out (mg/L) | Phosphate out (mg/L) |
|---:|---:|---:|---:|---:|---:|---:|
| 5,000 | 500 | 2.00 | 121.2 | 104.0 | 31.2 | 10.7 |
| 10,000 | 1,000 | 1.00 | 82.1 | 77.6 | 25.7 | 9.2 |
| 15,000 | 1,500 | 0.67 | 56.2 | 58.2 | 21.2 | 7.9 |
| **20,000** | **2,000** | **0.50** | **39.0** | **44.0** | **17.5** | **6.8** |
| 25,000 | 2,500 | 0.40 | 27.6 | 33.6 | 14.5 | 5.9 |

Larger area improves modeled removal with diminishing gains as outputs approach C*. If flow doubles without increasing area, A/Q halves and the predicted concentrations equal the **10,000 m² / 10 MLD** row. The simulator therefore needs both area and flow sensitivity.

### 4.6 Brief cost comparison with conventional mechanical STPs

The following values are **illustrative budgeting assumptions**, not vendor quotations or sourced local estimates. They compare a 10 MLD case at the same nominal daily flow; they do not establish equivalent effluent quality. Both exclude land acquisition, major sewer interception, contaminated-sediment remediation, financing, and site-specific approvals.

| Cost or operating factor | CW + FTW reference concept | Conventional mechanical STP | Interpretation |
|---|---|---|---|
| Illustrative capital basis | ₹3,000–₹8,000 per m² × 20,000 m² | ₹1.5–₹3.0 crore per MLD × 10 MLD | Actual quotes and treatment scope are required. |
| Illustrative capital total | **₹6–₹16 crore** | **₹15–₹30 crore** | Wetland land and hydraulic works can erase apparent savings. |
| Illustrative operating basis | **₹2–₹6 per m³** | **₹8–₹20 per m³** | Wetland costs include maintenance assumptions; STP costs depend on process and energy. |
| Illustrative annual O&M at continuous 10 MLD | **₹0.73–₹2.19 crore/year** | **₹2.92–₹7.30 crore/year** | Calculated using 3.65 million m³/year; rates are assumptions. |
| Energy and staffing | Potentially lower where gravity flow works; pumps and maintenance may still be needed | Aeration, pumping, process control, and sludge handling | Passive treatment has an energy opportunity, not zero operating cost. |
| Land and reliability | Large footprint; sensitive to loading, hydraulics, and maintenance | Typically smaller footprint with greater process control | Compare lifecycle cost at the same verified discharge objective. |
| Effluent capability | **44 mg/L modeled BOD** in this reference case; no pathogen or toxicity guarantee | Process-dependent; can be engineered for stricter objectives | LakeGuard complements interception and STPs; this model does not prove regulatory compliance. |

Detailed costing must cover screening, forebay construction, media, FTW modules, flow distribution, pumps where needed, harvesting, sludge disposal, monitoring, and replacement. Treatment of identified industrial toxicity may require source-specific pretreatment beyond wetlands.

### 4.7 Verification, feasibility, and success criteria

| Check | Judge-review criterion | Deployment evidence needed |
|---|---|---|
| Satellite validity | Correct index formulas, resolution handling, cloud masks, and scene timestamps | Dated scenes and paired water samples; no “live” label on old imagery. |
| Tracing correctness | Scenario identifies **B–C**, while not falsely labeling A–B | Travel-time-aligned observations, tributary mapping, and sensor-quality records. |
| Treatment reproducibility | 20,000 m² and 10 MLD reproduce the stated concentration endpoints | Independent pilot validation of coefficients and uncertainty. |
| Dimensional accuracy | Correct MLD conversion, exponent units, removal arithmetic, and load units | Calibrated flow instruments and consistent laboratory reporting. |
| Land and hydraulic viability | Show loading and residence-time assumptions | Surveyed footprint, flood levels, tracer testing, and inlet interception design. |
| Pollution reduction | Distinguish predicted concentration change from verified load reduction | Flow-weighted influent/effluent monitoring, bypass accounting, and maintenance logs. |
| Wider safety and ecology | Avoid interpreting NTU/BOD alone as safe water | Pathogens, dissolved oxygen, nutrients, relevant toxicants, and ecological assessment. |

**Deployment sequence:** Confirm drainage geometry and land ownership; establish baseline sampling; validate satellite proxies; deploy a limited monitoring reach; inspect suspected sources; pilot the treatment train; then refine footprint and coefficients before full-scale construction. Agency-led source correction and inlet treatment should proceed as coordinated workstreams.

---

## SECTION 5: STAKEHOLDERS & VALUE PROPOSITION MATRIX

### 5.1 Stakeholder-to-action mapping

| Stakeholder | Core problem | Actionable LakeGuard output | Action enabled | Value and success measure |
|---|---|---|---|---|
| **KSPCB — Karnataka State Pollution Control Board** | Sewage or industrial pollution is evident in the lake but difficult to localize upstream. | Highlighted **500 m B–C reach**, timestamps, anomaly magnitude, sampling locations, and an evidence packet. | Target inspection, identify the actual discharge point, and pursue enforcement or fines after verification. | Shorter investigation reach; confirmed incidents resolved; fewer recurrent spikes. |
| **BWSSB — Bangalore Water Supply and Sewerage Board** | Broken or misconnected sewers can leak into the **K100 rajakaluve**, adding biological load to drains and treatment infrastructure. | Suspected sewer-defect reach, inspection referrals, flow/concentration history, and before/after repair tracking. | Locate and repair verified faults; improve interception; coordinate treatment routing. | Lower untreated load in drains. Inlet treatment may reduce downstream biological load; any reduction in mechanical STP load depends on actual routing. |
| **BBMP — Lake Division & Stormwater Drain Department** | Lake investments may lack current evidence on which inlet hotspot needs intervention and how much area is required. | Sentinel-2 plume-priority maps, surveyed hotspot polygons, area/MLD estimates, and hydraulic constraints. | Place FTWs and associated inlet treatment at the verified **Northwest hotspot**; plan access, civil works, and maintenance. | Better-targeted spending; documented treatment location, capacity, and maintained performance. |
| **Citizen Lake Protection Groups / Local Residents — Bellandur Ward Committees** | Limited transparency on pollution sources and responses; persistent frothing, odor, and ecological degradation. | Publicly understandable dated maps, simulated-versus-measured labels, confirmed incident status, and treatment trends. | Follow agency action, report observations, and participate in restoration monitoring. | Transparent accountability and, after verified remediation, reduced odor/frothing and improved ecology. These outcomes need indicators beyond BOD alone. |
| **Downstream Farmers — Anekal / Kolar belt, as identified in the brief** | Polluted downstream water can impair irrigation usability and create crop, soil, and exposure concerns. | Downstream BOD/turbidity trends, treatment-status information, and irrigation-quality sampling results. | Evaluate water suitability with agricultural guidance and request corrective action when quality worsens. | Potentially cleaner, lower-BOD and lower-turbidity water where hydraulic connectivity is confirmed; salinity, pathogens, and metals must also be assessed. |
| **Wetland operators and maintenance teams** | Treatment declines when screens clog, biomass accumulates, media saturate, or flow bypasses cells. | Maintenance schedule, hydraulic-loading indicators, inlet/outlet trends, and harvest/solids records. | Remove solids, restore flow distribution, harvest plants, and replace media or modules when required. | Sustained removal, reduced downtime, and auditable operating cost. |
| **Accredited laboratories and academic partners** | Proxy readings and fitted coefficients need independent verification. | Georeferenced sampling plan, matched inlet/outlet data, declared analyte units, and model assumptions. | Validate BOD and nutrient measurements; calibrate satellite proxies and treatment rates. | Defensible uncertainty estimates and validated engineering parameters. |
| **Municipal planners and funding bodies** | Capital proposals lack a traceable link between pollution priority, footprint, cost, and expected benefit. | Prioritized inlet dossier, scenario comparisons, feasibility gaps, and lifecycle-cost assumptions. | Fund surveys and pilots, assess land feasibility, and compare treatment alternatives. | Investment decisions supported by measurable load-reduction evidence. |
| **Upstream premises and utilities** | A broad pollution allegation may not distinguish an illegal connection, a sewer defect, or another cause. | Verified incident location, inspection findings, and corrective-action requirements through the responsible agency. | Repair connections, provide pretreatment, and demonstrate compliance. | Fairer attribution and documented source-load reduction. |

The named downstream belts are stakeholder categories from the supplied brief; the report does not establish a direct natural drainage connection to every locality. Recipient-specific benefits require confirmation of surface-water or conveyance routes.

### 5.2 Accountability and information design

The public view should show dated inlet conditions and confirmed incident progress. Authorized agency views may contain sensitive source details, exact asset locations, raw observations, and evidence records. All views must clearly identify **satellite proxy**, **simulation**, **measured value**, or **model prediction**.

A closed-loop case should record: detected anomaly, assigned inspection, laboratory confirmation, source correction, inlet-treatment operation, and post-action verification. A resolved case requires evidence of improvement; a disappeared map plume alone is insufficient.

### 5.3 Value proposition and practical impact

LakeGuard gives each actor a concrete decision: **where to inspect, which reach to investigate, where to treat, how much area to provision, and what evidence to collect afterward**. At the reference scenario, it localizes the strongest concentration jump to B–C and provides a reproducible 20,000 m² / 10 MLD treatment calculation.

The projected benefits are lower pollutant loading at the inlet, better-directed municipal spending, faster source investigation, and more transparent restoration progress. Full lake recovery also depends on other inlets, sewer interception, sediments, hydrology, maintenance, and toxicant control; the Northwest intervention is a targeted component of that wider program.

### 5.4 Supporting technical basis and provenance

| Reference or input | Role in this report | Scope of support |
|---|---|---|
| **User-supplied Track 02 / C4 brief** | Lake area, named inlet, required storyline, virtual node readings, nominal targets, plants, and stakeholder list | Scenario specification; not independent evidence of current conditions or official rubric verification. |
| **ESA / Copernicus Sentinel-2 mission documentation** — [ESA Sentinel-2](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2), [Copernicus SentiWiki](https://sentiwiki.copernicus.eu/web/s2-mission) | Mission context and MSI band-resolution conventions | Supports sensor capabilities; no Bellandur image was verified for this report. |
| **CPCB, Water Quality Criteria** — [Designated-best-use criteria](https://cpcb.nic.in/water-quality-criteria/) | Meaning of the Class E category | Does not independently establish Bellandur's current classification. |
| **Mishra, S. and Mishra, D. R. (2012), “Normalized difference chlorophyll index: A novel model for remote estimation of chlorophyll-a concentration in turbid productive waters,” Remote Sensing of Environment, 117, 394–406** | NDCI methodological basis | Local calibration remains necessary for quantitative use. |
| **Kadlec, R. H. and Wallace, S. D. (2009), Treatment Wetlands, second edition, CRC Press** | First-order areal wetland modeling and engineering framework | Does not validate the reverse-fitted coefficients used here. |
| **U.S. EPA, Constructed Wetlands Treatment of Municipal Wastewaters (2000), EPA/625/R-99/010** | Treatment processes, design considerations, and operational limitations | General design basis; no Bellandur-specific performance or cost claim. |
| **Report calculations** | Removal percentages, rate coefficients, sensitivity values, hydraulic loading, pollutant loads, and cost arithmetic | Derived from explicitly stated scenario assumptions; no field-performance claim. |

**Submission outcome:** A technically explicit, reproducible design report connecting satellite-guided inlet prioritization, a 500 m upstream investigation reach, and a quantified hybrid-wetland scenario for Bellandur's challenge-designated Northwest inlet.

