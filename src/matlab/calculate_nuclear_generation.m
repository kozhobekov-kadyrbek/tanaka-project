function nuclear_twh = calculate_nuclear_generation(equivalent_capacity_mw, hours_per_year, capacity_factor)
%CALCULATE_NUCLEAR_GENERATION Convert MW capacity to annual TWh.
nuclear_twh = equivalent_capacity_mw .* hours_per_year .* capacity_factor ./ 1e6;
end
