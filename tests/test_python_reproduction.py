"""Public Python QA tests for the Tanaka deterministic annual reproduction."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "python"))
import verify_results as vr  # noqa: E402


class TanakaAnnualAccountingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.calculated, cls.caps, cls.inputs = vr.build_model()
        cls.calculated, cls.verification, cls.audit = vr.enrich_and_verify(cls.calculated, cls.inputs)

    def test_24_scenarios_times_10_regions(self) -> None:
        self.assertEqual(len(self.calculated), 240)
        self.assertEqual({(int(r["scenario"]), r["region"]) for r in self.calculated}, {(s, r) for s in range(1, 25) for r in vr.REGIONS})

    def test_annual_energy_identity(self) -> None:
        self.assertTrue(all(abs(float(r["annual_energy_identity_residual_TWh"])) < vr.IDENTITY_TOLERANCE_TWH for r in self.calculated))

    def test_fuel_share_normalization(self) -> None:
        for row in self.calculated:
            if float(row["weighted_fossil_EF_gCO2_per_kWh"]) > 0:
                self.assertAlmostEqual(sum(float(row[key]) for key in ("coal_weight", "lng_weight", "oil_weight")), 1.0, places=8)

    def test_nuclear_mw_to_twh_conversion(self) -> None:
        self.assertTrue(all(abs(float(r["nuclear_generation_TWh"]) - float(r["nuclear_formula_generation_TWh"])) <= vr.CANONICAL_TOLERANCE_TWH for r in self.calculated))

    def test_co2_cap_allocation_audit(self) -> None:
        deviations = {(r["EF_case"], r["region"]) for r in self.caps if r["audit_status"] == "documented_visible_BC_table_deviation"}
        self.assertEqual(deviations, {(case, region) for case in ("carbon_only", "carbon_and_food") for region in ("東京", "中部")})
        self.assertTrue(all(abs(float(r["allocation_delta_mt"])) < 1e-9 for r in self.caps if r["audit_status"] == "reconstructs_within_tolerance"))

    def test_canonical_workbook_derived_input_table_integrity(self) -> None:
        vr.validate_input_tables(self.inputs)
        self.assertEqual(len(self.inputs["reported"]), 240)
        self.assertTrue(all(row["source_cell_gross"] for row in self.inputs["reported"]))

    def test_case4_discrepancy_is_confirmed_by_scenario_equivalence(self) -> None:
        case4 = {(int(r["scenario"]), r["region"]) for r in self.audit if r["classification"] == "confirmed_case4_source_inconsistency"}
        self.assertEqual(case4, vr.CASE4_KEYS)
        reconstructed = {(int(r["scenario"]), r["region"]): float(r["gross_RE_requirement_TWh"]) for r in self.calculated}
        for _, region in vr.CASE4_KEYS:
            self.assertAlmostEqual(reconstructed[(4, region)], reconstructed[(6, region)], places=6)

    def test_cases13_to15_are_unresolved_not_formula_errors(self) -> None:
        unresolved = [r for r in self.audit if r["classification"] == "unresolved_source_or_formula_inconsistency"]
        self.assertEqual({(int(r["scenario"]), r["region"]) for r in unresolved}, vr.UNRESOLVED_KEYS)
        self.assertTrue(all(r["evidence_status"] == "source_cell_identified_formula_unavailable" for r in unresolved))
        self.assertTrue(all("formula-error" not in r["explanation"] for r in unresolved))

    def test_canonical_and_alternate_inputs_are_separated(self) -> None:
        self.assertTrue(all("Final Chapter 4 workbook" in r["canonical_source_basis"] for r in self.inputs["regional"]))
        self.assertTrue(all("alternate" not in r["source_basis"].lower() for r in self.inputs["nuclear"]))
        self.assertTrue((ROOT / "data" / "derived" / "alternate_main_workbook" / "alternate_key_benchmarks.csv").is_file())

    def test_published_headline_results(self) -> None:
        by_case = {}
        for row in self.calculated:
            by_case.setdefault(int(row["scenario"]), 0.0)
            by_case[int(row["scenario"])] += float(row["positive_additional_RE_TWh"])
        self.assertAlmostEqual(by_case[6], 388.402687, places=6)
        self.assertAlmostEqual(by_case[20], 148.896509, places=6)

    def test_ecological_footprint_context_identity(self) -> None:
        rows = vr.read_csv(ROOT / "config" / "ecological_footprint_scenarios.csv")
        totals = {}
        for row in rows:
            totals.setdefault(row["case"], 0.0)
            totals[row["case"]] += float(row["earth_equivalents"])
        self.assertAlmostEqual(totals["2016_baseline"], 2.756678300069254, places=12)
        self.assertAlmostEqual(totals["carbon_only"], 1.0, places=12)
        self.assertAlmostEqual(totals["carbon_and_food"], 1.0, places=12)

    def test_complete_publication_outputs_exist(self) -> None:
        required = [
            "scenario_assumptions_24.csv", "regional_demand_existing_RE_inputs.csv",
            "regional_biocapacity_components.csv", "ecological_footprint_inputs_and_targets.csv",
            "ecological_footprint_results_by_case.csv", "CO2_cap_allocation_audit.csv",
            "fossil_emission_factors_and_fuel_shares.csv", "nuclear_assumptions_by_region.csv",
            "renewable_capacity_factors.csv", "source_data_provenance.csv",
            "source_cell_audit.csv", "QA_SUMMARY.csv", "figure_catalog.csv", "source_figure_audit.csv",
        ]
        self.assertTrue(all((ROOT / "results" / name).is_file() for name in required))
        self.assertTrue(all((ROOT / "docs" / f"0{number}_{name}.md").is_file() for number, name in [
            (1, "BACKGROUND"), (2, "CASE_STUDIES"), (3, "METHODOLOGY_AND_FORMULATIONS"),
            (4, "SIMULATION_CONDITIONS_AND_DATA"), (5, "RESULTS"),
            (6, "CONCLUSION_LIMITATIONS"), (7, "OVERALL_SUMMARY"),
        ]))

    def test_source_figure_audit_and_public_redraws(self) -> None:
        source_rows = vr.read_csv(ROOT / "results" / "source_figure_audit.csv")
        self.assertEqual(len(source_rows), 32)
        self.assertEqual(sum(row["source_id"] == "final_presentation" for row in source_rows), 18)
        self.assertEqual(sum(row["source_id"] == "conference_graph_workbook" for row in source_rows), 14)
        figures = vr.read_csv(ROOT / "results" / "figure_catalog.csv")
        self.assertEqual(len(figures), 12)
        for row in figures:
            self.assertTrue((ROOT / row["png"]).is_file())
            self.assertTrue((ROOT / row["svg"]).is_file())

    def test_capacity_factors_not_used_for_canonical_re_credit(self) -> None:
        rows = vr.read_csv(ROOT / "results" / "renewable_capacity_factors.csv")
        self.assertTrue(all(row["used_to_recalculate_canonical_existing_FIT_RE_credit"] == "false" for row in rows))

    def test_no_restricted_originals_are_published(self) -> None:
        restricted = {".xlsx", ".xls", ".docx", ".pptx", ".pdf", ".zip"}
        found = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts and path.suffix.lower() in restricted]
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
