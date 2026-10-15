# Reproduction procedure

## Required local inputs

The original thesis and workbooks are restricted and are not part of this repository. On the local Paper 3 workspace used for this reconstruction, they were located as follows:

| Role | Local relative location |
|---|---|
| Thesis narrative | `本論/本論.docx` |
| Canonical Chapter 4 result workbook | `本論/4章/結果表.xlsx` |
| Alternate main-data workbook | `本論データ/本論データ.xlsx` |
| Existing analysis and its inventory | `New folder/` |

Their fingerprints and transformations are in [`DATA_MANIFEST.csv`](../DATA_MANIFEST.csv). The public repository contains no original PDF, Word, or Excel file.

## Build

From the repository root, first extract the historical reference table only when the private workbook is available:

```powershell
python src/python/extract_local_sources.py --final-workbook "C:\private\結果表.xlsx" --output-root .
```

Then create and audit all annual results and figures:

```powershell
python src/python/verify_results.py
```

Run the independent MATLAB implementation and its test:

```powershell
matlab -batch "addpath('src/matlab'); results=runtests('tests'); assertSuccess(results);"
```

The Python implementation produces the public CSVs and PNGs. MATLAB writes `results/matlab_annual_accounting_results.csv` as a separately generated cross-check. Both use the same published configuration values, but independent implementations and table readers.

## Verification contract

`verify_results.py` confirms 24 × 10 = 240 region-case rows, each annual energy identity, fuel-share normalization, nuclear MW-to-TWh conversion, and comparison with cached final-workbook values. It accepts eight named historical formula/cell discrepancies listed in [`DISCREPANCIES.md`](DISCREPANCIES.md); all other 232 rows agree within the six-decimal rounding printed by the source workbook.

The result file has both `as_reported_*` columns and diagnostic values. `as_reported_240.csv` is a historical derived record. `all_24_scenarios_by_region.csv` is the equation-based diagnostic table and never overwrites that historical record.
