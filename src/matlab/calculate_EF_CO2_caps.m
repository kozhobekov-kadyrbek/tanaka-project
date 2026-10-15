function [formula_caps_mt, canonical_caps_mt] = calculate_EF_CO2_caps(bc_total_gha, national_cap_mt, reported_caps_mt)
%CALCULATE_EF_CO2_CAPS Apply C_j = C_nat * BC_j / sum(BC).
% The final workbook's published regional cap inputs are returned separately.
formula_caps_mt = national_cap_mt .* bc_total_gha ./ sum(bc_total_gha);
canonical_caps_mt = reported_caps_mt;
end
