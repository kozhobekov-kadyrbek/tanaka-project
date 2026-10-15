# Codex build directive: Tanaka Project

## Goal

Build a reproducible MATLAB project for Hiroaki Tanaka's annual ecological-footprint and renewable-electricity scenario calculation. Reproduce the original 24 prescribed cases before adding any extension.

This project is an **annual deterministic accounting reproduction**. Do not present it as an optimisation, hourly power-system model, BESS model, unit-commitment model, power-flow model, or transmission-loss model.

## Source hierarchy

1. Use the final Chapter 4 results workbook and thesis narrative as the canonical reported-result version.
2. Preserve `本論データ.xlsx` as an alternate calculation version.
3. Never combine input values from those two versions in one reproduction run.
4. Retain raw source files locally; publish only permitted derived tables, code, hashes, citations, and documentation.

## Required repository structure

```text
config/
data/derived/canonical_final_workbook/
data/derived/alternate_main_workbook/
docs/
results/figures/
src/matlab/
src/python/
tests/
```

## Model to implement

Regions:
Hokkaido, Tohoku, Tokyo, Hokuriku, Chubu, Kansai, Chugoku, Shikoku, Kyushu, Okinawa.

Scenarios:
- ecological-footprint cases: carbon-only; carbon-plus-food;
- thermal cases: 2016 mix; 2030 mix; LNG-only; thermal retired;
- nuclear cases: currently operating; all candidate units; nuclear retired.

Implement:

\[
C_j^{cap}=C_{Japan}^{cap}\frac{BC_j}{\sum_mBC_m}
\]

\[
T_{js}=\frac{C_j^{cap}}{\sum_kw_{jks}e_k}
\]

\[
N_{js}=\sum_{u\in s}K_u\times8760\times0.70
\]

\[
R_{js}^{gross}=D_j-T_{js}-N_{js}
\]

\[
R_{jp}=K_{jp}\times8760\times cf_p
\]

\[
A_{js}=R_{js}^{gross}-R_j^{existing+FIT},
\qquad A_{js}^{build}=\max(0,A_{js})
\]

Use the original assumptions:
- coal 863.8 g-CO2/kWh;
- LNG 375.7 g-CO2/kWh;
- oil 695.1 g-CO2/kWh;
- conventional hydro CF 45%;
- wind CF 20%;
- solar below 10 kW CF 12%;
- solar at least 10 kW CF 14%;
- geothermal CF 83%;
- nuclear CF 70%;
- 8760 h/year.

## Required files

Create:
- `config/scenario_definitions.csv`
- `config/fossil_emission_factors.csv`
- `config/renewable_capacity_factors.csv`
- `config/nuclear_scenarios.csv`
- `config/EF_and_biocapacity_assumptions.csv`
- `config/regional_demand_and_existing_RE.csv`
- `src/matlab/run_tanaka_reproduction.m`
- `src/matlab/calculate_biocapacity.m`
- `src/matlab/calculate_EF_CO2_caps.m`
- `src/matlab/calculate_thermal_generation.m`
- `src/matlab/calculate_nuclear_generation.m`
- `src/matlab/calculate_RE_residual.m`
- `src/python/verify_results.py`
- `tests/test_24_case_reproduction.m`
- `results/all_24_scenarios_by_region.csv`
- `results/regional_CO2_baseline_and_caps.csv`
- `results/regional_demand_and_assumed_RE.csv`
- `results/identified_case4_cell_corrections.csv`
- `results/reproduction_summary.csv`
- `DATA_MANIFEST.csv`

## Verification

Test all 240 region-case rows and the annual-energy identity:

\[
D_j=T_{js}+N_{js}+R_{js}^{gross}
\]

Check cap allocation, fuel-share normalisation, nuclear calculation, capacity-to-energy conversion, and agreement with canonical reported values within a stated tolerance.

Report both:
1. `as_reported`: historical final-workbook values;
2. `diagnostic_corrected`: values recomputed from Tanaka's own equation.

Do not overwrite historical values. Document the known case-4 Hokuriku and Chubu inconsistency and the final-versus-main-workbook discrepancy.

## Publication and completion

Do not upload original thesis PDFs, source Excel workbooks, or restricted third-party data. Publish only permitted code and derived results. Add source URL, date, licence/access condition, raw-file SHA-256, transformation, and output path to `DATA_MANIFEST.csv`.

Run tests locally, commit the completed project to `main`, and finish with the commit SHA, test result, exact published files, reproduced benchmark values, and all excluded restricted files.
