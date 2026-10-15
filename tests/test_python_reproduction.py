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


if __name__ == "__main__":
    unittest.main()
