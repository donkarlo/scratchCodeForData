from linearAlgebra.vector import * 
def in_random_order(data):
    """generator that returns the elements of data in random order"""
    indexes = [i for i, _ in enumerate(data)] # create a list of indexes
    random.shuffle(indexes) # shuffle them
    for i in indexes:
        # return the data in that order
        yield data[i]
    
'''target_fn is the hypothesis function that guesses 
a value for xi using the parameters theta. it is function dependent on theta
vector
'''
def minimize_stochastic(target_fn, gradient_fn, x, y, theta_0, alpha_0=0.01):
    # the training data, x=(x1,...,xm) and y=(y1,...,ym)  
    #so data is ((x1,y1),...,(xm,ym))
    data = zip(x, y)
    # initial guess    
    theta = theta_0
    # initial step size
    alpha = alpha_0
    # the minimum so far
    min_theta, min_value = None, float("inf")
    iterations_with_no_improvement = 0
    
    # if we ever go 100 iterations with no improvement, stop
    while iterations_with_no_improvement < 100:
        value = sum( target_fn(x_i, y_i, theta) for x_i, y_i in data )
        if value < min_value:
            # if we've found a new minimum, remember it
            # and go back to the original step size
            min_theta, min_value = theta, value
            iterations_with_no_improvement = 0
            alpha = alpha_0
        else:
            # otherwise we're not improving, so try shrinking the step size
            iterations_with_no_improvement += 1
            alpha *= 0.9
        # and take a gradient step for each of the data points
        for x_i, y_i in in_random_order(data):
            gradient_i = gradient_fn(x_i, y_i, theta)
            theta = vector_subtract(theta, scalar_multiply(alpha, gradient_i))
            return min_theta
  

def negate(f):
    """return a function that for any input x returns -f(x)"""
    return lambda *args, **kwargs: -f(*args, **kwargs)
    
def negate_all(f):
    """the same when f returns a list of numbers"""
    return lambda *args, **kwargs: [-y for y in f(*args, **kwargs)]
          
def maximize_stochastic(target_fn, gradient_fn, x, y, theta_0, alpha_0=0.01):
    return minimize_stochastic(negate(target_fn),
        negate_all(gradient_fn),
        x, y, theta_0, alpha_0)


