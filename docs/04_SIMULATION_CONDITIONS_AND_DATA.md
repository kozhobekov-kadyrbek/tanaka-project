# 4. Simulation conditions, assumptions, and data

## Core conditions

| Item | Condition |
|---|---|
| Temporal resolution | One annual period; 8760 hours appears only in capacity-to-energy conversion. |
| Main data year | 2016 for national EF and regional electricity quantities. |
| Other dated assumptions | 2030 fuel mix comes from a historical outlook; nuclear operating status is described as April 2019. |
| Regions | Ten Japanese utility service regions. |
| Energy balance | Each region is balanced independently on annual energy. |
| Emissions | Direct fossil combustion CO2 only. |
| Nuclear and renewable operational CO2 | Treated as zero in the annual generation balance. |
| Demand | Fixed annual regional electricity quantity; no electrification or efficiency response. |
| Existing/FIT renewable output | Fixed annual workbook-derived credit. FIT approval is treated as available annual output in the historical study. |
| Storage and network | None. No BESS, interregional flow, losses, congestion, frequency converters, or curtailment. |
| Uncertainty | None. Every input and case is deterministic. |

The source note accompanying the alternate main-data workbook states that all calculations use 2016 data and that orange cells are year-dependent inputs. This explains update intent but does not reconcile the alternate workbook with the final Chapter 4 version.

## Regional canonical inputs

| Region | Demand (TWh) | Existing+FIT credit (TWh) | Baseline CO2 (Mt) | Carbon-only cap (Mt) | Carbon+food cap (Mt) |
|---|---:|---:|---:|---:|---:|
| Hokkaido | 23.195888 | 8.619280 | 15.595861 | 12.849896 | 28.182763 |
| Tohoku | 61.800850 | 30.390672 | 31.126295 | 13.799427 | 30.265301 |
| Tokyo | 200.378348 | 32.559860 | 190.276388 | 5.947593 | 13.044432 |
| Hokuriku | 27.760348 | 9.233047 | 18.548623 | 2.202325 | 4.830203 |
| Chubu | 118.889038 | 23.983531 | 55.738069 | 8.298299 | 18.200069 |
| Kansai | 94.977887 | 22.892627 | 39.187366 | 4.714472 | 10.339917 |
| Chugoku | 37.783495 | 11.583245 | 22.344563 | 5.494789 | 12.051329 |
| Shikoku | 20.215528 | 5.599591 | 9.768302 | 3.217802 | 7.057376 |
| Kyushu | 64.118867 | 24.445658 | 26.260842 | 7.270087 | 15.944964 |
| Okinawa | 6.492065 | 0.509885 | 4.569312 | 0.353569 | 0.775457 |
| **Total** | **655.612314** | **169.817396** | **413.415620** | **64.148259** | **140.691812** |

Machine-readable tables: [regional_demand_existing_RE_inputs.csv](../results/regional_demand_existing_RE_inputs.csv) and [CO2_cap_allocation_audit.csv](../results/CO2_cap_allocation_audit.csv).

## Biocapacity inputs

Visible regional BC contains forest, cropland, grazing, and built-up components. Historical 2016 factors in the supplied workbook are:

| Land class | Yield factor | Equivalence factor (gha/ha) |
|---|---:|---:|
| Forest | 1.37192 | 1.2792760703 |
| Cropland | 1.12143 | 2.5017671854 |
| Grazing | 2.15670 | 0.4592065351 |
| Built-up | 1.12143 | 2.5017671854 |

The ten-region components and totals are in [regional_biocapacity_components.csv](../results/regional_biocapacity_components.csv). Tohoku has the largest visible BC, about `12.990 million gha`; Okinawa has the smallest, about `0.333 million gha`.

## Ecological-footprint inputs and targets

The detailed land-category table is [ecological_footprint_inputs_and_targets.csv](../results/ecological_footprint_inputs_and_targets.csv). Key values are:

| Quantity | Value |
|---|---:|
| Japan 2016 EF | 4.492698 gha/person |
| World BC denominator | 1.629751 gha/person |
| Japan 2016 Earth equivalents | 2.756678 |
| Japan 2016 carbon EF | 3.388772 gha/person |
| Carbon-only carbon target | 0.525824 gha/person; 0.322641 Earths |
| Carbon+food carbon target | 1.153252 gha/person; 0.707625 Earths |

The source narrative sometimes expresses `0.71` as `gha/person`; the workbook shows that `0.71` is the Earth-equivalent contribution and `1.153` is the corresponding gha/person value.

## Fossil assumptions

| Fuel | Direct factor (g CO2/kWh) |
|---|---:|
| Coal | 863.8 |
| LNG combined cycle | 375.7 |
| Oil | 695.1 |

The 2016 shares are region-specific. The 2030 thermal mix normalizes the stated 26% coal, 27% LNG, and 3% oil within the 56% fossil subtotal. All raw and normalized values are in [fossil_emission_factors_and_fuel_shares.csv](../results/fossil_emission_factors_and_fuel_shares.csv).

## Nuclear assumptions

- capacity factor: `70%`;
- hours: `8760/year`;
- national current-operation annual output: `55.985160 TWh`;
- national all-candidate annual output: `176.411508 TWh`;
- zero-nuclear output: `0 TWh`.

All 30 regional case inputs and equivalent-capacity checks are in [nuclear_assumptions_by_region.csv](../results/nuclear_assumptions_by_region.csv).

## Renewable capacity factors

| Technology | Capacity factor |
|---|---:|
| Conventional hydro | 45% |
| Pumped hydro | 6% |
| Wind | 20% |
| Solar below 10 kW | 12% |
| Solar at least 10 kW | 14% |
| Geothermal | 83% |
| Nuclear | 70% |

Pumped hydro is alternate-workbook context. The renewable factors are historical context and are not used to recalculate the canonical annual existing/FIT credit. See [renewable_capacity_factors.csv](../results/renewable_capacity_factors.csv).

## Data provenance and version control

The full variable-level table is [source_data_provenance.csv](../results/source_data_provenance.csv). Three distinctions are mandatory:

1. **Canonical final-workbook inputs:** regional demand, annual renewable credit, regional caps, baseline emissions, nuclear scenario quantities, and historical 240 values.
2. **Calculated diagnostics:** normalized fuel weights, thermal energy, nuclear conversion checks, energy residuals, visible-BC cap audit, and positive shortfalls.
3. **Alternate-workbook context:** national baseline `308.715247 Mt` and caps `47.902268/105.060635 Mt`, plus technology-level historical context. These values are never used in the canonical run.

## Restricted-source boundary

Original PPTX, DOCX, XLSX, PDF, images, and third-party datasets remain local. The public repository contains source hashes, source roles, configuration values, derived results, chart audit metadata, code, and original redraws. See [SOURCE_FOLDER_PUBLIC_INVENTORY.md](SOURCE_FOLDER_PUBLIC_INVENTORY.md).
