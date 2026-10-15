# 1. Background, problem, objective, and contribution

## Research setting

Tanaka's academic thesis asks how much annual renewable electricity Japan's ten utility service regions would require if Japan reduced its ecological footprint (EF) from the 2016 level of about **2.7567 Earth equivalents** to **one Earth**. The final presentation identifies a 2016 electricity and EF baseline and states that carbon uptake land accounts for about **2.0793 Earths**, roughly three quarters of Japan's total EF.

Ecological footprint expresses demand for ecological services in global hectares (`gha`). Biocapacity (`BC`) represents biologically productive capacity. Tanaka connects the national one-Earth narrative to the operational CO2 emitted by fossil electricity generation, allocates an allowed national generation CO2 total among ten regions by visible regional BC, and calculates renewable electricity as the remaining annual energy balance.

## Problem addressed

The practical question is:

> Under prescribed EF, thermal-generation, and nuclear-generation assumptions, what annual renewable generation residual remains in each utility region after permitted thermal generation and assumed nuclear generation, and how much remains after crediting existing and FIT-related renewable output?

The ten regions are Hokkaido, Tohoku, Tokyo, Hokuriku, Chubu, Kansai, Chugoku, Shikoku, Kyushu, and Okinawa. They are accounting regions. The work does not represent transmission lines, hourly exchanges, storage, or electrical network feasibility.

## Motivation

The thesis gives four linked motivations:

1. Japan's 2016 consumption footprint exceeds a one-Earth level.
2. Carbon uptake is the largest EF component and electricity generation is a large operational CO2 source.
3. Environmental burden and biocapacity differ strongly among regions.
4. A national target alone does not show the annual renewable requirement assigned to each utility region.

The final presentation therefore proposes a regional procedure: calculate two one-Earth EF cases, derive national electricity-generation CO2 allowances, allocate them using regional BC, enumerate thermal and nuclear cases, and calculate annual renewable needs.

## Objective

The objective is to **estimate**, for 24 prescribed cases, the annual gross renewable residual and positive additional renewable requirement in each of ten regions. It is a deterministic scenario calculation. There is no cost, capacity, dispatch, or emissions objective function and there are no optimized decision variables.

## Proposed solution

The method has four steps:

1. Construct two one-Earth EF cases: carbon-only reduction and carbon-plus-food reduction.
2. Convert each case's retained carbon share into a national generation CO2 allowance and allocate that allowance among regions by BC share.
3. For each regional allowance, calculate permitted thermal generation under four fuel assumptions and combine it with one of three prescribed nuclear outputs.
4. Balance annual demand with thermal, nuclear, and gross renewable generation, then subtract a workbook-derived existing-plus-FIT annual renewable credit.

The complete calculation is documented in [03_METHODOLOGY_AND_FORMULATIONS.md](03_METHODOLOGY_AND_FORMULATIONS.md).

## Contribution and novelty

The contribution is the combination of:

- a one-Earth EF target;
- a BC-based regional allocation rule;
- ten Japanese utility service regions;
- 24 prescribed thermal/nuclear/EF combinations; and
- an annual shortfall after a historical existing-plus-FIT renewable credit.

This is an application and scenario-accounting framework. The work does not establish a new general EF method, a least-cost plan, or a physically feasible renewable portfolio. Its reported minimum and maximum are comparisons among 24 enumerated cases, not global optima.

## Relationship to other studies

| Study or method | Main focus | Relationship to Tanaka |
|---|---|---|
| Global Footprint Network national accounts | Consumption EF and BC using production, trade, yield factors, equivalence factors, and carbon-uptake accounting | Supplies the EF framework and 2016 national context. Tanaka applies a simplified electricity-sector bridge and regional BC allocation. |
| Wakiyama and Kuriyama (2018) | Regional renewable potential, hourly supply-demand relationships, and interregional grid issues in Japan | Closest electricity-system comparison identified in the supplied analysis. Tanaka adds the one-Earth framing but omits hourly operation, transfer limits, curtailment, and grid reform. |
| Muneno and Otsuka (2018) | Technology comparison using life-cycle EF and economic indicators | Shows a technology-level, life-cycle direction absent from Tanaka's annual regional quantity calculation. |

Direct numerical comparison is not valid without harmonizing the year, demand boundary, emissions boundary, renewable potential, and network assumptions.

## What the study does not claim

- It does not model corporate RE100 procurement or certify compliance with the RE100 initiative.
- It does not solve a mathematical optimization problem.
- It does not demonstrate that negative annual residuals can be exported.
- It does not use BESS, hourly dispatch, unit commitment, power flow, transmission capacity, GIS siting, or life-cycle assessment.
- It does not prove that meeting the electricity allowance alone makes Japan's complete consumption footprint equal to one Earth.

## Evidence base

The narrative is based on the restricted academic thesis, final Chapter 4 workbook, final 38-slide presentation, supporting workbooks, and the conference graph workbook. These originals are not published. Safe source fingerprints and roles are in [DATA_MANIFEST.csv](../DATA_MANIFEST.csv) and [SOURCE_FOLDER_PUBLIC_INVENTORY.md](SOURCE_FOLDER_PUBLIC_INVENTORY.md).
