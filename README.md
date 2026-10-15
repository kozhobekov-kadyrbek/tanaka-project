# Tanaka Project

Reproducible reconstruction of Hiroaki Tanaka's 24-case renewable-electricity study for ten Japanese utility regions.

## Scope

This is a **deterministic annual energy-accounting reproduction**. It applies prescribed annual assumptions and calculates residual renewable generation. It is not an optimisation model and does not solve a cost, capacity, or dispatch objective. It does not model hourly dispatch, BESS, storage, unit commitment, transmission flow or losses, GIS siting, lifecycle assessment, or physical exports.

A negative annual RE residual is an arithmetic surplus under the stated annual assumptions. It does **not** represent transferable electricity, physical export, or a demonstrated transmission outcome.

## Annual equations and source treatment

The visible biocapacity table is audited using:

\[
C_{j}^{formula}=C_{Japan}\frac{BC_j}{\sum_m BC_m}
\]

The executable canonical reproduction uses the **published final-workbook regional cap** \(C_j^{canonical}\), not the formula-audit value. Thermal, nuclear, and annual residual equations are:

\[
T_{js}=\frac{1000C_j^{canonical}}{\sum_k w_{jks}e_k},\quad
N_{js}=\frac{K_{js}\times8760\times0.70}{10^6},\quad
R^{gross}_{js}=D_j-T_{js}-N_{js}
\]

\[
A_{js}=R^{gross}_{js}-\bar R_j^{existing+FIT},\qquad A_{js}^{build}=\max(0,A_{js})
\]

\(\bar R_j^{existing+FIT}\) is a **workbook-derived annual credit read directly from configuration**. The canonical model does not recalculate it from technology-level renewable capacities. Capacity factors in `config/renewable_capacity_factors.csv` are historical context only.

## Run

Run the complete Python reproduction and QA from the repository root:

```powershell
python src/python/verify_results.py
```

Run the Python test suite:

```powershell
python -m unittest discover -s tests -p "test_python_reproduction.py"
```

Run the MATLAB test suite:

```powershell
matlab -batch "addpath('src/matlab'); results=runtests('tests'); assertSuccess(results);"
```

## Outputs

| File | Meaning |
|---|---|
| `data/derived/canonical_final_workbook/as_reported_240.csv` | Historical final-workbook-derived values. Never overwritten by the reproduction. |
| `results/all_24_scenarios_by_region.csv` | Diagnostic equation-based reconstruction for all 240 rows, alongside historical values. |
| `results/source_cell_audit.csv` | Eight source-cell differences, their evidence status, and classification. |
| `results/QA_SUMMARY.csv` | Check status, tolerance, and explanation. |
| `results/regional_CO2_baseline_and_caps.csv` | Formula audit and canonical regional cap inputs. |
| `results/reproduction_summary.csv` and `results/matlab_annual_accounting_results.csv` | Case totals and the independent MATLAB cross-check. |
| `results/figures/*.png` | Derived charts of annual positive additional RE requirements. |

The two Case 4 Hokuriku/Chubu differences are confirmed by scenario equivalence. The six Cases 13–15 differences are classified `unresolved_source_or_formula_inconsistency`: their source cells are known, but the restricted original Excel formulas and complete inputs were not traced. See [docs/DISCREPANCIES.md](docs/DISCREPANCIES.md).

## Limitations

The final workbook's regional caps are canonical inputs. Tokyo and Chubu do not exactly reconstruct from the visible biocapacity table, so the formula is an audit rather than an independent cap reconstruction. The public project cannot reproduce raw Excel formulas, underlying technology-level renewable capacities, or other restricted source information. See [docs/REPRODUCTION_STATUS.md](docs/REPRODUCTION_STATUS.md).

Only original code, derived results, metadata, and documentation are published. Original thesis, DOCX, XLSX, and other restricted sources are excluded.
