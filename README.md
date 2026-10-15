# Tanaka Project

Reproducible reconstruction and evidence audit of Hiroaki Tanaka's 24-case renewable-electricity study for ten Japanese utility regions.

## Scope

This is a **deterministic annual energy-accounting reproduction**. It applies prescribed annual assumptions and calculates thermal energy, nuclear energy, a gross renewable residual, and a positive additional renewable shortfall. It is not an optimization model and has no objective function or decision variables.

It does not model hourly dispatch, RE100 corporate procurement, BESS, other storage, unit commitment, transmission flow or losses, GIS siting, life-cycle assessment, or physical exports. A negative annual residual is arithmetic only and does not represent transferable electricity.

## Complete analysis

1. [Background, problem, objective, contribution, and comparison](docs/01_BACKGROUND.md)
2. [Case studies and all 24 scenario assumptions](docs/02_CASE_STUDIES.md)
3. [Methodology, variables, and complete formulations](docs/03_METHODOLOGY_AND_FORMULATIONS.md)
4. [Simulation conditions and all public data](docs/04_SIMULATION_CONDITIONS_AND_DATA.md)
5. [Results, comparisons, discrepancies, and figures](docs/05_RESULTS.md)
6. [Conclusion, limitations, gaps, and weaknesses](docs/06_CONCLUSION_LIMITATIONS.md)
7. [Overall summary and reproduction guide](docs/07_OVERALL_SUMMARY.md)

The safe source inventory is [SOURCE_FOLDER_PUBLIC_INVENTORY.md](docs/SOURCE_FOLDER_PUBLIC_INVENTORY.md).

## Model equations

The visible biocapacity table is audited with:

\[
C_j^{formula}=C_{Japan}^{cap}\frac{BC_j}{\sum_m BC_m}
\]

The executable reproduction uses the **final-workbook-derived canonical regional cap** because Tokyo and Chubu do not exactly reconstruct from the visible BC table:

\[
T_{js}=\frac{1000C_j^{canonical}}{\sum_k w_{jks}e_k},\qquad
N_{js}=\frac{K_{js}\times8760\times0.70}{10^6}
\]

\[
R_{js}^{gross}=D_j-T_{js}-N_{js}
\]

\[
A_{js}=R_{js}^{gross}-\bar R_j^{existing+FIT},\qquad
A_{js}^{build}=\max(0,A_{js})
\]

The canonical `existing_plus_fit_re_twh` credit is read directly as a workbook-derived annual input. It is not recalculated from technology capacities. Renewable capacity factors are retained as historical context only.

## Reproduced headline results

- 24 scenarios × 10 regions = **240 rows**;
- canonical generation CO2 baseline: **413.415620 Mt/year**;
- carbon-only cap: **64.148259 Mt/year**;
- carbon-plus-food cap: **140.691812 Mt/year**;
- Case 6 positive regional shortfall sum: **388.402687 TWh/year**;
- Case 20 positive regional shortfall sum: **148.896509 TWh/year**;
- 232 historical rows agree within rounding;
- 2 Case 4 rows are confirmed inconsistent by scenario equivalence;
- 6 Cases 13–15 rows remain `unresolved_source_or_formula_inconsistency`.

## One-command Python reproduction

```powershell
python src/python/generate_publication_outputs.py
```

This regenerates all canonical Python results, QA tables, extended documentation datasets, and 12 original figures in both PNG and SVG. It reads no restricted source files and leaves [as_reported_240.csv](data/derived/canonical_final_workbook/as_reported_240.csv) unchanged.

Install dependencies with:

```powershell
python -m pip install -r requirements.txt
```

## Tests

```powershell
python -m unittest discover -s tests -p "test_python_reproduction.py"
matlab -batch "addpath('src/matlab'); results=runtests('tests'); assertSuccess(results);"
```

## Result versions

| Version | File | Interpretation |
|---|---|---|
| Historical as reported | `data/derived/canonical_final_workbook/as_reported_240.csv` | Immutable final-workbook-derived values. |
| Diagnostic reconstruction | `results/all_24_scenarios_by_region.csv` | Equation-based recalculation from canonical public configuration. |
| Discrepancy evidence | `results/source_cell_audit.csv` | Exact source cells, values, differences, classifications, and explanations. |

The alternate main-data workbook is isolated under `data/derived/alternate_main_workbook/` and is never mixed into the canonical run.

## Main outputs

| Output | Contents |
|---|---|
| `results/scenario_assumptions_24.csv` | Exact EF, thermal, and nuclear mapping for every case. |
| `results/all_24_scenarios_by_region.csv` | Complete 240-row diagnostic and historical comparison. |
| `results/reproduction_summary.csv` | National totals for all 24 cases. |
| `results/regional_demand_existing_RE_inputs.csv` | Ten-region demand and direct annual renewable credits. |
| `results/regional_biocapacity_components.csv` | Four visible BC components and totals. |
| `results/ecological_footprint_inputs_and_targets.csv` | 2016 and two one-Earth EF pathways. |
| `results/ecological_footprint_results_by_case.csv` | Regional baseline, cap, and implied change for both EF cases. |
| `results/CO2_cap_allocation_audit.csv` | Formula cap, canonical cap, and Tokyo/Chubu deviations. |
| `results/fossil_emission_factors_and_fuel_shares.csv` | Fuel factors and normalized thermal shares. |
| `results/nuclear_assumptions_by_region.csv` | All 30 nuclear region-case inputs. |
| `results/renewable_capacity_factors.csv` | Historical capacity-factor context with canonical-use flags. |
| `results/source_data_provenance.csv` | Variable-level source, treatment, and limitation. |
| `results/source_figure_audit.csv` | Evidence status for all 32 charts in the named PPTX/XLSX sources. |
| `results/figure_catalog.csv` | Twelve figures, each available as PNG and SVG. |
| `results/QA_SUMMARY.csv` | Core numerical, publication, and restricted-source checks. |

## Limitations

The model does not establish hourly feasibility, reliability, storage needs, transmission feasibility, least cost, resource potential, land availability, or economy-wide one-Earth compliance. The final workbook's regional caps and annual existing/FIT credits remain restricted-workbook-derived numerical inputs. Exact historical Excel dependencies for six Cases 13–15 cells are unavailable.

## Source and publication policy

Original thesis, DOCX, PPTX, XLSX, PDF, images, and third-party raw datasets are excluded. This repository publishes original code, derived numerical results, source fingerprints and metadata, QA evidence, documentation, and original redraws only. See [REPRODUCTION_STATUS.md](docs/REPRODUCTION_STATUS.md) and [DATA_MANIFEST.csv](DATA_MANIFEST.csv).
