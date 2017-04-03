'''training data to train a decision tree'''
inputs=[
    ({'level':'Senior', 'lang':'Java', 'tweets':'no', 'phd':'no'}, False),
    ({'level':'Senior', 'lang':'Java', 'tweets':'no', 'phd':'yes'}, False),
    ({'level':'Mid', 'lang':'Python', 'tweets':'no', 'phd':'no'}, True),
    ({'level':'Junior', 'lang':'Python', 'tweets':'no', 'phd':'no'}, True),
    ({'level':'Junior', 'lang':'R', 'tweets':'yes', 'phd':'no'}, True),
    ({'level':'Junior', 'lang':'R', 'tweets':'yes', 'phd':'yes'}, False),
    ({'level':'Mid', 'lang':'R', 'tweets':'yes', 'phd':'yes'}, True),
    ({'level':'Senior', 'lang':'Python', 'tweets':'no', 'phd':'no'}, False),
    ({'level':'Senior', 'lang':'R', 'tweets':'yes', 'phd':'no'}, True),
    ({'level':'Junior', 'lang':'Python', 'tweets':'yes', 'phd':'no'}, True),
    ({'level':'Senior', 'lang':'Python', 'tweets':'yes', 'phd':'yes'}, True),
    ({'level':'Mid', 'lang':'Python', 'tweets':'no', 'phd':'yes'}, True),
    ({'level':'Mid', 'lang':'Java', 'tweets':'yes', 'phd':'no'}, True),
    ({'level':'Junior', 'lang':'Python', 'tweets':'no', 'phd':'yes'}, False)
]

#how much info?
'''
@param class_probability a list like 
[n(false)/labels(false),n(false)/labels(false)]
like [0.2,0.8]
@ return the entropy
'''
def entropy(class_probabilities):
    """given a list of class probabilities, compute the entropy"""
    return sum(-p * math.log(p, 2)
        for p in class_probabilities
        if p)# ignore zero probabilities

'''
@param labels for the sample inputs here are 
[True,False,False,True,...]
@return Returns a list with 2 elemensts if have used 
the inputs variable
in this file in data_entropy function like [0.1,0.9]
or if it help with better understanding 
[n(False)/n(labels),n(True)/n(labels)]
'''
def class_probabilities(labels):
    total_count = len(labels)
    return [count / total_count
        for count in Counter(labels).values()]
            
'''You can see a sample data 
in this file with the name inputs
@param labeled_data is list of tuples each element is like an entry of inputs
variable in the begining of the file 
({'level':'Junior', 'lang':'Python', 'tweets':'no', 'phd':'yes'}, False)
and this tuples are listed into one list because for example 
all their lang entries where Python
'''
def data_entropy(labeled_data):
    labels = [label for _, label in labeled_data]
    probabilities = class_probabilities(labels)
    return entropy(probabilities)
    
'''
@param subsets are like a sub list of inputs
which are usually grouped by a specific value of an attrbute
like list of all inputs whose lang are R
[[(),(),...],[(),(),...],...], in each pranthesis represents 
one input in the begining of the file
'''
def partition_entropy(subsets):
    """find the entropy from this partition of data into subsets
    subsets is a list of lists of labeled data"""
    total_count = sum(len(subset) for subset in subsets)
    return sum( data_entropy(subset) * len(subset) / total_count
        for subset in subsets )

'''
-Actually it is better to call this function parition by attribute. 
-@oaram attribute like (has)phd? in inputs as given above
-@param a subset of inputs
-@returns groups, which is like this if 
    attribute is 'level' then 
    {'senior':[input1,input2,...],'Mid':[input5,input7,...],...}
    or more expanded
    {'senior':[({attr1:val1,...},label),(),...]
                        ,'Mid':[({},label),...],'Junior':[inp1,inp4,...]}
'''
def partition_by(inputs, attribute):
    """each input is a pair (attribute_dict, label).
    returns a dict : attribute_value -> inputs"""
    
    '''so now groups is like {key1:[],key2:[],...}'''
    groups = defaultdict(list)
    for input in inputs:
        '''inputis like ({'level':'Senior','lang':'java',...},false)'''
        ''''get the value of the specified attribute'''
        '''So key is like Senior for example '''
        key = input[0][attribute]
        '''then add this input to the correct list'''
        groups[key].append(input)
    return groups

'''
- computes the entropy corresponding to the given partition
- @param inputs is the whole or a subset of 
    our training data as in the begining of this file
- @return a number as the entropy 
'''
def partition_entropy_by(inputs, attribute):
    partitions = partition_by(inputs, attribute)
    return partition_entropy(partitions.values())


'''Testing'''
for key in ['level','lang','tweets','phd']:
    print key, partition_entropy_by(inputs, key)
# level 0.693536138896
# lang 0.860131712855
# tweets 0.788450457308
# phd 0.892158928262
senior_inputs = [(input, label)
                    for input, label in inputs if input["level"] == "Senior"]

for key in ['lang', 'tweets', 'phd']:
    print key, partition_entropy_by(senior_inputs, key)
# lang 0.4
# tweets 0.0
# phd 0.950977500433
'''End testing'''

'''
-The tree built by the below function 
can just decide on whether a leaf node is False or True
and hence it doesn't support other labels
 
-@return Sample output of build_tree_id3
('level',
{'Junior': ('phd', {'no': True, 'yes': False}),
'Mid': True,
'Senior': ('tweets', {'no': False, 'yes': True})})
or in other words

(attribute_1
    ,{attribute_1_value_1:(another_tree)
    ,attrubute_1_value_2:(some_other_subtree)
    ,...
    }
)
'''
def build_tree_id3(inputs, split_candidates=None):
    # if this is our first pass,
    # all keys of the first input are split candidates
    '''split candidate will be a list like the first time 
    ['level','lang','tweets','phd']    
    '''
    if split_candidates is None:
        split_candidates = inputs[0][0].keys()
    # count Trues and Falses in the inputs
    num_inputs = len(inputs)
    num_trues = len([label for item, label in inputs if label])
    num_falses = num_inputs - num_trues
    
    if num_trues == 0: return False # no Trues? return a "False" leaf
    if num_falses == 0: return True# no Falses? return a "True" leaf
        
    
    if not split_candidates:# if no split candidates left
        return num_trues >= num_falses# return the majority leaf
    
    '''
    -otherwise, split on the best attribute
    -the first time the split_candidates is 
    ['level','lang','tweets','phd']
    -key is a one argument function that all
    split_candidate attributes
    are sent in to chose the one with minimum entropy
    - we have chosen min becase we want to place the 
    attribute(the question) with biggest entropy on the top
    so it better creates a balanced tree. but in this code 
    to achieve this goal we are actually building the tree from 
    it's deepes leaves to it's highest decision nodes. 
    check the book for what leaves and decision nodes mean. 
    '''
    best_attribute = min(split_candidates,
                         key=partial(partition_entropy_by, inputs))
    partitions = partition_by(inputs, best_attribute)
    new_candidates = [a for a in split_candidates
                        if a != best_attribute]
    '''recursively build the subtrees'''
    subtrees = { attribute_value : build_tree_id3(subset, new_candidates)
    for attribute_value, subset in partitions.iteritems() }
        subtrees[None] = num_trues > num_falses# default case
     
    return (best_attribute, subtrees)
    
"""
- classify the input using the given decision tree
- @param tree A sample tree is visible above build_tree_id3
- @param sample input input is like a single entry in the begining of the file
-  
"""
def classify(tree, input):
    # if this is a leaf node, return its value
    if tree in [True, False]:
        return tree
        
    # otherwise this tree consists of an attribute to split on
    # and a dictionary whose keys are values of that attribute
    # and whose values of are subtrees to consider next
    '''
    - Check the sample output tree above the build_tree_id3
    '''
    attribute, subtree_dict = tree
    
    subtree_key = input.get(attribute) # None if input is missing attribute
    
    if subtree_key not in subtree_dict:# if no subtree for key,
        subtree_key = None# we'll use the None subtree
    
    subtree = subtree_dict[subtree_key]# choose the appropriate subtree
    return classify(subtree, input)# and use it to classify the input
    
tree = build_tree_id3(inputs)
classify(tree, { "level" : "Junior",
"lang" : "Java",
"tweets" : "yes",
"phd" : "no"} )# True
classify(tree, { "level" : "Junior",
"lang" : "Java",
"tweets" : "yes",
"phd" : "yes"} ) # False
classify(tree, { "level" : "Intern" } ) # True
classify(tree, { "level" : "Senior" } ) # False

'''
Given how closely decision trees can fit themselves to 
their training data, it’s not sur‐
prising that they have a tendency to overfit. 
One way of avoiding this is a technique
called random forests, in which we build multiple 
decision trees and let them vote on
how to classify inputs:
'''
def forest_classify(trees, input):
    votes = [classify(tree, input) for tree in trees]
    vote_counts = Counter(votes)
    return vote_counts.most_common(1)[0][0]
    
'''
A second source of randomness involves changing the way we chose the
best_attribute to split on. Rather than looking at all the remaining attributes, we
first choose a random subset of them and then split on whichever of those is best:
'''    
# if there's already few enough split candidates, look at all of them
if len(split_candidates) <= self.num_split_candidates:
    sampled_split_candidates = split_candidates
    # otherwise pick a random sample
else:
    sampled_split_candidates = random.sample(split_candidates,
                                             self.num_split_candidates)
# now choose the best attribute only from those candidates
best_attribute = min(sampled_split_candidates,
key=partial(partition_entropy_by, inputs))
partitions = partition_by(inputs, best_attribute)




