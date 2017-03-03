'''Assuming we’ve determined such an 
alpha and beta, then we make predictions simply with:'''
def predict(alpha, beta, x_i):
    return beta * x_i + alpha
    
'''How do we choose alpha and beta? Well, any choice of alpha and beta gives us a
predicted output for each input x_i. Since we know the actual output y_i we can
compute the error for each pair:
'''
def error(alpha, beta, x_i, y_i):
    """the error from predicting beta * x_i + alpha
    when the actual value is y_i"""
    return y_i - predict(alpha, beta, x_i)
    
'''What we’d really like to know is the total error over the entire data set. But we don’t
want to just add the errors—if the prediction for x_1 is too high and the prediction
for x_2 is too low, the errors may just cancel out.
So instead we add up the squared errors:
alpha and beta are the estimates and x and y are
our training dataset so x is a list(num of friends) like [3,5,2,...]
and y is a list of times spent like [30,21,41,...]
'''
def sum_of_squared_errors(alpha, beta, x, y):
    return sum(error(alpha, beta, x_i, y_i) ** 2
        for x_i, y_i in zip(x, y))

'''The least squares solution is to choose the alpha and beta that make
sum_of_squared_errors as small as possible.
Using calculus (or tedious algebra), the error-minimizing alpha and beta 
are given by:
'''
def least_squares_fit(x, y):
    """given training values for x and y,
    find the least-squares values of alpha and beta"""
    beta = correlation(x, y) * standard_deviation(y) / standard_deviation(x)
    alpha = mean(y) - beta * mean(x)
    return alpha, beta
    
'''Trying to findout how good our model is'''
def total_sum_of_squares(y):
    """the total squared variation of y_i's from their mean"""
    return sum(v ** 2 for v in de_mean(y))
    
def r_squared(alpha, beta, x, y):
    """the fraction of variation in y captured by the model, which equals
    1 - the fraction of variation in y not captured by the model"""
    return 1.0 - (sum_of_squared_errors(alpha, beta, x, y) /
        total_sum_of_squares(y))
        
'''Using Gradient Descent'''
def squared_error(x_i, y_i, theta):
    alpha, beta = theta
    return error(alpha, beta, x_i, y_i) ** 2
    
def squared_error_gradient(x_i, y_i, theta):
    alpha, beta = theta
    return [-2 * error(alpha, beta, x_i, y_i), # alpha partial derivative
        -2 * error(alpha, beta, x_i, y_i) * x_i] # beta partial derivative
        
'''choose random value to start'''
random.seed(0)
theta = [random.random(), random.random()]
alpha, beta = minimize_stochastic(squared_error,
                                    squared_error_gradient,
                                    num_friends_good,
                                    daily_minutes_good,
                                    theta,
                                    0.0001)


