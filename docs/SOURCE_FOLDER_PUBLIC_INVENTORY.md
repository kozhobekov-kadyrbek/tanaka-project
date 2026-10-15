# Public inventory of the local Tanaka source folder

## Audit scope

The complete local source folder was hashed on **2026-10-15**. The private inventory contains **437 files** with relative paths, byte sizes, modification metadata, SHA-256 hashes, roles, and publication handling. It is stored outside this repository as `New folder/private_source_inventory_2026-10-15.csv` and is not published because it contains local-source metadata and restricted filenames.

The audit script is [audit_local_sources.py](../src/python/audit_local_sources.py). It also extracted safe metadata for the 18 charts in the final presentation and 14 charts in the conference graph workbook.

## Role counts

| Role | Files |
|---|---:|
| Background, reference, or unrelated material | 323 |
| Primary draft, result, or presentation material | 57 |
| Local derived analysis or inventory | 52 |
| Canonical academic thesis narrative | 1 |
| Canonical final Chapter 4 results workbook | 1 |
| Alternate main-data workbook | 1 |
| Final presentation | 1 |
| Conference graph workbook | 1 |

The large background group includes photovoltaic tutorials, code, administrative files, and reference materials that do not define the canonical annual reproduction.

## Main evidence sources

| Source ID | Safe locator | SHA-256 | Role | Public treatment |
|---|---|---|---|---|
| `tanaka_thesis` | `本論/本論.docx` | `B75F5A879F339B739904DF8191EAACAE4B21C732376575F34498E04C775FF19C` | Academic thesis narrative | Not uploaded; assumptions and section-level findings documented. |
| `canonical_final_workbook` | `本論/4章/結果表.xlsx` | `52B4B9D57D0E3E9319FC83D71E326B5B16B17261C8052B8A8A79E726D7FF6FCA` | Canonical historical outputs and caps | Not uploaded; permitted numerical derivatives only. |
| `alternate_main_workbook` | `本論データ/本論データ.xlsx` | `06838C75D9F13379C8D9EDB15A322829E2A3EF569F1434CF9E671D38BCCB469F` | Alternate formula workbook and context | Not uploaded; isolated benchmark derivatives only. |
| `final_presentation` | `卒論発表/発表資料Vo.7.pptx` | `C8A72469FAFB90D64819B18CDE6F4BD1111A85FE4C9EE7A66AA9F6CD78F1D03A` | Final 38-slide presentation with 18 embedded charts | Not uploaded; chart metadata and original public redraws. |
| `main_workbook_note` | `本論データ/本論データExcelファイルに関して.txt` | `49A7A754D0C96FCFE942FE972ABADF25256DB576C7715393FCAFF622ADEAAD42` | States 2016 basis and orange year-dependent cells | Not uploaded; factual summary only. |
| `conference_graph_workbook` | `電気学会/電気学会グラフ.xlsx` | `F1F98781D7A8580B09C4E77603C8A9F8F690C5F909F161611F750D3250B559F2` | Conference/chart calculations with 14 embedded charts | Not uploaded; chart metadata and evidence status only. |

## Source chart inventory

The final deck contains 18 embedded charts. The conference graph workbook contains 14. Every chart is listed in [source_figure_audit.csv](../results/source_figure_audit.csv) with its topic, evidence status, and public redraw mapping.

Chart themes that can be reconstructed from canonical public configuration are redrawn once even when the sources repeat them. Technology-specific output, capacity-allocation, or externally linked chart series are marked unavailable instead of being fabricated or silently copied.

## Publication boundary

The repository excludes every original `.pptx`, `.docx`, `.xlsx`, `.xls`, `.pdf`, image, archive, and third-party raw dataset. It publishes only original code, configuration, numerical derivatives, QA records, metadata, documentation, and original PNG/SVG redraws.
