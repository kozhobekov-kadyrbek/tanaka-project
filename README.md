# Tanaka Project

Reproducible reconstruction of Hiroaki Tanaka's annual ecological-footprint and renewable-electricity scenario study for Japan.

## Scope

This repository reproduces Tanaka's deterministic 2016 annual accounting model for ten Japanese utility regions. It implements 24 prescribed scenarios:

\[
2\ \text{ecological-footprint cases}
\times 4\ \text{thermal cases}
\times 3\ \text{nuclear cases}
=24
\]

It is not an hourly dispatch, BESS, unit-commitment, power-flow, transmission-loss, GIS-siting, cost-minimisation, or lifecycle-assessment model.

## Core equations

\[
C^{cap}_{j}=C^{cap}_{Japan}\frac{BC_j}{\sum_mBC_m}
\]

\[
T_{j,s}=\frac{C^{cap}_{j}}{\sum_k w_{jks}e_k}
\]

\[
N_{j,s}=\sum_{u\in s}K_u\times8760\times0.70
\]

\[
R^{gross}_{j,s}=D_j-T_{j,s}-N_{j,s}
\]

\[
R^{existing+FIT}_j=\sum_pK_{jp}\times8760\times cf_p
\]

\[
A_{j,s}=R^{gross}_{j,s}-R^{existing+FIT}_j,
\qquad
A^{build}_{j,s}=\max(0,A_{j,s})
\]

## Canonical reproduction basis

The final Chapter 4 workbook and thesis narrative are the canonical reported-result version. A separate main-data workbook contains materially different values and is preserved as an alternate version. The project must never mix these two source versions.

## Key reported benchmarks

- 2016 annual electricity quantity: **655.61 TWh**
- Final-workbook baseline generation emissions: **413.416 Mt-CO2/year**
- Carbon-only cap: **64.148 Mt-CO2/year**
- Carbon-plus-food cap: **140.692 Mt-CO2/year**
- Case 6 positive additional RE requirement: **388.40 TWh/year**
- Case 20 positive additional RE requirement: **148.90 TWh/year**
- Thermal-retired cases: **429.81**, **313.47**, and **485.80 TWh/year** for current nuclear, all-candidate nuclear, and nuclear-retired assumptions respectively.

## Important limits

Tanaka's results are annual energy-accounting residuals. A negative residual does not demonstrate physically exportable electricity. The model does not calculate hourly adequacy, renewable curtailment, storage, transmission capacity, power flow, or transmission losses.

## Repository policy

Only original code, derived tables, reproducible configuration files, source metadata, citations, and documentation may be published. Do not upload the original thesis, restricted Excel workbooks, proprietary databases, or third-party data without permission.

See [CODEX_TANAKA_REPRODUCTION_DIRECTIVE.md](CODEX_TANAKA_REPRODUCTION_DIRECTIVE.md) for the build specification.

## Run and inspect

```powershell
python src/python/verify_results.py
matlab -batch "addpath('src/matlab'); results=runtests('tests'); assertSuccess(results);"
```

The executable method, inputs, source boundaries, and discrepancies are documented in [docs/REPRODUCTION.md](docs/REPRODUCTION.md), [docs/ASSUMPTIONS_AND_METHOD.md](docs/ASSUMPTIONS_AND_METHOD.md), and [docs/DISCREPANCIES.md](docs/DISCREPANCIES.md).
