from vector import dot
from vector import magnitud
from vector import distance
from vector import scalar_multiply
from functools import partial

def shape(A):
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0
    return num_rows, num_cols

def get_row(A, i):
    return A[i]
    # A[i] is already the ith row
    
def get_column(A, j):
    return [A_i[j]
     # jth element of row A_i
    for A_i in A]
     # for each row A_i

def make_matrix(num_rows, num_cols, entry_fn):
    """returns a num_rows x num_cols matrix
    whose (i,j)th entry is entry_fn(i, j)"""
    return [[entry_fn(i, j)#given i create a list
        for j in range(num_cols)]#[entry_fn(i, 0), ... ]
       for i in range(num_rows)]#create one list for each i
       
def is_diagonal(i, j):
    """1's on the 'diagonal', 0's everywhere else"""
    return 1 if i == j else 0
# how to make an identity matrix 
identity_matrix = make_matrix(5, 5, is_diagonal)
# [[1, 0, 0, 0, 0],
# [0, 1, 0, 0, 0],
# [0, 0, 1, 0, 0],
# [0, 0, 0, 1, 0],
# [0, 0, 0, 0, 1]]
 
def matrix_product_entry(A, B, i, j):
    return dot(get_row(A, i), get_column(B, j))

def matrix_multiply(A, B):
    n1, k1 = shape(A)
    n2, k2 = shape(B)
    if k1 != n2:
        raise ArithmeticError("incompatible shapes!")         
    return make_matrix(n1, k2, partial(matrix_product_entry, A, B))

'''So we’ll need some helper functions to convert back and forth between the two repre‐
sentations:
v = [1, 2, 3]
v_as_matrix = [[1],
[2],
[3]]
'''   
def vector_as_matrix(v):
    """returns the vector v (represented as a list) as a n x 1 matrix"""
    return [[v_i] for v_i in v]

def vector_from_matrix(v_as_matrix):
    """returns the n x 1 matrix as a list of values"""
    return [row[0] for row in v_as_matrix]

def matrix_operate(A, v):
    v_as_matrix = vector_as_matrix(v)
    product = matrix_multiply(A, v_as_matrix)
    return vector_from_matrix(product)
'''
- we want to find guess in a way that
guess*A=A

Not all matrices of real numbers have eigenvectors and eigenvalues. For example the
matrix:
rotate = [[ 0, 1],
[-1, 0]]
rotates vectors 90 degrees clockwise, which means that the only vector it maps to a
scalar multiple of itself is a vector of zeroes. If you tried find_eigenvector(rotate)
it would run forever. Even matrices that have eigenvectors can sometimes get stuck in
cycles. Consider the matrix:
flip = [[0, 1],
[1, 0]]
This matrix maps any vector [x, y] to [y, x]. 
This means that, for example, [1, 1]
is an eigenvector with eigenvalue 1. 
However, if you start with a random vector with
unequal coordinates, find_eigenvector will just repeatedly swap the coordinates
forever. (Not-from-scratch libraries like NumPy use different methods that would
work in this case.) Nonetheless, when find_eigenvector does return a result, that
result is indeed an eigenvector.

'''
def find_eigenvector(A, tolerance=0.00001):
    guess = [1 for __ in A]

    while True:
        result = matrix_operate(A, guess)
        length = magnitude(result)
        next_guess = scalar_multiply(1/length, result)
        
        if distance(guess, next_guess) < tolerance:
            return next_guess, length # eigenvector, eigenvalue
        
        guess = next_guess
        
