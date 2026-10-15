# 2. Case studies and scenario assumptions

## Factorial design

Tanaka enumerates **2 EF cases × 4 thermal cases × 3 nuclear cases = 24 cases**. Every case is evaluated for ten regions, producing 240 region-case records. The exact machine-readable mapping is [scenario_assumptions_24.csv](../results/scenario_assumptions_24.csv).

## EF cases

### Carbon only: Cases 1–12

Non-carbon EF contributions remain at their 2016 values. Carbon uptake is reduced to the remaining one-Earth budget:

- carbon contribution: `0.32264067 Earths`;
- carbon EF: `0.52582386 gha/person`;
- national canonical generation CO2 allowance: `64.148259 Mt/year`;
- reduction from the canonical 413.415620 Mt baseline: about `84.48%`.

### Carbon plus food: Cases 13–24

Cropland, fishing-ground, and grazing contributions are reduced to corresponding Japanese BC contributions; built-up and forest-product contributions remain at their stated levels. Carbon receives the remaining budget:

- carbon contribution: `0.70762482 Earths`;
- carbon EF: `1.15325205 gha/person`;
- national canonical generation CO2 allowance: `140.691812 Mt/year`;
- reduction from the canonical baseline: about `65.97%`.

The food changes are external assumptions. The thesis does not model diets, imports, waste, yields, or a policy pathway that would achieve them.

## Thermal cases

| Thermal case | Scenario numbers in each EF block | Assumption |
|---|---|---|
| `2016_mix` | 1–3 and 13–15 | Region-specific observed coal/LNG/oil values are normalized to sum to one within fossil generation. |
| `2030_mix` | 4–6 and 16–18 | Coal 26%, LNG 27%, and oil 3% of total electricity are normalized within their 56% fossil subtotal: 46.4286%, 48.2143%, and 5.3571%. |
| `lng_only` | 7–9 and 19–21 | All permitted thermal output is LNG. |
| `zero_thermal` | 10–12 and 22–24 | Thermal generation and operational fossil CO2 are set to zero. |

The detailed regional shares and factors are in [fossil_emission_factors_and_fuel_shares.csv](../results/fossil_emission_factors_and_fuel_shares.csv).

## Nuclear cases

| Nuclear case | Position within each three-case block | Assumption |
|---|---:|---|
| `currently_operating` | first | Units identified as operating in the historical study; nonzero only in Kansai, Shikoku, and Kyushu. |
| `all_candidate_units` | second | Operating, authorized, under-review, and construction-listed capacity is assumed available at a uniform 70% capacity factor. |
| `zero_nuclear` | third | Nuclear generation is zero. |

The all-candidate case is an intentionally optimistic counterfactual, not a forecast. Regional inputs are in [nuclear_assumptions_by_region.csv](../results/nuclear_assumptions_by_region.csv).

## Complete case map

| Cases | EF case | Thermal case | Nuclear order |
|---|---|---|---|
| 1–3 | Carbon only | 2016 mix | current; all candidate; zero |
| 4–6 | Carbon only | 2030 mix | current; all candidate; zero |
| 7–9 | Carbon only | LNG only | current; all candidate; zero |
| 10–12 | Carbon only | zero thermal | current; all candidate; zero |
| 13–15 | Carbon plus food | 2016 mix | current; all candidate; zero |
| 16–18 | Carbon plus food | 2030 mix | current; all candidate; zero |
| 19–21 | Carbon plus food | LNG only | current; all candidate; zero |
| 22–24 | Carbon plus food | zero thermal | current; all candidate; zero |

## RE100 interpretation

The study does not implement the corporate RE100 initiative. If “RE100” is used informally to mean a 100% renewable annual balance, only the zero-thermal and zero-nuclear cases 12 and 24 force the **gross annual residual** to equal annual demand. Even then, the model does not establish 24/7 renewable supply because it has no hourly chronology, storage, curtailment, reliability, or network constraints.

In the other cases, renewable generation is the residual after permitted thermal and assumed nuclear output. This is not a 100% renewable supply case.

## Supply balance and negative values

Each region is balanced independently on an annual energy basis:

`demand = thermal + nuclear + gross renewable residual`.

A negative gross or net renewable residual means prescribed annual thermal plus nuclear energy exceeds annual demand or exceeds the demand remaining after the renewable credit. It is an arithmetic surplus. It is not transferable electricity, physical export, curtailment, or stored energy.

## BESS

No battery energy storage system is used. The study has no storage power, storage energy, state of charge, efficiency, degradation, charging, or discharging variable.
