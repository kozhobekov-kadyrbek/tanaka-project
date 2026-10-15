"""Independent annual-accounting calculation and verification for Tanaka Chapter 4.

All energy values are annual TWh and all CO2 values are Mt unless the column name
says otherwise.  The model is deliberately annual: it has no chronological
dispatch, inter-regional transfer, storage, curtailment, BESS, or capacity build
optimisation.
"""
from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config"
RESULTS = ROOT / "results"
DERIVED = ROOT / "data" / "derived"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def build_model() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    scenarios = read_csv(CONFIG / "scenario_definitions.csv")
    regional = read_csv(CONFIG / "regional_demand_and_existing_RE.csv")
    biocap = read_csv(CONFIG / "EF_and_biocapacity_assumptions.csv")
    factors = {r["fuel"]: f(r, "g_co2_per_kwh") for r in read_csv(CONFIG / "fossil_emission_factors.csv")}
    shares = read_csv(CONFIG / "thermal_fuel_shares.csv")
    nuclear = read_csv(CONFIG / "nuclear_scenarios.csv")
    region_order = [r["region"] for r in regional]
    reg = {r["region"]: r for r in regional}
    bc = {r["region"]: r for r in biocap}
    nuke = {(r["region"], r["nuclear_case"]): r for r in nuclear}
    share_by_key = {(r["region"], r["thermal_case"]): r for r in shares}

    components = ("forest_gha", "cropland_gha", "grazing_gha", "built_up_gha")
    bc_total = {region: sum(f(bc[region], c) for c in components) for region in region_order}
    national_bc = sum(bc_total.values())
    national_caps = {
        "carbon_only": sum(f(bc[r], "carbon_only_cap_mt") for r in region_order),
        "carbon_and_food": sum(f(bc[r], "carbon_and_food_cap_mt") for r in region_order),
    }

    caps: list[dict[str, object]] = []
    for region in region_order:
        for ef_case, cap_column in (("carbon_only", "carbon_only_cap_mt"),
                                    ("carbon_and_food", "carbon_and_food_cap_mt")):
            allocated = national_caps[ef_case] * bc_total[region] / national_bc
            caps.append({
                "region": region, "EF_case": ef_case,
                "biocapacity_gha": f"{bc_total[region]:.6f}",
                "allocated_cap_mt": f"{allocated:.12f}",
                "reported_cap_mt": f"{f(bc[region], cap_column):.12f}",
                "allocation_delta_mt": f"{allocated - f(bc[region], cap_column):.12g}",
                "baseline_co2_mt": f"{f(bc[region], 'baseline_co2_mt'):.12f}",
            })

    output: list[dict[str, object]] = []
    for scenario in scenarios:
        number = int(scenario["scenario"])
        ef_case = scenario["ef_case"]
        for region in region_order:
            # The final workbook supplies the ten published regional allowances.
            # We retain them as canonical calculation inputs.  The adjacent audit
            # column records whether its visible BC table reconstructs them exactly.
            cap_column = "carbon_only_cap_mt" if ef_case == "carbon_only" else "carbon_and_food_cap_mt"
            cap = f(bc[region], cap_column)
            share = share_by_key.get((region, scenario["thermal_case"]),
                                     share_by_key.get(("all", scenario["thermal_case"])))
            raw = [f(share, x) for x in ("coal_share", "lng_share", "oil_share")]
            raw_total = sum(raw)
            if raw_total:
                weights = [x / raw_total for x in raw]
                weighted_factor = sum(w * factors[fuel] for w, fuel in zip(weights, ("coal", "lng", "oil")))
                thermal = 1000 * cap / weighted_factor
            else:
                weights, weighted_factor, thermal = [0.0, 0.0, 0.0], 0.0, 0.0
            nuc = nuke[(region, scenario["nuclear_case"])]
            nuclear_twh = f(nuc, "annual_generation_twh")
            nuclear_formula_twh = f(nuc, "equivalent_capacity_mw") * f(nuc, "hours_per_year") * f(nuc, "capacity_factor") / 1_000_000
            gross = f(reg[region], "demand_twh") - thermal - nuclear_twh
            existing = f(reg[region], "existing_plus_fit_re_twh")
            signed = gross - existing
            output.append({
                "scenario": number, "EF_case": ef_case, "thermal_case": scenario["thermal_case"],
                "nuclear_case": scenario["nuclear_case"], "region": region,
                "allocated_CO2_cap_Mt": f"{cap:.9f}",
                "weighted_fossil_EF_gCO2_per_kWh": f"{weighted_factor:.9f}",
                "coal_weight": f"{weights[0]:.9f}", "lng_weight": f"{weights[1]:.9f}",
                "oil_weight": f"{weights[2]:.9f}", "thermal_generation_TWh": f"{thermal:.9f}",
                "nuclear_generation_TWh": f"{nuclear_twh:.9f}",
                "nuclear_formula_generation_TWh": f"{nuclear_formula_twh:.9f}",
                "gross_RE_requirement_TWh": f"{gross:.9f}",
                "assumed_existing_plus_FIT_RE_TWh": f"{existing:.9f}",
                "signed_net_RE_shortfall_TWh": f"{signed:.9f}",
                "positive_additional_RE_TWh": f"{max(0, signed):.9f}",
                "annual_energy_identity_residual_TWh": f"{f(reg[region], 'demand_twh') - thermal - nuclear_twh - gross:.12g}",
            })
    return output, caps


def load_reported() -> dict[tuple[int, str], dict[str, str]]:
    rows = read_csv(DERIVED / "canonical_final_workbook" / "as_reported_240.csv")
    if len(rows) != 240:
        raise AssertionError(f"Expected 240 canonical reported rows, found {len(rows)}")
    return {(int(r["scenario"]), r["region"]): r for r in rows}


def enrich_and_verify(calculated: list[dict[str, object]], caps: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    reported = load_reported()
    # Independently recomputed values reveal eight historical formula/cell errors:
    # two in Case 4 and the Hokuriku/Chubu pair in Cases 13--15.  They remain in
    # as_reported_240.csv; these expected deltas simply make the audit explicit.
    known_deltas = {
        (4, "北陸"): 9.841286852, (4, "中部"): -9.841286869,
        (13, "北陸"): 3.824572444, (13, "中部"): -14.410882357,
        (14, "北陸"): 3.824572444, (14, "中部"): -14.410882357,
        (15, "北陸"): 3.824572444, (15, "中部"): -14.410882357,
    }
    verification: list[dict[str, object]] = []
    for row in calculated:
        key = (int(row["scenario"]), str(row["region"]))
        historical = reported[key]
        reported_gross = float(historical["gross_RE_requirement_TWh"])
        reported_signed = float(historical["signed_net_RE_shortfall_TWh"])
        calc_gross = float(row["gross_RE_requirement_TWh"])
        calc_signed = float(row["signed_net_RE_shortfall_TWh"])
        gross_delta = calc_gross - reported_gross
        signed_delta = calc_signed - reported_signed
        correction = key in known_deltas
        # The source workbook prints six decimal places; all other rows should agree
        # with the independently reimplemented annual equations within this rounding.
        expected_match = abs(gross_delta) <= 1.1e-6 and abs(signed_delta) <= 1.1e-6
        if correction:
            expected_match = abs(gross_delta - known_deltas[key]) <= 2e-6 and abs(signed_delta - known_deltas[key]) <= 2e-6
        energy_ok = abs(float(row["annual_energy_identity_residual_TWh"])) < 1e-10
        nuclear_ok = abs(float(row["nuclear_generation_TWh"]) - float(row["nuclear_formula_generation_TWh"])) < 1.1e-6
        row.update({
            "as_reported_gross_RE_requirement_TWh": f"{reported_gross:.6f}",
            "as_reported_signed_net_RE_shortfall_TWh": f"{reported_signed:.6f}",
            "as_reported_positive_additional_RE_TWh": f"{float(historical['positive_additional_RE_TWh']):.6f}",
            "gross_delta_diagnostic_minus_reported_TWh": f"{gross_delta:.9f}",
            "result_version": "diagnostic_corrected",
            "quality_flag": "historical_workbook_formula_error_corrected" if correction else "consistent_with_arithmetic",
        })
        verification.append({
            "scenario": key[0], "region": key[1],
            "reported_gross_RE_TWh": f"{reported_gross:.6f}", "diagnostic_gross_RE_TWh": f"{calc_gross:.9f}",
            "gross_delta_TWh": f"{gross_delta:.9f}", "reported_signed_shortfall_TWh": f"{reported_signed:.6f}",
            "diagnostic_signed_shortfall_TWh": f"{calc_signed:.9f}", "signed_delta_TWh": f"{signed_delta:.9f}",
            "annual_energy_identity_pass": energy_ok,
            "nuclear_capacity_formula_pass": nuclear_ok,
            "expected_source_comparison_pass": expected_match,
            "quality_flag": row["quality_flag"],
        })
    if len(verification) != 240 or not all(r["annual_energy_identity_pass"] and r["nuclear_capacity_formula_pass"] and r["expected_source_comparison_pass"] for r in verification):
        failed = [r for r in verification if not (r["annual_energy_identity_pass"] and r["nuclear_capacity_formula_pass"] and r["expected_source_comparison_pass"])]
        raise AssertionError(f"Verification failed for {len(failed)} of {len(verification)} rows")
    return calculated, verification


def write_outputs(calculated: list[dict[str, object]], caps: list[dict[str, object]], verification: list[dict[str, object]]) -> None:
    write_csv(RESULTS / "all_24_scenarios_by_region.csv", calculated)
    write_csv(RESULTS / "regional_CO2_baseline_and_caps.csv", caps)
    write_csv(RESULTS / "regional_demand_and_assumed_RE.csv", read_csv(CONFIG / "regional_demand_and_existing_RE.csv"))
    write_csv(RESULTS / "verification_240_rows.csv", verification)
    corrected = [r for r in calculated if r["quality_flag"] == "historical_workbook_formula_error_corrected"]
    corrections = [{
        "region": r["region"], "scenario": r["scenario"],
        "workbook_gross_RE_TWh": r["as_reported_gross_RE_requirement_TWh"],
        "arithmetic_expected_gross_RE_TWh": r["gross_RE_requirement_TWh"],
        "expected_minus_workbook_TWh": r["gross_delta_diagnostic_minus_reported_TWh"],
        "workbook_signed_net_shortfall_TWh": r["as_reported_signed_net_RE_shortfall_TWh"],
        "arithmetic_expected_signed_net_shortfall_TWh": r["signed_net_RE_shortfall_TWh"],
    } for r in corrected]
    write_csv(RESULTS / "identified_workbook_formula_discrepancies.csv", corrections)
    write_csv(RESULTS / "identified_case4_cell_corrections.csv", [r for r in corrections if int(r["scenario"]) == 4])

    summary = []
    by_scenario: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in calculated:
        by_scenario[int(row["scenario"])].append(row)
    for scenario, rows in sorted(by_scenario.items()):
        summary.append({
            "scenario": scenario, "EF_case": rows[0]["EF_case"], "thermal_case": rows[0]["thermal_case"],
            "nuclear_case": rows[0]["nuclear_case"], "regions": len(rows),
            "diagnostic_total_thermal_TWh": f"{sum(float(x['thermal_generation_TWh']) for x in rows):.6f}",
            "diagnostic_total_nuclear_TWh": f"{sum(float(x['nuclear_generation_TWh']) for x in rows):.6f}",
            "diagnostic_total_gross_RE_TWh": f"{sum(float(x['gross_RE_requirement_TWh']) for x in rows):.6f}",
            "diagnostic_total_positive_additional_RE_TWh": f"{sum(float(x['positive_additional_RE_TWh']) for x in rows):.6f}",
            "reported_total_positive_additional_RE_TWh": f"{sum(float(x['as_reported_positive_additional_RE_TWh']) for x in rows):.6f}",
            "verification_passed_rows": sum(1 for x in verification if int(x['scenario']) == scenario and x['expected_source_comparison_pass']),
        })
    write_csv(RESULTS / "reproduction_summary.csv", summary)

    alternate = [
        {"metric": "alternate_main_workbook_national_2016_CO2_Mt", "value": "308.715247014", "canonical_final_value": "413.415620233", "difference": "-104.700373219", "note": "Different workbook/version; not used by canonical reproduction"},
        {"metric": "alternate_main_workbook_carbon_only_cap_Mt", "value": "47.902267785", "canonical_final_value": "64.148259403", "difference": "-16.245991618", "note": "Different workbook/version; not used by canonical reproduction"},
        {"metric": "alternate_main_workbook_carbon_and_food_cap_Mt", "value": "105.060634726", "canonical_final_value": "140.691811913", "difference": "-35.631177187", "note": "Different workbook/version; not used by canonical reproduction"},
    ]
    write_csv(DERIVED / "alternate_main_workbook" / "alternate_key_benchmarks.csv", alternate)


def make_figures(calculated: list[dict[str, object]]) -> None:
    import matplotlib.pyplot as plt
    RESULTS.joinpath("figures").mkdir(parents=True, exist_ok=True)
    grouped: dict[int, float] = defaultdict(float)
    for row in calculated:
        grouped[int(row["scenario"])] += float(row["positive_additional_RE_TWh"])
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(list(grouped), [grouped[i] for i in grouped], color="#246eb9")
    ax.set(xlabel="Scenario", ylabel="Positive additional renewable requirement (TWh/year)", xticks=list(grouped))
    ax.grid(axis="y", alpha=.25)
    fig.tight_layout()
    fig.savefig(RESULTS / "figures" / "positive_additional_RE_by_case.png", dpi=180)
    plt.close(fig)

    regions = ["北海道", "東北", "東京", "北陸", "中部", "関西", "中国", "四国", "九州", "沖縄"]
    region_labels = ["Hokkaido", "Tohoku", "Tokyo", "Hokuriku", "Chubu", "Kansai", "Chugoku", "Shikoku", "Kyushu", "Okinawa"]
    values = {case: [float(next(r for r in calculated if int(r["scenario"]) == case and r["region"] == region)["positive_additional_RE_TWh"]) for region in regions] for case in (6, 20)}
    x = list(range(len(regions)))
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar([v - .19 for v in x], values[6], width=.38, label="Case 6: carbon-only, 2030 mix, zero nuclear")
    ax.bar([v + .19 for v in x], values[20], width=.38, label="Case 20: carbon+food, LNG-only, all candidate nuclear")
    ax.set_xticks(x, region_labels, rotation=25, ha="right"); ax.set_ylabel("Positive additional renewable requirement (TWh/year)")
    ax.legend(fontsize=8); ax.grid(axis="y", alpha=.25)
    fig.tight_layout()
    fig.savefig(RESULTS / "figures" / "case6_vs_case20_by_region.png", dpi=180)
    plt.close(fig)


def main() -> None:
    calculated, caps = build_model()
    calculated, verification = enrich_and_verify(calculated, caps)
    write_outputs(calculated, caps, verification)
    make_figures(calculated)
    print("Verified 240 region-scenario results; 232 arithmetic matches and 8 documented workbook formula corrections.")


if __name__ == "__main__":
    main()
