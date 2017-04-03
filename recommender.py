from __future__ import division
import math, random
from collections import defaultdict, Counter
from linear_algebra import dot

users_interests = [
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
@returns a list like [('Python', 4),
('R', 4),
('Java', 3),
('regression', 3),
('statistics', 3),
('probability', 3),
# ...
]
'''
popular_interests = Counter(interest
                            for user_interests in users_interests
                            for interest in user_interests).most_common()


def most_popular_new_interests(user_interests, max_results=5):
    suggestions = [(interest, frequency) 
                   for interest, frequency in popular_interests
                   if interest not in user_interests]
    return suggestions[:max_results]







'''The better way'''
#
# user-based filtering
#
'''['Big Data',
'C++',
'Cassandra',
'HBase',
'Hadoop',
'Haskell',
# ...
]
'''
def cosine_similarity(v, w):
    return dot(v, w) / math.sqrt(dot(v, v) * dot(w, w))



'''
A good place to start is collecting the known 
interests and (implicitly) assigning indi‐
ces to them. We can do this by using a set 
comprehension to find the unique interests,
putting them in a list, and then sorting them. 
The first interest in the resulting list will
be interest 0, and so on:
'''
unique_interests = sorted(list({ interest 
                                 for user_interests in users_interests
                                 for interest in user_interests }))
'''Next we want to produce an “interest” vector 
of 0s and 1s for each user. We just need
to iterate over the unique_interests list, 
substituting a 1 if the user has each interest,
a 0 if not:
'''
def make_user_interest_vector(user_interests):
    """given a list of interests, produce a vector whose i-th element is 1
    if unique_interests[i] is in the list, 0 otherwise"""
    return [1 if interest in user_interests else 0
            for interest in unique_interests]
'''after which, we can create a matrix of user interests simply by map-ping this function
against the list of lists of interests:
'''
user_interest_matrix = map(make_user_interest_vector, users_interests)

'''Now user_interest_matrix[i][j] equals 1 if user i specified interest j, 0 other‐
wise.
Because we have a small data set, it’s no problem to compute the pairwise similarities
between all of our users:
'''
user_similarities = [[cosine_similarity(interest_vector_i, interest_vector_j)
                      for interest_vector_j in user_interest_matrix]
                     for interest_vector_i in user_interest_matrix]

'''
after which, user_similarities[i][j] gives 
us the similarity between users i and j.
For instance, user_similarities[0][9] 
is 0.57, as those two users share interests in
Hadoop, Java, and Big Data. On the other
 hand, user_similarities[0][8] is only
0.19, as users 0 and 8 share only one interest, Big Data.
In particular, user_similarities[i] is the 
vector of user i’s similarities to every
other user. We can use this to write a function 
that finds the most similar users to a
given user. We’ll make sure not to include
 the user herself, nor any users with zero
similarity. And we’ll sort the results from 
most similar to least similar:

@return [(9, 0.5669467095138409),
(1, 0.3380617018914066),
(8, 0.1889822365046136),
(13, 0.1690308509457033),
(5, 0.1543033499620919)]

'''
def most_similar_users_to(user_id):
    pairs = [(other_user_id, similarity)                      # find other
             for other_user_id, similarity in                 # users with
                enumerate(user_similarities[user_id])         # nonzero 
             if user_id != other_user_id and similarity > 0]  # similarity

    return sorted(pairs,                                      # sort them
                  key=lambda (_, similarity): similarity,     # most similar
                  reverse=True)                               # first

'''

[('MapReduce', 0.5669467095138409),
('MongoDB', 0.50709255283711),
('Postgres', 0.50709255283711),
('NoSQL', 0.3380617018914066),
('neural networks', 0.1889822365046136),
('deep learning', 0.1889822365046136),
('artificial intelligence', 0.1889822365046136),
#...
]
'''
def user_based_suggestions(user_id, include_current_interests=False):
    # sum up the similarities
    suggestions = defaultdict(float)
    for other_user_id, similarity in most_similar_users_to(user_id):
        for interest in users_interests[other_user_id]:
            suggestions[interest] += similarity

    # convert them to a sorted list
    suggestions = sorted(suggestions.items(),
                         key=lambda (_, weight): weight,
                         reverse=True)

    # and (maybe) exclude already-interests
    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight) 
                for suggestion, weight in suggestions
                if suggestion not in users_interests[user_id]]

#
# Item-Based Collaborative Filtering
#
'''To start with, we’ll want to transpose our user-interest matrix so that rows correspond
to interests and columns correspond to users:
'''
interest_user_matrix = [[user_interest_vector[j]
                         for user_interest_vector in user_interest_matrix]
                        for j, _ in enumerate(unique_interests)]
'''We can now use cosine similarity again. If precisely the same users are interested in
two topics, their similarity will be 1. If no two users are interested in both topics, their
similarity will be 0:
'''
interest_similarities = [[cosine_similarity(user_vector_i, user_vector_j)
                          for user_vector_j in interest_user_matrix]
                         for user_vector_i in interest_user_matrix]
'''For example, we can find the interests 
most similar to Big Data (interest 0) using:
'''
def most_similar_interests_to(interest_id):
    '''[0.1,0.3,0.5,...]
- actually the indexes are interest ids    
    '''
    similarities = interest_similarities[interest_id]
    pairs = [(unique_interests[other_interest_id], similarity)
             for other_interest_id, similarity in enumerate(similarities)
             if interest_id != other_interest_id and similarity > 0]
    return sorted(pairs,
                  key=lambda (_, similarity): similarity,
                  reverse=True)

def item_based_suggestions(user_id, include_current_interests=False):
    suggestions = defaultdict(float)
    user_interest_vector = user_interest_matrix[user_id]
    for interest_id, is_interested in enumerate(user_interest_vector):
        if is_interested == 1:
            similar_interests = most_similar_interests_to(interest_id)
            for interest, similarity in similar_interests:
                suggestions[interest] += similarity

    suggestions = sorted(suggestions.items(),
                         key=lambda (_, similarity): similarity,
                         reverse=True)

    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight) 
                for suggestion, weight in suggestions
                if suggestion not in users_interests[user_id]]
