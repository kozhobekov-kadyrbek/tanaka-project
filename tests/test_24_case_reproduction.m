function tests = test_24_case_reproduction
tests = functiontests(localfunctions);
end

function testAnnualResults(testCase)
results = run_tanaka_reproduction();
verifyEqual(testCase, height(results), 240);
verifyLessThan(testCase, max(abs(results.annual_energy_identity_residual_TWh)), 1e-10);
verifyEqual(testCase, sum(results.positive_additional_RE_TWh(results.scenario == 6)), 388.402687, 'AbsTol', 2e-6);
verifyEqual(testCase, sum(results.positive_additional_RE_TWh(results.scenario == 20)), 148.900000, 'AbsTol', 1e-2);
end
