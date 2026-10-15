function results = run_tanaka_reproduction()
%RUN_TANAKA_REPRODUCTION Reproduce the annual Chapter 4 accounting in MATLAB.
% The output is diagnostic_corrected and leaves the historical workbook-derived
% values in data/derived/canonical_final_workbook/as_reported_240.csv untouched.
this_file = mfilename('fullpath');
root = fileparts(fileparts(fileparts(this_file)));
cfg = fullfile(root, 'config');
derived = fullfile(root, 'data', 'derived', 'canonical_final_workbook');
outdir = fullfile(root, 'results');
if ~isfolder(outdir), mkdir(outdir); end

csvopts = {'TextType', 'string', 'Encoding', 'UTF-8', 'Delimiter', ','};
scenarios = readtable(fullfile(cfg, 'scenario_definitions.csv'), csvopts{:});
regional = readtable(fullfile(cfg, 'regional_demand_and_existing_RE.csv'), csvopts{:});
bc = readtable(fullfile(cfg, 'EF_and_biocapacity_assumptions.csv'), csvopts{:});
shares = readtable(fullfile(cfg, 'thermal_fuel_shares.csv'), csvopts{:});
nuclear = readtable(fullfile(cfg, 'nuclear_scenarios.csv'), csvopts{:});
factors_t = readtable(fullfile(cfg, 'fossil_emission_factors.csv'), csvopts{:});
reported = readtable(fullfile(derived, 'as_reported_240.csv'), csvopts{:});
factors = factors_t.g_co2_per_kwh';
[bc_total, ~] = calculate_biocapacity(bc);

n = height(scenarios) * height(regional);
scenario_out = zeros(n,1); ef_out = strings(n,1); thermal_case_out = strings(n,1);
nuclear_case_out = strings(n,1); region_out = strings(n,1); cap_out = zeros(n,1);
thermal_out = zeros(n,1); nuclear_out = zeros(n,1); gross_out = zeros(n,1);
existing_out = zeros(n,1); signed_out = zeros(n,1); positive_out = zeros(n,1);
energy_residual_out = zeros(n,1); reported_gross_out = zeros(n,1); delta_out = zeros(n,1);
idx = 0;
for s = 1:height(scenarios)
    ef_case = scenarios.ef_case(s);
    cap_column = 'carbon_only_cap_mt';
    if ef_case == "carbon_and_food", cap_column = 'carbon_and_food_cap_mt'; end
    national_cap = sum(bc.(cap_column));
    [formula_caps, canonical_caps] = calculate_EF_CO2_caps(bc_total, national_cap, bc.(cap_column)); %#ok<ASGLU>
    for j = 1:height(regional)
        idx = idx + 1;
        region = regional.region(j);
        share_row = find(shares.region == region & shares.thermal_case == scenarios.thermal_case(s), 1);
        if isempty(share_row), share_row = find(shares.region == "all" & shares.thermal_case == scenarios.thermal_case(s), 1); end
        raw = [shares.coal_share(share_row), shares.lng_share(share_row), shares.oil_share(share_row)];
        [thermal, ~, ~] = calculate_thermal_generation(canonical_caps(j), raw, factors);
        nuc_row = find(nuclear.region == region & nuclear.nuclear_case == scenarios.nuclear_case(s), 1);
        nuc = calculate_nuclear_generation(nuclear.equivalent_capacity_mw(nuc_row), nuclear.hours_per_year(nuc_row), nuclear.capacity_factor(nuc_row));
        [gross, signed, positive] = calculate_RE_residual(regional.demand_twh(j), thermal, nuc, regional.existing_plus_fit_re_twh(j));
        report_row = find(reported.scenario == scenarios.scenario(s) & reported.region == region, 1);
        scenario_out(idx) = scenarios.scenario(s); ef_out(idx) = ef_case; thermal_case_out(idx) = scenarios.thermal_case(s);
        nuclear_case_out(idx) = scenarios.nuclear_case(s); region_out(idx) = region; cap_out(idx) = canonical_caps(j);
        thermal_out(idx) = thermal; nuclear_out(idx) = nuc; gross_out(idx) = gross; existing_out(idx) = regional.existing_plus_fit_re_twh(j);
        signed_out(idx) = signed; positive_out(idx) = positive; energy_residual_out(idx) = regional.demand_twh(j)-thermal-nuc-gross;
        reported_gross_out(idx) = reported.gross_RE_requirement_TWh(report_row); delta_out(idx) = gross-reported_gross_out(idx);
    end
end
results = table(scenario_out, ef_out, thermal_case_out, nuclear_case_out, region_out, cap_out, thermal_out, nuclear_out, gross_out, existing_out, signed_out, positive_out, energy_residual_out, reported_gross_out, delta_out, ...
    'VariableNames', {'scenario','EF_case','thermal_case','nuclear_case','region','allocated_CO2_cap_Mt','thermal_generation_TWh','nuclear_generation_TWh','gross_RE_requirement_TWh','assumed_existing_plus_FIT_RE_TWh','signed_net_RE_shortfall_TWh','positive_additional_RE_TWh','annual_energy_identity_residual_TWh','as_reported_gross_RE_requirement_TWh','gross_delta_diagnostic_minus_reported_TWh'});
writetable(results, fullfile(outdir, 'matlab_annual_accounting_results.csv'), 'Encoding', 'UTF-8');
end
