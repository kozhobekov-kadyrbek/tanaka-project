function tests = test_24_case_reproduction
tests = functiontests(localfunctions);
end

function testScenarioMatrix24By10(testCase)
projectRoot();
results = run_tanaka_reproduction();
verifyEqual(testCase, height(results), 240);
verifyEqual(testCase, numel(unique(strcat(string(results.scenario), "|", results.region))), 240);
verifyEqual(testCase, unique(results.scenario)', 1:24);
end

function testAnnualEnergyIdentity(testCase)
projectRoot();
results = run_tanaka_reproduction();
verifyLessThan(testCase, max(abs(results.annual_energy_identity_residual_TWh)), 1e-10);
end

function testFuelShareNormalization(testCase)
root = projectRoot(); shares = csvTable(fullfile(root, 'config', 'thermal_fuel_shares.csv'));
for row = 1:height(shares)
    total = shares.coal_share(row) + shares.lng_share(row) + shares.oil_share(row);
    if total > 0, verifyEqual(testCase, sum([shares.coal_share(row), shares.lng_share(row), shares.oil_share(row)]) / total, 1, 'AbsTol', 1e-12); end
end
end

function testNuclearMWToTWhConversion(testCase)
root = projectRoot(); nuclear = csvTable(fullfile(root, 'config', 'nuclear_scenarios.csv'));
calculated = calculate_nuclear_generation(nuclear.equivalent_capacity_mw, nuclear.hours_per_year, nuclear.capacity_factor);
verifyLessThanOrEqual(testCase, max(abs(calculated - nuclear.annual_generation_twh)), 1.1e-6);
end

function testCO2CapAllocationAudit(testCase)
root = projectRoot(); bc = csvTable(fullfile(root, 'config', 'EF_and_biocapacity_assumptions.csv'));
[bcTotal, ~] = calculate_biocapacity(bc);
for capColumn = ["carbon_only_cap_mt", "carbon_and_food_cap_mt"]
    reported = bc.(capColumn); formula = calculate_EF_CO2_caps(bcTotal, sum(reported), reported);
    flagged = string(bc.region(abs(formula - reported) >= 1e-9));
    verifyEqual(testCase, sort(flagged), sort(["東京"; "中部"]));
end
end

function testCanonicalWorkbookDerivedInputTableIntegrity(testCase)
root = projectRoot(); reported = csvTable(fullfile(root, 'data', 'derived', 'canonical_final_workbook', 'as_reported_240.csv'));
verifyEqual(testCase, height(reported), 240);
verifyEqual(testCase, numel(unique(strcat(string(reported.scenario), "|", reported.region))), 240);
verifyTrue(testCase, all(strlength(reported.source_cell_gross) > 0));
end

function testCase4Discrepancy(testCase)
root = projectRoot(); results = run_tanaka_reproduction(); reported = csvTable(fullfile(root, 'data', 'derived', 'canonical_final_workbook', 'as_reported_240.csv'));
for region = ["北陸", "中部"]
    r4 = results.gross_RE_requirement_TWh(results.scenario == 4 & results.region == region);
    r6 = results.gross_RE_requirement_TWh(results.scenario == 6 & results.region == region);
    p4 = reported.gross_RE_requirement_TWh(reported.scenario == 4 & reported.region == region);
    verifyEqual(testCase, r4, r6, 'AbsTol', 1.1e-6);
    verifyGreaterThan(testCase, abs(r4 - p4), 1.1e-6);
end
end

function testCases13To15UnresolvedClassification(testCase)
root = projectRoot(); audit = csvTable(fullfile(root, 'results', 'source_cell_audit.csv'));
unresolved = audit(strcmp(audit.classification, "unresolved_source_or_formula_inconsistency"), :);
verifyEqual(testCase, height(unresolved), 6);
verifyTrue(testCase, all(strcmp(unresolved.evidence_status, "source_cell_identified_formula_unavailable")));
verifyTrue(testCase, all(ismember(unresolved.scenario, [13; 14; 15])));
end

function testCanonicalAndAlternateInputsSeparated(testCase)
root = projectRoot(); regional = csvTable(fullfile(root, 'config', 'regional_demand_and_existing_RE.csv')); nuclear = csvTable(fullfile(root, 'config', 'nuclear_scenarios.csv'));
verifyTrue(testCase, all(contains(regional.canonical_source_basis, "Final Chapter 4 workbook")));
verifyFalse(testCase, any(contains(lower(nuclear.source_basis), "alternate")));
end

function testPublishedCase6AndCase20Benchmarks(testCase)
projectRoot(); results = run_tanaka_reproduction();
case6 = sum(results.positive_additional_RE_TWh(results.scenario == 6));
case20 = sum(results.positive_additional_RE_TWh(results.scenario == 20));
verifyEqual(testCase, case6, 388.402687, 'AbsTol', 1e-6);
verifyEqual(testCase, case20, 148.896509, 'AbsTol', 1e-6);
end

function root = projectRoot()
root = fileparts(fileparts(mfilename('fullpath')));
addpath(fullfile(root, 'src', 'matlab'));
end

function tableOut = csvTable(path)
tableOut = readtable(path, 'TextType', 'string', 'Encoding', 'UTF-8', 'Delimiter', ',');
end
