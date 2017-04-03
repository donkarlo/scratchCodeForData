'''The gibs sampler'''
random.random()
inverse_normal_cdf(random.random())
def roll_a_die():
    return random.choice([1,2,3,4,5,6])

def direct_sample():
    d1 = roll_a_die()
    d2 = roll_a_die()
    return d1, d1 + d2

def random_y_given_x(x):
    """equally likely to be x + 1, x + 2, ... , x + 6"""
    return x + roll_a_die()

def random_x_given_y(y):
    if y <= 7:
        # if the total is 7 or less, the first die is equally likely to be
        # 1, 2, ..., (total - 1)
        return random.randrange(1, y)
    else:
        # if the total is 7 or more, the first die is equally likely to be
        # (total - 6), (total - 5), ..., 6
        return random.randrange(y - 6, 7)
'''
The way Gibbs sampling works is that we start with any (valid) 
value for x and y and
then repeatedly alternate replacing x with a random 
value picked conditional on y
and replacing y with a random value picked conditional 
on x. After a number of iterations, the resulting values 
of x and y will represent a sample from the unconditional
joint distribution:
'''
def gibbs_sample(num_iters=100):
    x, y = 1, 2 # doesn't really matter
    for _ in range(num_iters):
        x = random_x_given_y(y)
        y = random_y_given_x(x)
    return x, y
    
'''just a simple check to see if gibbs_sample works
as good as direct_sample
'''
def compare_distributions(num_samples=1000):
    counts = defaultdict(lambda: [0, 0])
    for _ in range(num_samples):
        counts[gibbs_sample()][0] += 1
        counts[direct_sample()][1] += 1
    return counts

'''
- each document is a list of unrwpeated words as
users’ interests, which look like 
documents=[
        ["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"],
        ["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres"],
        ...
]

- if they ask us to get a 4-topic out of given documents
we will end up a list of lists in each of which words
are sorted according to the weights they gained 
by that topic as a result of LDK that 
we will soon implement
[["java", "big data", "hadoop",...]
,["R","statistics","python",...]
,["hbase","postgres","mongo",...]
,["regression","libsvm","scikit-learn",...]]

- Having this, by just revieweing the results 
we will give each topic an arbitrary name according
let's say first 5 most weighted words out of each list
like:
topic_names = ["Big Data and programming languages",
"Python and statistics",
"databases",
"machine learning"]

- now by writing a quick code you can say that a user with intrests
like
['Hadoop', 'Big Data', 'HBase', 'Java', 'Spark', 'Storm', 'Cassandra']
wieght of interest for
Big Data and programming languages (topic 0)
is 4
and his weight of interest for databases (topic 2)
is 3

- So that the fifth word in the fourth document is:
documents[3][4]
and the topic from which that word was chosen is:
document_topics[3][4] in 
other words it holds the number of the topic 
(a number between 0 and k-1) to the 5th word
in 4th document considering that words are not repeating
in a single document. So for example the 5th word 
in 4th document is "java" and you 
hence trying to asign it 
a topic index in which programming language words are weighted 
the most. 

This very explicitly defines each document’s 
distribution over topics, and it implicitly
defines each topic’s distribution over words.


- Although these topics are just numbers,
 we can give them descriptive names by looking 
 at the words on which they put the heaviest weight. 
 
- We just have to somehow generate the document_topics. 
This is where Gibbs sampling comes into play.
We start by assigning every word in every document a topic 
completely at random.
Now we go through each document one word at a time.
 For that word and document,
we construct weights for each topic that depend 
on the (current) distribution of topics in that document 
and the (current) distribution of words for that topic. We then
use those weights to sample a new topic for that word. 
If we iterate this process many
times, we will end up with a joint sample from 
the topic-word distribution and the
document-topic distribution.

'''
documents=[
        ["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"],
        ["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres"],
        ["Python", "scikit-learn", "scipy", "numpy", "statsmodels", "pandas"],
        ["R", "Python", "statistics", "regression", "probability"],
        ["machine learning", "regression", "decision trees", "libsvm"],
        ["Python", "R", "Java", "C++", "Haskell", "programming languages"],
        ["statistics", "probability", "mathematics", "theory"],
        ["machine learning", "scikit-learn", "Mahout", "neural networks"],
        ["neural networks", "deep learning", "Big Data", "artificial intelligence"],
        ["Hadoop", "Java", "MapReduce", "Big Data"],
        ["statistics", "R", "statsmodels"],
        ["C++", "deep learning", "artificial intelligence", "probability"],
        ["pandas", "R", "Python"],
        ["databases", "HBase", "Postgres", "MySQL", "MongoDB"],
        ["libsvm", "regression", "support vector machines"]
]

'''
-To start with, we’ll need a function
 to randomly choose an index based 
 on an arbitrary set of weights:
- For instance, if you give it weights [1, 1, 3] 
then one-fifth(the fifth comes from 1+1+3=5 )
 of the time it will return
0, one-fifth of the time it will return 1, 
and three-fifths of the time it will return 2.
so the index of the topic that has more weight
acoording to word(j) in document(i) will be
return three times more.

@param list weights a list contains
the numbers representing the weight assigned 
each for each topic in each word in each document
or the each element of that list represent the
weight assigned to word i in document j for topic q

@return integer a random number between 0 to k-1
'''
def sample_from(weights):
    """returns i with probability weights[i] / sum(weights)"""
    total = sum(weights)
    rnd = total * random.random() # uniform between 0 and total
    for i, w in enumerate(weights):
        rnd -= w # return the smallest i such that
        if rnd <= 0: return i # weights[0] + ... + weights[i] >= rnd

'''we want k=4, later, after the word weights are generated we
will assign each a proper name like "programming languages"
,"databases", ...
'''

'''
In order to calculate the sampling weights, we’ll need to keep 
track of several counts.
Let’s first create the data structures for them.
'''
'''How many times each topic is assigned to each document:
-For example, once we populate these, we can find, for example, 
the number of words
in documents[3] associated with topic 1 as:
document_topic_counts[3][1]
- document_topic_counts by the end will look like 
 [{topic_0:counts_in_doc_1,topic_1:counts_in_doc_1,...}
 ,{topic_0:counts_in_doc_2,topic_1:counts_in_doc_2,...}
 ,...]
'''
# a list of Counters, one for each document
document_topic_counts = [Counter() for _ in documents]

'''How many times each word is assigned to each topic:
-We can find the number of times nlp is associated with topic 2 as:
topic_word_counts[2]["nlp"]
- [{word_0:count_of_word_0_for_topic_0,word_1:count_of_word_1_for_topic_0,...}
,{word_0:count_of_word_0_for_topic_1,word_1:count_of_word_1_for_topic_1,...}
,...
,{word_0:count_of_word_0_for_topic_k,word_1:count_of_word_1_for_topic_k,...}]
'''
# a list of Counters, one for each topic
topic_word_counts = [Counter() for _ in range(K)]

'''The total number of words assigned to each topic:'''
# a list of numbers, one for each topic
topic_counts = [0 for _ in range(K)]


'''The total number of words contained in each document:'''
# a list of numbers, one for each document
document_lengths = map(len, documents)

'''The number of distinct words:'''
distinct_words = set(word 
                        for document in documents 
                            for word in document)
W = len(distinct_words)

'''And the number of documents:
'''
D = len(documents)

'''
- Now we’re ready to define our conditional 
probability functions. As in Chapter 13,
each has a smoothing term that ensures 
every topic has a nonzero chance of being
chosen in any document and that every 
word has a nonzero chance of being chosen
for any topic:
'''
def p_topic_given_document(topic, d, alpha=0.1):
    """the fraction of words in document _d_
    that are assigned to _topic_ (plus some smoothing)"""
    return ((document_topic_counts[d][topic] + alpha) /
        (document_lengths[d] + K * alpha))

def p_word_given_topic(word, topic, beta=0.1):
    """the fraction of words assigned to _topic_
    that equal _word_ (plus some smoothing)"""
    return ((topic_word_counts[topic][word] + beta) /
        (topic_counts[topic] + W * beta))

'''
- There are solid mathematical reasons why topic_weight 
is defined the way it is, but
their details would lead us too far 
afield. Hopefully it makes at least intuitive sense
that—given a word and its document—the 
likelihood of any topic choice depends on
both how likely that topic is for the 
document and how likely that word is for the
topic.
-actually it is topic weight for a word in a document
and as paper 2 says we will asign the topic with the highest weight
to that word in that document
'''
def topic_weight(d, word, k):
    """given a document and a word in that document,
    return the weight for the kth topic"""
    return p_word_given_topic(word, k) * p_topic_given_document(k, d)
    
'''We’ll use these to create the weights for updating topics:
@return list a list of K members like [0.1,0.3,...] 
'''
def choose_new_topic(d, word):
    return sample_from([topic_weight(d, word, k)
                        for k in range(K)])

'''This is all the machinery we need. 
We start by assigning every word to a random
topic, and populating our counters appropriately:
'''
random.seed(0)

''' As mentioned before document_topics[3][4]
for example contains which topic the fifth
word in forth document is belonging to. we 
first fill it randomly '''
document_topics = [[random.randrange(K) for word in document]
for document in documents]

'''D is the length of documents'''   
for d in range(D):
    for word, topic in zip(documents[d], document_topics[d]):
        document_topic_counts[d][topic] += 1
        topic_word_counts[topic][word] += 1
        topic_counts[topic] += 1

'''Our goal is to get a joint sample of 
the topics-words distribution
 and 
 the documents-topics distribution. 
 We do this using a 
form of Gibbs sampling that uses the conditional
probabilities defined previously:
'''
for iter in range(1000):
    for d in range(D):
        for i, (word, topic) in enumerate(zip(documents[d],
                                            document_topics[d])):
            # remove this word / topic from the counts
            # so that it doesn't influence the weights
            document_topic_counts[d][topic] -= 1
            topic_word_counts[topic][word] -= 1
            topic_counts[topic] -= 1
            document_lengths[d] -= 1
            # choose a new topic based on the weights
            new_topic = choose_new_topic(d, word)
            document_topics[d][i] = new_topic
            # and now add it back to the counts
            document_topic_counts[d][new_topic] += 1
            topic_word_counts[new_topic][word] += 1
            topic_counts[new_topic] += 1
            document_lengths[d] += 1

'''What are the topics? They’re just numbers 0, 1, 2, and 3.
 If we want names for them
we have to do that ourselves. 
Let’s look at the five most heavily weighted words for
each (Table 20-1):'''
for k, word_counts in enumerate(topic_word_counts):
    for word, count in word_counts.most_common():
        if count > 0: print k, word, count

'''Based on these I’d probably assign topic names:'''
topic_names = ["Big Data and programming languages",
                "Python and statistics",
                "databases",
                "machine learning"]
                
'''at which point we can see how the model 
assigns topics to each user’s interests:'''
for document, topic_counts in zip(documents, document_topic_counts):
    print document
    for topic, count in topic_counts.most_common():
        if count > 0:
            print topic_names[topic], count,
    print

'''
which gives:
['Hadoop', 'Big Data', 'HBase', 'Java', 'Spark', 'Storm', 'Cassandra']
Big Data and programming languages 4 databases 3
['NoSQL', 'MongoDB', 'Cassandra', 'HBase', 'Postgres']
databases 5
['Python', 'scikit-learn', 'scipy', 'numpy', 'statsmodels', 'pandas']
Python and statistics 5 machine learning 1

and so on. Given the “ands” we needed in some of our topic names, it’s possible we
should use more topics, although most likely we don’t have enough data to success‐
fully learn them.
'''

