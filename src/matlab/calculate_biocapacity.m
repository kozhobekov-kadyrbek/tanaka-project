function [bc_total_gha, national_bc_gha] = calculate_biocapacity(regional_bc)
%CALCULATE_BIOCAPACITY Sum the four land classes used by Tanaka (gha).
% Fishing grounds and carbon uptake land are outside this regional allocation.
bc_total_gha = regional_bc.forest_gha + regional_bc.cropland_gha + ...
    regional_bc.grazing_gha + regional_bc.built_up_gha;
national_bc_gha = sum(bc_total_gha);
end
