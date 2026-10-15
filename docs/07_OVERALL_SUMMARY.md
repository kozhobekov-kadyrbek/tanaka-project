# 7. Overall work summary and reproduction guide

## What Tanaka calculates

Tanaka begins with two one-Earth EF scenarios, converts their retained carbon shares into national electricity-generation CO2 allowances, allocates the allowances to ten regions using BC, and enumerates four thermal and three nuclear cases. Renewable generation is the annual residual needed to close each regional energy balance. A workbook-derived existing-plus-FIT annual credit is then subtracted, and negative shortfalls are clipped to zero when reporting additional build need.

## Calculation sequence

1. Read the canonical annual regional demand, existing/FIT credit, baseline CO2, regional caps, nuclear case values, fuel shares, and historical 240 results.
2. Audit visible regional BC as the sum of forest, cropland, grazing, and built-up components.
3. Audit the stated national-cap allocation formula; retain final-workbook regional caps as canonical because Tokyo and Chubu deviate.
4. Normalize fossil fuel shares and compute the weighted direct emission factor.
5. Divide each canonical regional CO2 allowance by the weighted factor to obtain permitted thermal TWh.
6. read the canonical annual nuclear input and verify its equivalent `MW × 8760 × 70%` conversion.
7. Calculate gross renewable residual as demand minus thermal minus nuclear.
8. Subtract the direct existing-plus-FIT annual credit.
9. Report both the signed shortfall and its positive part.
10. Compare every diagnostic result with the immutable historical result and assign an evidence-based classification.

## Direct answers to common interpretation questions

### How is RE100 made?

The thesis does not model the corporate RE100 initiative. Its renewable value is an annual residual. Cases 12 and 24 have zero thermal and zero nuclear, so gross renewable generation equals annual demand, but the model still does not prove hourly 100% renewable supply.

### How is supply balance solved?

It is solved by arithmetic, not an optimizer:

`gross renewable = annual demand − permitted thermal − assumed nuclear`.

Each region is independent and has no imports or exports.

### Is BESS used?

No. There is no storage model.

### What is reduced?

The EF cases reduce the carbon share permitted by the one-Earth accounting. This is translated into power-generation CO2 caps. The model then calculates how those caps change permitted thermal energy and the remaining renewable residual. It does not optimize total system emissions or prove an economy-wide one-Earth result.

## Result headline

- canonical baseline: `413.415620 Mt CO2/year`;
- carbon-only cap: `64.148259 Mt`;
- carbon-plus-food cap: `140.691812 Mt`;
- Case 6 positive regional shortfall sum: `388.402687 TWh/year`;
- Case 20 positive regional shortfall sum: `148.896509 TWh/year`;
- all 240 diagnostic rows satisfy annual balance;
- 232 historical rows agree within rounding;
- 2 Case 4 rows are confirmed inconsistent;
- 6 Cases 13–15 rows remain unresolved.

## One-command public run

From the repository root:

```powershell
python src/python/generate_publication_outputs.py
```

This regenerates the canonical Python results, QA, extended CSV tables, and 12 figures in both PNG and SVG. It does not read or alter restricted sources and does not overwrite the immutable historical table.

## Tests

```powershell
python -m unittest discover -s tests -p "test_python_reproduction.py"
matlab -batch "addpath('src/matlab'); results=runtests('tests'); assertSuccess(results);"
```

The public workflow runs Python generation and tests on push and pull request. MATLAB is verified locally.

## Main output index

- [all_24_scenarios_by_region.csv](../results/all_24_scenarios_by_region.csv): complete 240-row diagnostic and historical comparison.
- [reproduction_summary.csv](../results/reproduction_summary.csv): national totals for 24 cases.
- [scenario_assumptions_24.csv](../results/scenario_assumptions_24.csv): exact scenario definitions.
- [source_data_provenance.csv](../results/source_data_provenance.csv): variable-level provenance and limits.
- [source_cell_audit.csv](../results/source_cell_audit.csv): eight discrepancies with source cells and evidence status.
- [QA_SUMMARY.csv](../results/QA_SUMMARY.csv): every automated check.
- [figure_catalog.csv](../results/figure_catalog.csv): 12 public redrawn figures and their data sources.
- [source_figure_audit.csv](../results/source_figure_audit.csv): coverage of all 32 charts in the named final presentation and conference graph workbook.

## Evidence boundary

Public configuration reproduces the annual equations. Several numerical inputs are permitted derivatives of restricted workbooks. Original formulas, full dependency chains, technology-by-region capacity data, and exact artwork cannot be reproduced without restricted sources. The boundary is itemized in [REPRODUCTION_STATUS.md](REPRODUCTION_STATUS.md).
