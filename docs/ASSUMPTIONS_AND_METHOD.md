# Method and assumptions

## What is calculated

This is a deterministic annual accounting model. It does not solve an objective function or choose an optimum. Each of the 24 combinations is prescribed: two ecological-footprint cases, four thermal cases, and three nuclear cases across ten utility regions.

For region `j` and scenario `s`, the intended equations are:

```text
BC_j = forest_j + cropland_j + grazing_j + built-up_j
Ccap_j = Ccap_Japan * BC_j / sum(BC)
e_js = sum_k(w_jks * e_k)
T_js = 1000 * Ccap_j / e_js                         [TWh]
N_js = sum_u(K_u * 8760 * 0.70) / 1,000,000         [TWh]
Rgross_js = D_j - T_js - N_js
Rexisting_j = sum_p(K_jp * 8760 * cf_p) / 1,000,000 [TWh]
A_js = Rgross_js - Rexisting_j
Abuild_js = max(0, A_js)
```

`Ccap` is in Mt CO2, `e` in gCO2/kWh, `K` in MW for nuclear and kW for renewable capacity, and the factor 1000 performs the Mt/g and TWh/kWh conversion. Fuel weights are normalized within fossil generation.

## Scenario cases

| Dimension | Cases |
|---|---|
| EF allowance | `carbon_only` (Cases 1–12), `carbon_and_food` (Cases 13–24) |
| Thermal generation | 2016 regional fuel mix; 2030 26% coal / 27% LNG / 3% oil mix; LNG-only; zero thermal |
| Nuclear generation | currently operating; all candidate units; zero nuclear |

The scenario order is recorded in [`config/scenario_definitions.csv`](../config/scenario_definitions.csv). Case 6 is carbon-only / 2030 mix / zero nuclear. Case 20 is carbon-and-food / LNG-only / all candidate units.

## Numerical assumptions

| Item | Value |
|---|---:|
| Coal operational factor | 863.8 gCO2/kWh |
| LNG operational factor | 375.7 gCO2/kWh |
| Oil operational factor | 695.1 gCO2/kWh |
| Hours per year | 8,760 |
| Nuclear capacity factor | 70% |
| Conventional hydro / wind | 45% / 20% |
| Solar below 10 kW / at least 10 kW | 12% / 14% |
| Geothermal | 83% |
| Pumped hydro in alternate capacity audit | 6% |

The canonical final workbook supplies the already aggregated existing-plus-FIT renewable annual credits by region. The alternate workbook holds a capacity-based version and is retained only as an alternate audit, because its national emissions and caps differ materially.

## Supply balance interpretation

`Rgross` closes only an annual energy equation. A positive `A` is a positive annual renewable requirement after the assumed installed/FIT credit. A negative `A` is an annual arithmetic surplus. It does not demonstrate feasible export, transmission, storage, BESS operation, reserve adequacy, or hourly balance. No BESS appears in the model or is assumed in the results.

## Published-cap treatment

The visible final-workbook BC table reconstructs the published CO2 allowance rule for eight regions, but its Tokyo and Chubu entries yield offsetting allocation deviations of 0.766235 Mt in the carbon-only case (1.680529 Mt in the carbon-and-food case). The canonical final regional allowance values are therefore held as immutable inputs for historical reproduction, while `regional_CO2_baseline_and_caps.csv` publishes the formula audit. This is a source inconsistency, not a calibration choice.
