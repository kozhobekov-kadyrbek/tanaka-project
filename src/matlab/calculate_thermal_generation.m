function [thermal_twh, weighted_ef, weights] = calculate_thermal_generation(cap_mt, raw_shares, factors)
%CALCULATE_THERMAL_GENERATION Annual thermal TWh permitted by the CO2 cap.
% factors are [coal LNG oil] in gCO2/kWh. Shares are normalized within fossil
% generation because source 2016 shares do not sum to one across all electricity.
if sum(raw_shares) == 0
    weights = [0 0 0]; weighted_ef = 0; thermal_twh = 0; return
end
weights = raw_shares ./ sum(raw_shares);
weighted_ef = sum(weights .* factors);
% 1 Mt = 10^12 g and 1 TWh = 10^9 kWh.
thermal_twh = 1000 .* cap_mt ./ weighted_ef;
end
