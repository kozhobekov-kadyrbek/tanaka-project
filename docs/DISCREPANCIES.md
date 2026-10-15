# Discrepancy evidence and treatment

## Canonical versus alternate workbook

The final Chapter 4 workbook is the canonical reported-result version. Its national baseline is 413.415620 MtCO2 and its carbon-only / carbon-and-food caps are 64.148259 / 140.691812 MtCO2. The alternate main-data workbook reports 308.715247, 47.902268, and 105.060635 MtCO2. These are materially different versions. The canonical executable model does not read alternate-workbook values; alternate numerical derivatives are context only in `data/derived/alternate_main_workbook/`.

## Case 4: confirmed scenario-equivalence inconsistency

The historical cells `再エネ目標量!F6` (Hokuriku) and `再エネ目標量!F7` (Chubu) differ from the equation-based reconstruction. In both regions currently operating nuclear output is zero, as is the zero-nuclear output. Case 4 and Case 6 therefore use the same EF case, thermal case, and nuclear output, and must produce the same reconstructed gross RE value. This is evidence from the published scenario structure, not an assertion about an unavailable original Excel formula.

These two rows retain the classification `confirmed_case4_source_inconsistency`. They are separately available in `results/identified_case4_cell_corrections.csv` and in the full `results/source_cell_audit.csv`.

## Cases 13–15: unresolved source-or-formula inconsistencies

The six Hokuriku/Chubu differences in Cases 13–15 are **not** labelled workbook formula errors. A read-only audit found that the final-workbook source cells are stored numeric constants rather than formulas. The public derivative identifies the cells, reported values, reconstruction, and difference, but there is no formula dependency chain that establishes how those constants were produced. They are therefore classified `unresolved_source_or_formula_inconsistency` with evidence status `source_cell_identified_formula_unavailable`.

No hard-coded mismatch magnitude is used to pass QA. The verifier computes each difference from the immutable historical table and equation-based reconstruction, then accepts only the documented scenario-region classifications; any other mismatch fails validation.

## Cap allocation and renewable-credit limitations

Tokyo and Chubu do not exactly reconstruct from the visible BC table. This is documented as a cap-allocation audit deviation, and final-workbook regional caps remain canonical inputs.

The canonical existing/FIT renewable credit is a workbook-derived annual value. Technology-level capacities are not complete public inputs, so capacity-factor assumptions are historical context rather than a canonical renewable-credit reconstruction.
