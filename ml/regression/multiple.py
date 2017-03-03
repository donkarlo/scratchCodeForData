#beta = [alpha, beta_1, ..., beta_k]
#x_i = [1, x_i1, ..., x_ik]

def predict(x_i, beta):
    """assumes that the first element of each x_i is 1"""
    return dot(x_i, beta)

#[1, # constant term
#49, # number of friends
#4, # work hours per day
#0] # doesn't have PhD
def error(x_i, y_i, beta):
    return y_i - predict(x_i, beta)

def squared_error(x_i, y_i, beta):
    return error(x_i, y_i, beta) ** 2

def squared_error_gradient(x_i, y_i, beta):
    """the gradient (with respect to beta)
    corresponding to the ith squared error term"""
    return [-2 * x_ij * error(x_i, y_i, beta)
        for x_ij in x_i]
'''
x is something like [1,12,44,...] and y is just scalar
for the above example it returns # [30.63, 0.972, -1.868, 0.911]
'''            
def estimate_beta(x, y):
    beta_initial = [random.random() for x_i in x[0]]
    return minimize_stochastic(squared_error,
                                squared_error_gradient,
                                x, y,
                                beta_initial,
                                0.001)
                                random.seed(0)
                                beta = estimate_beta(x, daily_minutes_good) # [30.63, 0.972, -1.868, 0.911]

"""goodness of the fit"""
def multiple_r_squared(x, y, beta):
    sum_of_squared_errors = sum(error(x_i, y_i, beta) ** 2
    for x_i, y_i in zip(x, y))
        return 1.0 - sum_of_squared_errors / total_sum_of_squares(y)
"""
sample is a list of pairs (x_i, y_i)
in which x_i is a vecor like [1,54,554,...] and y_i is a scalar
and zip(*sample), reversly unsew the data in it    
"""
def estimate_sample_beta(sample):
    x_sample, y_sample = zip(*sample) # magic unzipping trick
    return estimate_beta(x_sample, y_sample)
    
'''Testing the goodness of the fit'''
random.seed(0) # so that you get the same results as me
bootstrap_betas = bootstrap_statistic(zip(x, daily_minutes_good),
                                        estimate_sample_beta,
                                        100)
bootstrap_standard_errors = [
    standard_deviation([beta[i] for beta in bootstrap_betas])
    for i in range(4)]
# [1.174, # constant term, actual error = 1.19
# 0.079, # num_friends, actual error = 0.080
# 0.131, # unemployed, actual error = 0.127
# 0.990] # phd, actual error = 0.998

#Standard Errors of Regression Coefficients   
def p_value(beta_hat_j, sigma_hat_j):
    if beta_hat_j > 0:
        # if the coefficient is positive, we need to compute twice the
        # probability of seeing an even *larger* value
        return 2 * (1 - normal_cdf(beta_hat_j / sigma_hat_j))
    else:
        # otherwise twice the probability of seeing a *smaller* value
        return 2 * normal_cdf(beta_hat_j / sigma_hat_j)

p_value(30.63, 1.174) # ~0 (constant term)
p_value(0.972, 0.079) # ~0 (num_friends)
p_value(-1.868, 0.131) # ~0 (work_hours)
p_value(0.911, 0.990) # 0.36 (phd)

#rugularization- ridge regression
# alpha is a *hyperparameter* controlling how harsh the penalty is
# sometimes it's called "lambda" but that already means something in Python
def ridge_penalty(beta, alpha):
    return alpha * dot(beta[1:], beta[1:])
    
def squared_error_ridge(x_i, y_i, beta, alpha):
    """estimate error plus ridge penalty on beta"""
    return error(x_i, y_i, beta) ** 2 + ridge_penalty(beta, alpha)
    
def ridge_penalty_gradient(beta, alpha):
    """gradient of just the ridge penalty"""
    return [0] + [2 * alpha * beta_j for beta_j in beta[1:]]
    
def squared_error_ridge_gradient(x_i, y_i, beta, alpha):
    """the gradient corresponding to the ith squared error term
    including the ridge penalty"""
    return vector_add(squared_error_gradient(x_i, y_i, beta),
                      ridge_penalty_gradient(beta, alpha))
def estimate_beta_ridge(x, y, alpha):
    """use gradient descent to fit a ridge regression
    with penalty alpha"""
    beta_initial = [random.random() for x_i in x[0]]
    return minimize_stochastic(partial(squared_error_ridge, alpha=alpha),
                                partial(squared_error_ridge_gradient,
                                alpha=alpha),
                                x, y,
                                beta_initial,
                                0.001)

random.seed(0)
beta_0 = estimate_beta_ridge(x, daily_minutes_good, alpha=0.0)
# [30.6, 0.97, -1.87, 0.91]
dot(beta_0[1:], beta_0[1:]) # 5.26
multiple_r_squared(x, daily_minutes_good, beta_0) # 0.680

beta_0_01 = estimate_beta_ridge(x, daily_minutes_good, alpha=0.01)
# [30.6, 0.97, -1.86, 0.89]
dot(beta_0_01[1:], beta_0_01[1:]) # 5.19
multiple_r_squared(x, daily_minutes_good, beta_0_01) # 0.680
beta_0_1 = estimate_beta_ridge(x, daily_minutes_good, alpha=0.1)
# [30.8, 0.95, -1.84, 0.54]
dot(beta_0_1[1:], beta_0_1[1:]) # 4.60
multiple_r_squared(x, daily_minutes_good, beta_0_1) # 0.680
beta_1 = estimate_beta_ridge(x, daily_minutes_good, alpha=1)
# [30.7, 0.90, -1.69, 0.085]
dot(beta_1[1:], beta_1[1:]) # 3.69
multiple_r_squared(x, daily_minutes_good, beta_1) # 0.676
beta_10 = estimate_beta_ridge(x, daily_minutes_good, alpha=10)
# [28.3, 0.72, -0.91, -0.017]
dot(beta_10[1:], beta_10[1:]) # 1.36
multiple_r_squared(x, daily_minutes_good, beta_10)
 # 0.573
'''lasso regularization'''
def lasso_penalty(beta, alpha):
    return alpha * sum(abs(beta_i) for beta_i in beta[1:])


