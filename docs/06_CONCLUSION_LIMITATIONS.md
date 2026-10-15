# 6. Conclusion, limitations, gaps, and weaknesses

## Main conclusion

Tanaka converts a one-Earth ecological-footprint narrative into ten regional annual renewable-generation shortfalls under 24 prescribed supply assumptions. The reproduction confirms the central qualitative result: Tokyo, Chubu, Kansai, and Okinawa retain positive additional renewable requirements in every enumerated case, while other regions are more sensitive to the EF, fuel, and nuclear assumptions.

For cases retaining thermal generation, the largest reproduced positive regional sum is Case 6 at **388.40 TWh/year**, and the smallest is Case 20 at **148.90 TWh/year**. These values are annual arithmetic requirements under fixed assumptions, not optimized plans.

## Main contribution

The useful contribution is the traceable chain from national EF scenarios to regional CO2 allowances and annual energy residuals. It exposes how a BC allocation rule, fossil emission factors, nuclear availability, and existing/FIT credit affect regional results.

## Author-identified future work

The source identifies interregional transmission, renewable resource potential, and life-cycle CO2 treatment as future directions. Those omissions are material because the largest deficits occur in urban or geographically constrained regions.

## Limitations and gaps

| Priority | Gap | Consequence | Stronger next step |
|---|---|---|---|
| Critical | No optimization objective or decision variables | “Minimum” means the lowest of 24 chosen cases, not the least-cost or globally best plan. | Define a policy objective and solve a capacity-expansion/dispatch problem. |
| Critical | Annual energy is not operational feasibility | The calculation omits peak adequacy, hourly renewable coincidence, reserves, curtailment, and ramping. | Add hourly demand, weather profiles, dispatch, reserves, and reliability metrics. |
| Critical | National consumption EF is bridged to regional production-side power emissions | Meeting the power allowance does not prove total Japanese consumption EF equals one Earth. | Reconcile sectoral and trade accounting and calculate total EF after power-sector changes. |
| High | No transmission model | Negative residuals cannot be interpreted as usable exports; regional deficits cannot be supplied across actual bottlenecks. | Model topology, line limits, losses, frequency converters, and expansion. |
| High | No BESS or other storage | Annual matching cannot establish 24/7 renewable supply. | Add charge/discharge power, energy, efficiency, state of charge, degradation, and chronology. |
| High | No renewable potential, siting, or land constraint | A TWh deficit does not show which technology can be built or whether local resource and land are sufficient. | Add technology-specific potential, land/roof limits, interconnection, and siting costs. |
| High | BC allocation is a normative choice | Results strongly favor land-rich regions and constrain dense regions; Hokkaido can receive a cap above baseline. | Compare BC, population, demand, grandfathering, mitigation-cost, and hybrid allocations. |
| High | Final and alternate workbooks differ materially | A reader using the alternate workbook cannot reproduce the final thesis values. | Freeze source versions and maintain a reconciliation ledger. |
| High | FIT approval and all-candidate nuclear are treated as certain output | Best-case shortfalls can be understated if projects or reactors do not materialize. | Use realization probabilities, delays, availability ranges, and scenario bounds. |
| Medium | Direct combustion emissions only | Upstream fuel, construction, land use, decommissioning, and life-cycle burdens are omitted. | Use a consistent life-cycle inventory and EF conversion method. |
| Medium | Fixed deterministic 2016 demand and capacity factors | Electrification, efficiency, population, climate, and weather uncertainty are absent. | Establish a target year and use sensitivity, stochastic, or robust cases. |
| Medium | Existing/FIT credit is an aggregate input | Technology capacities, overlap, curtailment, and actual commissioning cannot be independently audited publicly. | Publish de-duplicated asset-level data where licensing permits. |
| Medium | Pumped-storage accounting is unclear in historical sources | Gross generation can be credited without accounting for pumping consumption and losses. | Use net storage energy and trace charging sources. |
| Medium | No cost, build rate, or deployment pathway | TWh results do not give GW, investment, land, workforce, or schedule. | Convert deficits into endogenous capacity with capex, opex, lifetime, and build constraints. |
| Medium | Food-sector feasibility is not modeled | The easier carbon-plus-food result depends on unmodeled diet, imports, yields, and waste reductions. | Couple to a food/land model or treat food reduction explicitly as an external sensitivity. |

## Documented source discrepancies

1. The canonical final workbook uses a `413.416 Mt` baseline and `64.148/140.692 Mt` caps. The alternate main-data workbook uses `308.715 Mt` and `47.902/105.061 Mt`. The reason is unavailable.
2. The visible BC allocation does not exactly reconstruct Tokyo and Chubu, although the differences offset nationally.
3. Case 4 Hokuriku/Chubu is a confirmed source inconsistency based on scenario equivalence.
4. Cases 13–15 Hokuriku/Chubu remain unresolved because the final cells are stored values without formula dependencies.
5. The source narrative's `0.71 gha/person` wording for carbon plus food mixes an Earth-equivalent value with a gha/person value; the workbook gives `0.7076 Earths` and `1.1533 gha/person`.
6. Historical presentation/conference rounding reports roughly 413–416 Mt, so source-version and rounding labels must be retained.

## Recommended continuation

A defensible next study would be a multi-region hourly capacity-expansion and dispatch model that minimizes discounted system cost subject to an explicitly reconciled sectoral CO2 or total-EF budget and a reliability requirement. Renewable capacity, storage, thermal/nuclear operation, demand response, and transmission could be endogenous. Regional renewable potential, land use, life-cycle impacts, and alternative allowance rules should be tested. Tanaka's annual calculation should remain the first validation benchmark.

That recommended model is outside this repository's scope. This repository preserves and explains the original annual accounting before any extension.
