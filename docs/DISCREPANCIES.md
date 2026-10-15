# Source discrepancies and treatment

## Canonical versus alternate version

The final Chapter 4 workbook is canonical because it matches the thesis narrative and stated benchmarks. Its baseline generation emissions are 413.415620 Mt CO2 and its national allowances are 64.148259 Mt (carbon-only) and 140.691812 Mt (carbon-and-food). The alternate main-data workbook reports 308.715247, 47.902268, and 105.060635 Mt respectively. The discrepancy is materially larger than rounding, so this reproduction does not mix the versions. See [`alternate_key_benchmarks.csv`](../data/derived/alternate_main_workbook/alternate_key_benchmarks.csv).

## Historical final-workbook formula/cell errors

The cached final workbook contains eight values inconsistent with its own annual equations. They are retained in [`as_reported_240.csv`](../data/derived/canonical_final_workbook/as_reported_240.csv), and equation-based values appear in the results table.

| Cases | Regions | Diagnostic change in gross RE requirement |
|---|---|---:|
| 4 | Hokuriku | +9.841287 TWh |
| 4 | Chubu | -9.841287 TWh |
| 13, 14, 15 | Hokuriku | +3.824572 TWh each |
| 13, 14, 15 | Chubu | -14.410882 TWh each |

Case 4 is particularly clear: Hokuriku and Chubu have zero current nuclear generation, so Case 4 must equal Case 6 under the same EF and thermal assumptions. The two Case 4 cells transfer 9.841287 TWh between these regions. The complete eight-row audit is [`identified_workbook_formula_discrepancies.csv`](../results/identified_workbook_formula_discrepancies.csv); the required narrower Case 4 file is [`identified_case4_cell_corrections.csv`](../results/identified_case4_cell_corrections.csv).

## Nuclear and renewable-credit caveats

The alternate workbook contains a current-nuclear formula defect in one Kansai entry. The final results imply the full 25.1412 TWh current Kansai output, so that final output is used. The canonical final workbook also provides only regional annual existing/FIT renewable credits; its asset-level capacities cannot be reconstructed from that result sheet. The capacity factors remain published as assumptions and MW-to-TWh nuclear conversion is tested explicitly.

Pumped hydro is separately present in the alternate workbook and can be a generation-accounting ambiguity because it consumes electricity. No net-energy loss reconciliation is available in the source; the canonical annual credit is reproduced as supplied.
