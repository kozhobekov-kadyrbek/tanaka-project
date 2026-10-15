# Tested environment

| Component | Tested version | Use |
|---|---:|---|
| Python | 3.11.3 | Reproduction, QA, public tests, figures |
| matplotlib | 3.10.8 | PNG figures |
| openpyxl | 3.1.5 | Optional restricted-workbook numerical extraction only |
| MATLAB | R2025a | Independent annual calculation and tests |
| MATLAB toolboxes | None required beyond base MATLAB | `readtable`, `writetable`, and unit-test framework are used |

Use `pip install -r requirements.txt` in a Python 3.11 environment. The GitHub Actions workflow runs the Python verification and public unit tests. MATLAB testing is run locally because a MATLAB licence is not available in the public workflow.
