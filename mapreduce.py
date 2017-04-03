from __future__ import division
import math, random, re, datetime
from collections import defaultdict, Counter
from functools import partial
from naive_bayes import tokenize

def word_count_old(documents):
    """word count not using MapReduce"""
    return Counter(word 
        for document in documents 
        for word in tokenize(document))

'''
Imagine we have a collection of items we’d like to process somehow. For instance, the
items might be website logs, the texts of various books, image files, or anything else.
A basic version of the MapReduce algorithm consists of the following steps:
1. Use a mapper function to turn each item into zero or more key-value pairs.
(Often this is called the map function, but there is already a Python function
called map and we don’t need to confuse the two.)
2. Collect together all the pairs with identical keys.
3. Use a reducer function on each collection of grouped values to produce output
values for the corresponding key.
'''

'''
First, we need a function that turns a document into a sequence of key-value pairs.
We’ll want our output to be grouped by word, which means that the keys should be
words. And for each word, we’ll just emit the value 1 to indicate that this pair corre‐
sponds to one occurrence of the word:

First, we need a function that turns a document into a sequence of key-value pairs.
We’ll want our output to be grouped by word, which means that the keys should be
words. And for each word, we’ll just emit the value 1 to indicate that this pair corre‐
sponds to one occurrence of the word:'''
def wc_mapper(document):
    """for each word in the document, emit (word,1)"""        
    for word in tokenize(document):
        yield (word, 1)

'''
Skipping the “plumbing” step 2 for the moment, imagine that for some word we’ve
collected a list of the corresponding counts we emitted. Then to produce the overall
count for that word we just need:
'''
def wc_reducer(word, counts):
    """sum up the counts for a word"""
    yield (word, sum(counts))

'''Returning to step 2, we now need to collect 
the results from wc_mapper and feed them
to wc_reducer. Let’s think about how we would do 
this on just one computer:

Imagine that we have three documents ["data science", "big data", "science
fiction"].
Then wc_mapper applied to the first document yields the two pairs ("data", 1) and
("science", 1). After we’ve gone through all three documents, the collector con‐
tains
{ "data" : [1, 1],
"science" : [1, 1],
"big" : [1],
"fiction" : [1] }
Then wc_reducer produces the count for each word:
[("data", 2), ("science", 2), ("big", 1), ("fiction", 1)]
'''
def word_count(documents):
    """count the words in the input documents using MapReduce"""

    # place to store grouped values
    collector = defaultdict(list) 

    for document in documents:
        for word, count in wc_mapper(document):
            collector[word].append(count)

    return [output
            for word, counts in collector.iteritems()
            for output in wc_reducer(word, counts)]



wc_mapper_results = [result 
                     for document in documents
                     for result in wc_mapper(document)]
'''
MapReduce More Generally
If you think about it for a minute, all of the word-count-specific code in the previous
example is contained in the wc_mapper and wc_reducer functions. This means that
with a couple of changes we have a much more general framework (that still runs on
a single machine):
'''
def map_reduce(inputs, mapper, reducer):
    """runs MapReduce on the inputs using mapper and reducer"""
    collector = defaultdict(list)

    for input in inputs:
        for key, value in mapper(input):
            collector[key].append(value)

    return [output
            for key, values in collector.iteritems()
            for output in reducer(key,values)]
''' And then we can count words simply by using:
'''
word_counts = map_reduce(documents, wc_mapper, wc_reducer)
'''Before we proceed, observe that wc_reducer is just summing the values correspond‐
ing to each key. This kind of aggregation is common enough that it’s worth abstract‐
ing it out:
'''
def reduce_with(aggregation_fn, key, values):
    """reduces a key-values pair by applying aggregation_fn to the values"""
    yield (key, aggregation_fn(values))

def values_reducer(aggregation_fn):
    """turns a function (values -> output) into a reducer"""
    return partial(reduce_with, aggregation_fn)

sum_reducer = values_reducer(sum)
max_reducer = values_reducer(max)
min_reducer = values_reducer(min)
count_distinct_reducer = values_reducer(lambda values: len(set(values)))


'''
Sample of analysing the status
'''
status_updates = [
    {"id": 1, 
     "username" : "joelgrus", 
     "text" : "Is anyone interested in a data science book?",
     "created_at" : datetime.datetime(2013, 12, 21, 11, 47, 0),
     "liked_by" : ["data_guy", "data_gal", "bill"] },
    # add your own
]
'''
Let’s say we need to figure out which day of 
the week people talk the most about data
science. In order to find this, we’ll just 
count how many data science updates there are
on each day of the week. This means we’ll need 
to group by the day of week, so that’s
our key. And if we emit a value of 1 for each 
update that contains “data science,” we
can simply get the total number using sum:
'''
def data_science_day_mapper(status_update):
    """yields (day_of_week, 1) if status_update contains "data science" """
    if "data science" in status_update["text"].lower():
        day_of_week = status_update["created_at"].weekday()
        yield (day_of_week, 1)
        
data_science_days = map_reduce(status_updates, 
                               data_science_day_mapper, 
                               sum_reducer)
'''As a slightly more complicated example, imagine we need to find out for each user
the most common word that she puts in her status updates. There are three possible
approaches that spring to mind for the mapper:
• Put the username in the key; put the words and counts in the values.
• Put the word in key; put the usernames and counts in the values.
• Put the username and word in the key; put the counts in the values.
If you think about it a bit more, we definitely want to group by username, because we
want to consider each person’s words separately. And we don’t want to group by word,
since our reducer will need to see all the words for each person to find out which is
the most popular. This means that the first option is the right choice:
'''
def words_per_user_mapper(status_update):
    user = status_update["username"]
    for word in tokenize(status_update["text"]):
        yield (user, (word, 1))
            
def most_popular_word_reducer(user, words_and_counts):
    """given a sequence of (word, count) pairs, 
    return the word with the highest total count"""
    
    word_counts = Counter()
    for word, count in words_and_counts:
        word_counts[word] += count

    word, count = word_counts.most_common(1)[0]
                       
    yield (user, (word, count))

user_words = map_reduce(status_updates,
                        words_per_user_mapper, 
                        most_popular_word_reducer)
'''Or we could find out the number of distinct status-likers for each user:
'''
def liker_mapper(status_update):
    user = status_update["username"]
    for liker in status_update["liked_by"]:
        yield (user, liker)
                
distinct_likers_per_user = map_reduce(status_updates, 
                                      liker_mapper, 
                                      count_distinct_reducer)


'''
Recall from “Matrix Multiplication” on page 260 that given a m × n matrix A and a
n × k matrix B, we can multiply them to form a m × k matrix C, where the element of
C in row i and column j is given by:
Ci j = Ai1B1 j + Ai2B2 j + ... + AinBn j
As we’ve seen, a “natural” way to represent a m × n matrix is with a list of lists,
where the element Ai j is the jth element of the ith list.
But large matrices are sometimes sparse, which means that most of their elements
equal zero. For large sparse matrices, a list of lists can be a very wasteful representa‐
tion. A more compact representation is a list of tuples (name, i, j, value) where
name identifies the matrix, and where i, j, value indicates a location with nonzero
value.
For example, a billion × billion matrix has a quintillion entries, which would not be
easy to store on a computer. But if there are only a few nonzero entries in each row,
this alternative representation is many orders of magnitude smaller.

Given this sort of representation, it turns out that we can use MapReduce to perform
matrix multiplication in a distributed manner.
To motivate our algorithm, notice that each element Ai j is only used to compute the
elements of C in row i, and each element Bi j is only used to compute the elements of
C in column j. Our goal will be for each output of our reducer to be a single entry of
C, which means we’ll need our mapper to emit keys identifying a single entry of C.
This suggests the following:

'''
def matrix_multiply_mapper(m, element):
    """m is the common dimension (columns of A, rows of B)
    element is a tuple (matrix_name, i, j, value)"""
    matrix, i, j, value = element

    if matrix == "A":
        for column in range(m):
            # A_ij is the jth entry in the sum for each C_i_column
            yield((i, column), (j, value))
    else:
        for row in range(m):
            # B_ij is the ith entry in the sum for each C_row_j
            yield((row, j), (i, value))
     
def matrix_multiply_reducer(m, key, indexed_values):
    results_by_index = defaultdict(list)
    for index, value in indexed_values:
        results_by_index[index].append(value)

    # sum up all the products of the positions with two results
    sum_product = sum(results[0] * results[1]
                      for results in results_by_index.values()
                      if len(results) == 2)
                      
    if sum_product != 0.0:
        yield (key, sum_product)
        
entries = [("A", 0, 0, 3), ("A", 0, 1,  2),
           ("B", 0, 0, 4), ("B", 0, 1, -1), ("B", 1, 0, 10)]
    mapper = partial(matrix_multiply_mapper, 3)
    reducer = partial(matrix_multiply_reducer, 3)

    print "map-reduce matrix multiplication"
    print "entries:", entries
    print "result:", map_reduce(entries, mapper, reducer)        

    