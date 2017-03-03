class KMeans:
    """performs k-means clustering"""
    def __init__(self, k):
        self.k = k# number of clusters
        '''Means are a list of 2-d points. since eache point
            was also presented by a list so it looks something like
            [[1.2,2.3],[2.6,6.5],...], in kmeans
            a means has k elements and if first is filled
            by k random selected inputs in train method
        '''
        self.means = None# means of clusters
    '''
    @param input is a pint(list) in 2D(or n-D world) like [1.2,2.6]
    @return int the index of the mean from which 
    the input has the least distance
    '''  
    def classify(self, input):
        """return the index of the cluster closest to the input"""
        return min(range(self.k),
                       key=lambda i: squared_distance(input, self.means[i]))
                       
    def train(self, inputs):
        '''choose k random points from inputs as the initial means'''
        self.means = random.sample(inputs, self.k)
        
        '''Is a list of integers each denoting 
        the index of the mean to which
        each input is closer. So it has as many members as the inputs.
        Since we dont mess with the order of inputs, this could serve
        us as a good tool to see if points are changing their clusters
        or not
        '''
        assignments = None

        ''' The loop runs as long as the new 
        computed means 
        would not
        make inputs to choose new assignments.   
        '''        
        while True:
            '''Find new assignments'''
            new_assignments = map(self.classify, inputs)
            
            '''If no assignments have changed, we're done.'''
            if assignments == new_assignments:
                return
            
            '''Otherwise keep the new assignments'''
            assignments = new_assignments
            
            '''And compute new means based on the new assignments'''
            for i in range(self.k):
                '''find all the points assigned to cluster i'''
                i_points = [p for p, a in zip(inputs, assignments) if a == i]
                
                '''make sure i_points is not empty so don't divide by 0'''
                if i_points:
                    self.means[i] = vector_mean(i_points)

random.seed(0) # so you get the same results as me
clusterer = KMeans(3)
clusterer.train(inputs)
print clusterer.means


'''How to choose k'''
def squared_clustering_errors(inputs, k):
    """finds the total squared error from k-means clustering the inputs"""
    clusterer = KMeans(k)
    clusterer.train(inputs)
    means = clusterer.means
    assignments = map(clusterer.classify, inputs)
    return sum(squared_distance(input, means[cluster])
        for input, cluster in zip(inputs, assignments))
        
'''now plot from 1 up to len(inputs) clusters
plot it and now choose the k for which the graph bends
'''
ks = range(1, len(inputs) + 1)
errors = [squared_clustering_errors(inputs, k) for k in ks]
plt.plot(ks, errors)
plt.xticks(ks)
plt.xlabel("k")
plt.ylabel("total squared error")
plt.title("Total Error vs. # of Clusters")
plt.show()


