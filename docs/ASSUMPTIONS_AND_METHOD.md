# Method, assumptions, and data provenance

## Model class

This project is a deterministic annual energy-accounting reproduction. It has no objective function and does not optimise technology, capacity, cost, dispatch, or emissions. The 24 cases are prescribed combinations of two ecological-footprint cases, four thermal cases, and three nuclear cases.

It has no hourly chronology, BESS, storage dispatch, unit commitment, power flow, transmission model, GIS, lifecycle assessment, or physical export calculation. A negative annual residual is not transferable electricity or physical export; it is only an annual arithmetic result.

## Equations

For region `j` and scenario `s`:

```text
BC_j = forest_j + cropland_j + grazing_j + built-up_j
Cformula_j = CJapan * BC_j / sum(BC)                 # audit only
e_js = sum_k(w_jks * e_k)
T_js = 1000 * Ccanonical_j / e_js                    # TWh
N_js = K_equivalent_js * 8760 * 0.70 / 1,000,000     # TWh
Rgross_js = D_j - T_js - N_js
A_js = Rgross_js - Rcredit_existing+FIT_j
Abuild_js = max(0, A_js)
```

`Ccanonical_j` is the final-workbook regional CO2 cap. `Cformula_j` is retained only to audit the stated biocapacity allocation rule. Fuel shares are normalised within fossil generation. The nuclear capacity is an equivalent MW value that verifies the annual scenario input; it is not claimed to be a recovered unit-level capacity dataset.

## Scenarios and numerical assumptions

| Dimension | Cases |
|---|---|
| EF allowance | `carbon_only` (1–12); `carbon_and_food` (13–24) |
| Thermal | 2016 regional mix; 2030 26% coal / 27% LNG / 3% oil; LNG-only; zero thermal |
| Nuclear | currently operating; all candidate units; zero nuclear |

| Assumption | Value | Role |
|---|---:|---|
| Coal / LNG / oil operational factor | 863.8 / 375.7 / 695.1 gCO2/kWh | Executable thermal calculation |
| Hours per year | 8,760 | Executable nuclear conversion |
| Nuclear capacity factor | 70% | Executable nuclear conversion |
| Hydro / wind / solar <10kW / solar >=10kW / geothermal | 45% / 20% / 12% / 14% / 83% | Historical context only; not used to reconstruct canonical RE credit |
| Pumped hydro | 6% | Alternate-workbook context only |

## Data provenance

| Variable | Unit | Source | Treatment | Limitation |
|---|---|---|---|---|
| Regional demand `D_j` | TWh/year | Final Chapter 4 workbook-derived configuration | Direct executable input | Annual quantity only |
| Existing + FIT RE credit `Rcredit_existing+FIT_j` | TWh/year | Final Chapter 4 workbook-derived configuration | Direct executable input | Not recalculated from technology capacities; asset detail unavailable publicly |
| Regional CO2 cap `Ccanonical_j` | MtCO2/year | Final Chapter 4 workbook-derived configuration | Direct executable input | Cap formula does not exactly reconstruct Tokyo/Chubu from visible BC table |
| Biocapacity land classes | gha | Final-workbook-derived configuration | Calculated into formula-audit BC total | Does not independently establish original regional cap inputs |
| Fossil factors and fuel shares | gCO2/kWh; share | Thesis/final-workbook-derived configuration | Calculated | Operational CO2 only |
| Nuclear annual scenario output | TWh/year | Canonical final-workbook-derived scenario input | Direct input, checked against equivalent MW conversion | Equivalent MW is not an original unit-capacity dataset |
| Historical reported results | TWh/year | Restricted final workbook, extracted as permitted numerical derivative | Immutable comparison input | Original formula trace is not public |
| Alternate benchmark data | TWh/year; MtCO2/year | Alternate main-data workbook | Output-only context | Never read by the canonical executable model |

## CO2-cap audit

The code calculates `Cformula_j` from the visible BC values and compares it with the final-workbook regional caps. Eight regions reconstruct within tolerance. Tokyo and Chubu have offsetting differences of 0.766235 Mt in the carbon-only case and 1.680529 Mt in the carbon-and-food case. The project therefore does not claim an independent reconstruction of every original cap; it uses the published final-workbook cap as the canonical input and reports the audit in `results/regional_CO2_baseline_and_caps.csv`.
