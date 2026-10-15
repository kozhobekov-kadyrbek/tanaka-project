function [gross_re_twh, signed_shortfall_twh, positive_additional_twh] = calculate_RE_residual(demand_twh, thermal_twh, nuclear_twh, existing_re_twh)
%CALCULATE_RE_RESIDUAL Tanaka's annual energy-balance residual.
gross_re_twh = demand_twh - thermal_twh - nuclear_twh;
signed_shortfall_twh = gross_re_twh - existing_re_twh;
positive_additional_twh = max(0, signed_shortfall_twh);
end
