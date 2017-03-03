# -*- coding: utf-8 -*-

from ....linearAlgebra.vector import distance
inputs = [[1,3]
            ,[4,7]
            ,[17,4]
            ,[21,5]
            ,[11,45]
            ,[2,2]
            ,[15,12]
            ,[22,11]
            ,[6,7]
            ,[9,14]
            ,[11,32]
            ,[13,21]
            ,[1,2]
            ,[3,7]
            ,[17,10]
            ,[10,17]
            ,[12,8]
            ,[4,3]
            ,[4,8]
            ,[15,6]
            ]

'''Each leaf only contains one input point. Don't let 
the trailing comma deceive you. it is just to prevent
python intrepertor from interpreting it as normal prantheses
like those we use in functions' argument definitions
'''
leaf1 = ([10, 20],) # to make a 1-tuple you need the trailing comma
leaf2 = ([30, -15],) # otherwise Python treats the parentheses as parentheses

'''We’ll use these to grow merged clusters, which we will represent as 2-tuples (merge
order, children):'''
merged = (1, [leaf1, leaf2])

def is_leaf(cluster):
    """a cluster is a leaf if it has length 1"""
    return len(cluster) == 1

def get_children(cluster):
    """returns the two children of this cluster if it's a merged cluster;
    raises an exception if this is a leaf cluster"""
    if is_leaf(cluster):
        raise TypeError("a leaf cluster has no children")
    else:
        return cluster[1]

'''
@param cluster [[2,11],[3,21],...]
'''
def get_values(cluster):
    """returns the value in this cluster (if it's a leaf cluster)
    or all the values in the leaf clusters below it (if it's not)"""
    if is_leaf(cluster):
        return cluster
     # is already a 1-tuple containing value
    else:
        return [value
                for child in get_children(cluster)
                for value in get_values(child)]

'''
In order to merge the closest clusters, we need some notion of the distance between
clusters. We’ll use the minimum distance between elements of the two clusters, which
merges the two clusters that are closest to touching (but will sometimes produce large
chain-like clusters that aren’t very tight). If we wanted tight spherical clusters, we
might use the maximum distance instead, as it merges the two clusters that fit in the
smallest ball. Both are common choices, as is the average distance:
@param cluster1 list [[1,4],[7,45],...] 
@param cluster2 list [[11,41],[71,45],...] 
'''
def cluster_distance(cluster1, cluster2, distance_agg=min):
    """compute all the pairwise distances between cluster1 and cluster2
    and apply _distance_agg_ to the resulting list"""
    return distance_agg([distance(input1, input2)
                            for input1 in get_values(cluster1)
                            for input2 in get_values(cluster2)])

'''We’ll use the merge order slot to track the order in which we did the merging. Smaller
numbers will represent later merges. This means when we want to unmerge clusters,
we do so from lowest merge order to highest. Since leaf clusters were never merged
(which means we never want to unmerge them), we’ll assign them infinity:'''
def get_merge_order(cluster):
    if is_leaf(cluster):
        return float('inf')
    else:
        return cluster[0] # merge_order is first element of 2-tuple
'''
@param inputs [[1,2],[5,8],[12,2],...]
@param distance_agg is function like min or max
@return 
(0, [(1, [(3, [(14, [(18, [([19, 28],),
                           ([21, 27],)]),
                    ([20, 23],)]),
                ([26, 13],)]),
            (16, [([11, 15],),
                  ([13, 13],)])]),
    (2, [(4, [(5, [(9, [(11, [([-49, 0],),
                              ([-46, 5],)]),
                        ([-41, 8],)]),
                    ([-49, 15],)]),
                ([-34, -1],)]),
            (6, [(7, [(8, [(10, [([-22, -16],),
                                 ([-19, -11],)]),
                            ([-25, -9],)]),
            (13, [(15, [(17, [([-11, -6],),
                              ([-12, -8],)]),
                        ([-14, -5],)]),
                    ([-18, -3],)])]),
         (12, [([-13, -19],),
               ([-9, -16],)])])])])
'''        
def bottom_up_cluster(inputs, distance_agg=min):
    '''start with every input a leaf cluster / 1-tuple
       - clusters is a list like [([1,5],[3,7],...),([4,78],[21,32],...),...]
       so each cluster is a tuple like ([1,5],[5,21],...)
    '''
    clusters = [(input,) for input in inputs]
    
    # as long as we have more than one cluster left...
    while len(clusters) > 1:
        # find the two closest clusters
        c1, c2 = min([(cluster1, cluster2)
            for i, cluster1 in enumerate(clusters)
            for cluster2 in clusters[:i]],
            key=lambda (x, y): cluster_distance(x, y, distance_agg))
        
        # remove them from the list of clusters
        clusters = [c for c in clusters if c != c1 and c != c2]
        # merge them, using merge_order = # of clusters left
        merged_cluster = (len(clusters), [c1, c2])
        # and add their merge
        clusters.append(merged_cluster)
    '''when there's only one cluster left, return it
    - This actually is 1-tulip    
    '''
    return clusters[0]

base_cluster = bottom_up_cluster(inputs)
print base_cluster

'''
A sample output
Since we had 20 inputs, it took 19 merges to get to this one cluster. The first merge
created cluster 18 by combining the leaves [19, 28] and [21, 27]. And the last
merge created cluster 0.
'''

'''
Generally, though, we don’t want to be squinting 
at nasty text representations like
this. Instead 
let’s write a function that generates any number
of clusters by performing the appropriate number of unmerges:
@param base_cluster is a cluster generated by 
'''
def generate_clusters(base_cluster, num_clusters):
    # start with a list with just the base cluster
    clusters = [base_cluster]
    # as long as we don't have enough clusters yet...
    while len(clusters) < num_clusters:
        # choose the last-merged of our clusters
        next_cluster = min(clusters, key=get_merge_order)
        # remove it from the list
        clusters = [c for c in clusters if c != next_cluster]
        # and add its children to the list (i.e., unmerge it)
        clusters.extend(get_children(next_cluster))
    # once we have enough clusters...
    return clusters

three_clusters = [get_values(cluster)
    for cluster in generate_clusters(base_cluster, 3)]

for i, cluster, marker, color in zip([1, 2, 3],
                                    three_clusters,
                                    ['D','o','*'],
                                    ['r','g','b']):
    xs, ys = zip(*cluster) # magic unzipping trick
    plt.scatter(xs, ys, color=color, marker=marker)
    # put a number at the mean of the cluster
    x, y = vector_mean(cluster)
    plt.plot(x, y, marker='$' + str(i) + '$', color='black')