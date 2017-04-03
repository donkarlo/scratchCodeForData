from __future__ import division
from collections import Counter
from functools import partial
from linear_algebra import dot
import math, random
import matplotlib
import matplotlib.pyplot as plt

def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))
def step_function(x):
    return 1 if x >= 0 else 0

def perceptron_output(weights, bias, x):
    """returns 1 if the perceptron 'fires', 0 if not"""
    calculation = dot(weights, x) + bias
    return step_function(calculation)

def sigmoid(t):
    return 1 / (1 + math.exp(-t))
'''
@param weights=[2,4,1,...,45]->the last element, 45, is the bias
be careful, weights could be like [[],[],...] as well

@param inputs is something like [1,4,..,1] the last element 
must be 1 to reproduce
bias when multiplied by weights' last element
'''
def neuron_output(weights, inputs):
    return sigmoid(dot(weights, inputs))

'''
takes in a neural network
    (represented as a list of lists of lists of weights)
    and returns the output from forward-propagating the input
-@param neural_network a list like [[[],[],...,[]],[[]]]
    a sample is like 
    xor_network = [
    [[20, 20, -30],
        [20, 20, -10]],
    [[-60, 60, -30]]]
-@param input_vector [0,0,1,...] like [0,1]
-@return [[w_1,w_2],[output]]
like [[4.5397868702434395e-05, 0.9999546021312976], [0.9999999999999059]]
or
[[0.9999546021312976, 0.9999999999999065], [9.383146683006828e-14]]
'''
def feed_forward(neural_network, input_vector):   
    outputs = []
    # process one layer at a time
    for layer in neural_network:
        input_with_bias = input_vector + [1]# add a bias input
        '''
        - compute the output
        - Now go over the neurons of a  single layer and produce
        a single number near to 1 or 0
        '''
        output = [neuron_output(neuron, input_with_bias)
            for neuron in layer]# for each neuron
        outputs.append(output)# and remember it
        # then the input to the next layer is the output of this one
        input_vector = output
        
    return outputs

xor_network = [
        # hidden layer, a layer with two neurons
        [
            [20, 20, -30]# 'and' neuron
            ,[20, 20, -10]# 'or' neuron
        ],
        # output layer, as the last layer
        [
            [-60, 60, -30]
        ]
    ]# '2nd input but not 1st input' neuron, I dont understand this
    
for x in [0, 1]:
    for y in [0, 1]:
        # feed_forward produces the outputs of every neuron
        # feed_forward[-1] is the outputs of the output-layer neurons
        print x, y, feed_forward(xor_network,[x, y])
#     0 0 [9.38314668300676e-14]
#     0 1 [0.9999999999999059]
#     1 0 [0.9999999999999059]
#     1 1 [9.383146683006828e-14]

'''
- The book's code is wrong, this code is springed from 
the book's github page
- You have to run this code in a loop for some 
hundreds or thousands of time
to get a good estimation of neuron weights
@param network is a network with arbitrary weights. 
this function just works with a neural network with a SINGLE 
hidden layer
@param input_vector is the training input vector. A list like
[scalar_1,sclalar_2,...] or better to say a list of scalars
@param target is the same as input_vector in schema. a list like
[scalar_1,sclalar_2,...] or better to say a list of scalars
@return the network weight will refined and 
network will be interpreted as a sent by refrence
'''     
def backpropagate(network, input_vector, target):

    hidden_outputs, outputs = feed_forward(network, input_vector)
    
    '''the output * (1 - output) is from the derivative of sigmoid'''
    output_deltas = [output * (1 - output) * (output - target[i])
                     for i, output in enumerate(outputs)]
                     
    '''adjust weights for output layer (network[-1])'''
    for i, output_neuron in enumerate(network[-1]):
        '''focus on the ith output layer neuron'''
        for j, hidden_output in enumerate(hidden_outputs + [1]):
            '''-adjust the jth weight based on both
            this neuron's delta and its jth input'''
            output_neuron[j] = output_neuron[j] - output_deltas[i] * hidden_output

    '''back-propagate errors to hidden layer'''
    hidden_deltas = [hidden_output * (1 - hidden_output) * 
                      dot(output_deltas, [n[i] for n in network[-1]]) 
                     for i, hidden_output in enumerate(hidden_outputs)]

    '''adjust weights for hidden layer (network[0])'''
    for i, hidden_neuron in enumerate(network[0]):
        for j, input in enumerate(input_vector + [1]):
            hidden_neuron[j] = hidden_neuron[j] - hidden_deltas[i] * input

"""return a matplotlib 'patch' object with the specified
location, crosshatch pattern, and color"""            
def patch(x, y, hatch, color):
    return matplotlib.patches.Rectangle((x - 0.5, y - 0.5), 1, 1,
                                        hatch=hatch, fill=False, color=color)


def show_weights(neuron_idx):
    weights = network[0][neuron_idx]
    abs_weights = map(abs, weights)

    grid = [abs_weights[row:(row+5)] # turn the weights into a 5x5 grid
            for row in range(0,25,5)] # [weights[0:5], ..., weights[20:25]]

    ax = plt.gca() # to use hatching, we'll need the axis

    ax.imshow(grid, # here same as plt.imshow
              cmap=matplotlib.cm.binary, # use white-black color scale
              interpolation='none') # plot blocks as blocks

    # cross-hatch the negative weights
    for i in range(5): # row
        for j in range(5): # column
            if weights[5*i + j] < 0: # row i, column j = weights[5*i + j]
                # add black and white hatches, so visible whether dark or light
                ax.add_patch(patch(j, i, '/', "white"))
                ax.add_patch(patch(j, i, '\\', "black"))
    plt.show()

if __name__ == "__main__":

    raw_digits = [
          """11111
             1...1
             1...1
             1...1
             11111""",
             
          """..1..
             ..1..
             ..1..
             ..1..
             ..1..""",
             
          """11111
             ....1
             11111
             1....
             11111""",
             
          """11111
             ....1
             11111
             ....1
             11111""",     
             
          """1...1
             1...1
             11111
             ....1
             ....1""",             
             
          """11111
             1....
             11111
             ....1
             11111""",   
             
          """11111
             1....
             11111
             1...1
             11111""",             

          """11111
             ....1
             ....1
             ....1
             ....1""",
             
          """11111
             1...1
             11111
             1...1
             11111""",    
             
          """11111
             1...1
             11111
             ....1
             11111"""]     

    def make_digit(raw_digit):
        return [1 if c == '1' else 0
                for row in raw_digit.split("\n")
                for c in row.strip()]
                
    inputs = map(make_digit, raw_digits)
'''check the comments on output size comments'''
    targets = [[1 if i == j else 0 for i in range(10)]
               for j in range(10)]

    random.seed(0)   # to get repeatable results
    input_size = 25  # each input is a vector of length 25
    num_hidden = 5   # we'll have 5 neurons in the hidden layer
    
'''We’ll want our output to indicate which digit the neural network thinks it is, so we’ll
need 10 outputs. The correct output for digit 4, for instance, will be:
'''    
    output_size = 10 # we need 10 outputs for each input

    # each hidden neuron has one weight per input, plus a bias weight
    '''a list of 5 lists each is bearing 26 scalars of
    random numbers between 0 and 1 as the weights  
    '''
    hidden_layer = [[random.random() for __ in range(input_size + 1)]
                    for __ in range(num_hidden)]

    '''-each output neuron has one weight 
    per hidden neuron, plus a bias weight
-     list of 10 lists each having 6 scalars 
of numbers between 0 and 1
    '''
    output_layer = [[random.random() for __ in range(num_hidden + 1)]
                    for __ in range(output_size)]

    # the network starts out with random weights
    network = [hidden_layer, output_layer]

    # 10,000 iterations seems enough to converge
    for __ in range(10000):
        for input_vector, target_vector in zip(inputs, targets):
            backpropagate(network, input_vector, target_vector)

    def predict(input):
        return feed_forward(network, input)[-1]

    for i, input in enumerate(inputs):
        outputs = predict(input)
        print i, [round(p,2) for p in outputs]

    print """.@@@.
...@@
..@@.
...@@
.@@@."""
    print [round(x, 2) for x in
          predict(  [0,1,1,1,0,  # .@@@.
                     0,0,0,1,1,  # ...@@
                     0,0,1,1,0,  # ..@@.
                     0,0,0,1,1,  # ...@@
                     0,1,1,1,0]) # .@@@.
          ]
    print

    print """.@@@.
@..@@
.@@@.
@..@@
.@@@."""
    print [round(x, 2) for x in 
          predict(  [0,1,1,1,0,  # .@@@.
                     1,0,0,1,1,  # @..@@
                     0,1,1,1,0,  # .@@@.
                     1,0,0,1,1,  # @..@@
                     0,1,1,1,0]) # .@@@.
          ]
    print