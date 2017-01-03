from probabilities.distributions.discrete.binomial import * 
from probabilities.distributions.continuous.normal import * 
mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)
#lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)
#print lo,hi
#
#mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)
#type_2_probability = normal_probability_between(lo, hi, mu_1, sigma_1)
#print type_2_probability
print normal_two_sided_bounds(0.5, mu_0, sigma_0)

print normal_two_sided_bounds(0.95, mu_0, sigma_0)

print normal_two_sided_bounds(0.99, mu_0, sigma_0)
