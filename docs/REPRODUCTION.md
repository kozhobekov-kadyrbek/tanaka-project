# Reproduction procedure

## Public reproduction

Install the pinned dependency range in `requirements.txt`, then run:

```powershell
python src/python/generate_publication_outputs.py
python -m unittest discover -s tests -p "test_python_reproduction.py"
matlab -batch "addpath('src/matlab'); results=runtests('tests'); assertSuccess(results);"
```

The first command produces all diagnostic CSVs, QA output, and figures. It does not modify `data/derived/canonical_final_workbook/as_reported_240.csv`.

## Restricted-workbook extraction

Only a holder of the restricted final workbook can rerun extraction of the historical numerical table:

```powershell
python src/python/extract_local_sources.py --final-workbook "C:\private\結果表.xlsx" --output-root .
```

Do not commit that workbook or any original DOCX/XLSX/PDF. The public data manifest records the local source fingerprints and transformations without publishing the sources.

## Verification contract

The Python and MATLAB tests separately check the 24×10 scenario matrix, annual balance, fuel normalization, nuclear conversion, cap audit, canonical-table integrity, Case 4 evidence, unresolved Cases 13–15 classification, and canonical/alternate separation. `results/QA_SUMMARY.csv` reports status, tolerance, and explanation for each check.

See [REPRODUCTION_STATUS.md](REPRODUCTION_STATUS.md) for the boundary between public reproducibility and restricted-source dependence.
