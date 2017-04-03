from collections import Counter
'''give it a list of repeated labels like [p,pg,p,pp,pg,pg] 
    and it give you back which label is repeated the most
    as for this the winner is pg with 3 repeation 
    @return pg , a label
    '''
def raw_majority_vote(repeated_labels):# count of elements in repeated_labels in kNN is k
    votes = Counter(repeated_labels)
    label_repeated_the_most, _ = votes.most_common(1)[0]
    return label_repeated_the_most

def majority_vote(labels):
    """assumes that labels are ordered from nearest to farthest"""
    vote_counts = Counter(labels)
    winner, winner_count = vote_counts.most_common(1)[0]
    num_winners = len([count
                        for count in vote_counts.values()
                            if count == winner_count])
    if num_winners == 1:
        return winner# unique winner, so return it
    else:
        return majority_vote(labels[:-1]) # try again without the farthest, that means the label belonging to the farthest point  in comparision to the new coming point  among the k nearst points
'''
@param k is a number and for any given point 
we find k nearest neightbouring points and we vote their labels
and the label with most points will be also sticked to the new point

@param labeled_points is a list like 
cities = [([-122.3 , 47.53], "Python"), # Seattle
([ -96.85, 32.85], "Java"), # Austin
([ -89.33, 43.13], "R"), # Madison
# ... and so on
]

'''       
def knn_classify(k, labeled_points, new_point):
    """each labeled point should be a pair (point, label)"""
    # order the labeled points from nearest to farthest
    by_distance = sorted(labeled_points,
                         key=lambda (point, _): distance(point, new_point))
    # find the labels for the k closest
    k_nearest_labels = [label for _, label in by_distance[:k]]
    # and let them vote
    return majority_vote(k_nearest_labels)
    
    
#testing
# try several different values for k
cities = [([-122.3 , 47.53], "Python"), # Seattle
    ([ -96.85, 32.85], "Java"), # Austin
    ([ -89.33, 43.13], "R"), # Madison
    # ... and so on
]
    

for k in [1, 3, 5, 7]:
    num_correct = 0
    for city in cities:
        location, actual_language = city
        
        other_cities = [other_city
            for other_city in cities
                if other_city != city]
                    
        predicted_language = knn_classify(k, other_cities, location)
        if predicted_language == actual_language:
        num_correct += 1
        
    print k, "neighbor[s]:", num_correct, "correct out of", len(cities)

    