# 3. Methodology and complete formulation

## Model class

The executable reproduction is a **deterministic annual energy-accounting model**. It enumerates prescribed scenarios. It has no objective function, optimizer, decision variables, feasible-region search, shadow prices, or optimality proof. Therefore it is not an LP, MILP, nonlinear program, stochastic program, or robust optimization model.

## Indices, variables, and parameters

| Symbol | Meaning | Unit or domain | Status |
|---|---|---|---|
| `i` | consumption product in the general EF method | category | historical method |
| `l` | land class | category | historical method |
| `j` | utility region | 10 regions | executable index |
| `k` | fossil fuel | coal, LNG, oil | executable index |
| `p` | renewable technology | hydro, wind, solar, geothermal | historical context |
| `s` | prescribed scenario | 1…24 | executable index |
| `D_j` | regional annual electricity quantity treated as demand | TWh/year | direct canonical input |
| `C_j^0` | regional baseline operational generation CO2 | Mt/year | direct canonical input |
| `C_j^cap` | canonical regional CO2 allowance | Mt/year | direct canonical input |
| `BC_j` | visible regional biocapacity | gha | formula-audit input |
| `e_k` | direct combustion emission factor | g CO2/kWh | parameter |
| `w_jks` | fossil fuel share, normalized within thermal generation | fraction | parameter |
| `T_js` | permitted annual thermal generation | TWh/year | calculated quantity |
| `K_js` | equivalent nuclear capacity under a case | MW | conversion-check input |
| `N_js` | annual nuclear generation | TWh/year | canonical input and checked quantity |
| `R_js^gross` | gross renewable energy balance residual | TWh/year | calculated quantity |
| `Rbar_j` | canonical existing-plus-FIT annual RE credit | TWh/year | direct workbook-derived input |
| `A_js` | signed net renewable shortfall | TWh/year | calculated quantity |
| `A_js^build` | positive additional renewable requirement | TWh/year | calculated quantity |

`T`, `N`, `R`, and `A` are calculated outputs, not optimization decisions.

## General EF equations documented in the source

### Net consumption

For product `i`:

\[
Q_i=P_i+I_i-X_i
\]

where `P`, `I`, and `X` are production, imports, and exports.

### Physical area per person

\[
aa_i=\frac{c_i}{y_i}
\]

where `c_i` is per-person consumption and `y_i` is yield per physical hectare.

### Simplified footprint and population footprint

\[
ef=\sum_i aa_i,
\qquad EF_{pop}=Population\times ef
\]

### Equivalence conversion

\[
EF_{i,l}[gha]=aa_i[ha]\times EQF_l[gha/ha]
\]

### Biocapacity

\[
BC_{j,l}=A_{j,l}\,YF_l\,EQF_l,
\qquad BC_j=\sum_l BC_{j,l}
\]

`A` is physical land area, `YF` is a yield factor, and `EQF` is an equivalence factor. The regional calculation includes forest, cropland, grazing land, and built-up land. Fishing grounds are excluded because the source says they cannot be allocated accurately to the ten regions. Carbon uptake land is an EF demand category and is not included as a separate BC category.

### Yield factor

\[
YF_{N,l}=\frac{Y_{N,l}}{Y_{W,l}}
\]

For the cropland derivation:

\[
A_N=\frac{P_N}{Y_N},\qquad A_W=\frac{P_N}{Y_W},\qquad YF_{N,crop}=\frac{A_W}{A_N}
\]

## Electricity CO2 and EF bridge

### Generic source emission-factor definition

The thesis first describes an organization-level factor as:

\[
e=\frac{\text{measured CO2 emissions}}{\text{electricity sold}}
\]

The executable workbook calculation instead uses fuel-specific generation factors, so those two numerator/denominator boundaries should not be treated as identical.

### Fuel emissions

\[
C_{jk}^{0}=E_{jk}^{0}e_k,
\qquad C_j^0=\sum_k C_{jk}^{0}
\]

The executable factors are coal `863.8`, LNG `375.7`, and oil `695.1 g CO2/kWh`. These are operational combustion factors; upstream and construction emissions are outside the calculation.

### Carbon uptake EF

\[
EF_{CO2}=C\times EQF_{forest}\times F_{forest}
\]

with:

\[
F_{forest}=\frac{A_{forest}}{S_{forest}}
\]

The thesis describes `EQF_forest ≈ 1.28 gha/ha` and a forest conversion near `0.29 ha/(t CO2/year)`. Rounded narrative inputs do not reproduce that coefficient exactly, so this public project treats the EF scenario table as historical context and the final regional caps as canonical numerical inputs.

### Earth-equivalent contribution

\[
n_l=\frac{EF_{Japan,l}^{per-person}}{BC_{world}^{per-person}}
\]

The historical denominator is `1.62975071059329 gha/person`. The 2016 total is:

\[
\frac{4.4926984184}{1.6297507106}=2.7566783001\text{ Earths}
\]

### National generation CO2 cap bridge

The workbook logic retains the same proportion of generation CO2 as the retained national carbon EF:

\[
C_{nat}^{cap}=C_{nat}^{0}
\frac{EF_{CO2}^{case}}{EF_{CO2}^{2016}}
\]

This produces the canonical national totals `64.148259 Mt` and `140.691812 Mt` from the final-workbook baseline `413.415620 Mt`.

## Regional cap allocation

The stated allocation is:

\[
C_{j}^{formula}=C_{nat}^{cap}\frac{BC_j}{\sum_m BC_m}
\]

The public code audits this equation. It does **not** use `C_j^formula` as the executable cap because the visible BC table fails to reconstruct Tokyo and Chubu exactly. The executable model uses the final-workbook values:

\[
C_j^{canonical}=\text{final-workbook-derived regional cap}
\]

Eight regions reconstruct within `1e-9 Mt`. Tokyo and Chubu have equal and opposite deviations of `0.766235 Mt` in the carbon-only case and `1.680529 Mt` in the carbon-plus-food case. See [CO2_cap_allocation_audit.csv](../results/CO2_cap_allocation_audit.csv).

## Thermal generation

Raw fuel shares are normalized within fossil generation:

\[
\hat w_{jks}=\frac{w_{jks}}{\sum_k w_{jks}},
\qquad \sum_k\hat w_{jks}=1
\]

The weighted direct emission factor is:

\[
\bar e_{js}=\sum_k\hat w_{jks}e_k
\]

With `C` in Mt and `e` in g/kWh, permitted thermal energy in TWh is:

\[
T_{js}=\frac{1000C_j^{canonical}}{\bar e_{js}}
\]

For the zero-thermal case, `T_js=0`. For LNG-only, `e-bar=375.7 g/kWh`.

## Nuclear generation

\[
N_{js}=\frac{K_{js}[MW]\times8760[h/year]\times0.70}{10^6}
\quad[TWh/year]
\]

The canonical annual nuclear quantities are direct scenario inputs. Equivalent MW values verify this conversion; they are not presented as a recovered unit-level source database.

## Renewable balance

### Gross annual renewable residual

\[
R_{js}^{gross}=D_j-T_{js}-N_{js}
\]

Therefore the annual identity is:

\[
D_j=T_{js}+N_{js}+R_{js}^{gross}
\]

### Historical capacity-to-energy equation

The source workbooks use:

\[
R_{jp}=K_{jp}\times8760\times cf_p
\]

for technology capacity `K` and capacity factor `cf`. The public canonical reproduction does **not** use this equation to recalculate the existing-plus-FIT credit because complete technology-by-region capacity inputs and an overlap audit are not publicly available. `Rbar_j` is read directly as an annual workbook-derived credit.

### Signed and positive additional requirement

\[
A_{js}=R_{js}^{gross}-\bar R_j
\]

\[
A_{js}^{build}=\max(0,A_{js})
\]

Negative `A` is retained for audit but is not treated as exportable power.

## What is optimized?

Nothing. The model calculates one result for each fixed scenario. A future optimization could introduce endogenous capacities, dispatch, storage, and transmission, but those variables and constraints do not belong to Tanaka's formulation and are not implemented here.
