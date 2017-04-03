from collections import deque

users = [
    { "id": 0, "name": "Hero" },
    { "id": 1, "name": "Dunn" },
    { "id": 2, "name": "Sue" },
    { "id": 3, "name": "Chi" },
    { "id": 4, "name": "Thor" },
    { "id": 5, "name": "Clive" },
    { "id": 6, "name": "Hicks" },
    { "id": 7, "name": "Devin" },
    { "id": 8, "name": "Kate" },
    { "id": 9, "name": "Klein" }
]
friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
(4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

for user in users:
    user["friends"] = []
    
for i, j in friendships:
    # this works because users[i] is the user whose id is i
    users[i]["friends"].append(users[j]) # add i as a friend of j
    users[j]["friends"].append(users[i]) # add j as a friend of i

'''
- we give this function a user and we will expect
all shortest paths to that user. 
- we do start by his own direct friends
@param type from_user a dictionary like
{'id':6,'name':'Kate',friends:[{'id':14,...},{'id':24,...},{'id':19,...},...]}
@return a dictionary like 
a  user like {'id':7,'name':'Devin',friends:[{},{},...]}
is as follows:
{0: [[5, 4, 3, 1, 0], [5, 4, 3, 2, 0], [5, 4, 3, 1, 2, 0]],
 1: [[5, 4, 3, 1]],
 2: [[5, 4, 3, 2], [5, 4, 3, 1, 2]],
 3: [[5, 4, 3]],
 4: [[5, 4]],
 5: [[5]],
 6: [[5, 6], [8, 6]],
 7: [[]],#there is no path between 7 and 7
 8: [[8]],
 9: [[8, 9]]}

'''
def shortest_paths_from(from_user):
    # a dictionary from "user_id" to *all* shortest paths to that user
    '''
- in this line we are saying there is no path from from_user
to from_user    
    '''    
    shortest_paths_to = { from_user["id"] : [[]] }
    # a queue of (previous user, next user) that we need to check.
    # starts out with all pairs (from_user, friend_of_from_user)
    '''is a list with pop and push facilities
        - it is like [({'id':14,...},{'id':16,...})
        ,({'id':11,...},{'id':54,...}),...]    
    '''
    frontier = deque((from_user, friend)
                        for friend in from_user["friends"])
    # keep going until we empty the queue
    while frontier:
        prev_user, user = frontier.popleft()# remove the user who's
        user_id = user["id"]# first in the queue
        '''because of the way we're adding to the queue,
        - necessarily we already know 
        some shortest paths to prev_user
        , that is we actioally added an empty path like [[]] in
        the first line of this function 
        which was shortest_paths_to = { from_user["id"] : [[]] }         
        -ie the direct friends are already considered 
        as shortest paths        
        -On first iteration it must be empty but like [[]] in 
        schema  but in 
        later iterations it is expected to be a list of lists like 
        [[],[],...]      
        - by name path_to_prev_user
        we actually mean 
        paths_from_user_to_prev_user
        '''        
        paths_to_prev_user = shortest_paths_to[prev_user["id"]]
        '''- on the first iteration it will just contain the user_id 
        as a direct friend, so actually we are adding 
        direct friends as first found path    
        so in the first iteration for user 7
        new_paths_to_user will be [[1]]
        - [a]+[b] = [a,b]
        - by name new_paths_to_user
        we mean new_paths_from_prev_user_to_user
        '''        
        new_paths_to_user = [path + [user_id] 
                            for path 
                            in paths_to_prev_user]
        # it's possible we already know a shortest path
        '''If no shortest path has not been yet registered to
        user_id(which is the case in first iteration) 
        then assign an empty list like [] to it
        (see definition of dictionaries and their get method)
        - old_paths_from_prev_user_to_user
        '''
        old_paths_to_user = shortest_paths_to.get(user_id, [])
        '''what's the shortest path to here that we've seen so far?
        - note that paths to a node are naturally
        ordered in a from shortest to longest
        so old_paths_to_user[0] in undoubtedly
        the shortest possible path, the reason to the
        this naturality is that we add user id to paths one by one        
        '''
        if old_paths_to_user:
            min_path_length = len(old_paths_to_user[0])
        if not old_paths_to_user:
            min_path_length = float('inf')
            
        '''only keep paths that aren't too long and are actually new'''
        new_paths_to_user = [path
                                for path in new_paths_to_user
                                if len(path) <= min_path_length
                                and path not in old_paths_to_user]
            
        shortest_paths_to[user_id] = old_paths_to_user + new_paths_to_user
        # add never-seen neighbors to the frontier
        '''in the next line says friend["id"] must 
        not be direct freind of from_user        
        '''
        frontier.extend((user, friend)
                        for friend in user["friends"]
                        if friend["id"] not in shortest_paths_to)
    return shortest_paths_to
#print shortest_paths_from(users[7])
'''Now we can store these dicts with each node:'''
for user in users:
    user["shortest_paths"] = shortest_paths_from(user)

for user in users:
    user["betweenness_centrality"] = 0.0
'''
- we want to calculae how many times a node has appeared 
in shortes paths

- if a user id is not in neither the head or the tail 
of a path then it betweeness centrality is reduces as
the number of the heads and the tails of the paths
between them increases
'''
for source in users:
    source_id = source["id"]
    for target_id, paths in source["shortest_paths"].iteritems():
        if source_id < target_id:   # don't double count
            num_paths = len(paths)  # how many shortest paths?
            contrib = 1 / num_paths # contribution to centrality
            for path in paths:
                for id in path:
                    if id not in [source_id, target_id]:
                        users[id]["betweenness_centrality"] += contrib


#
# closeness centrality
#
def farness(user):
    """the sum of the lengths of the shortest paths to each other user"""
    return sum(len(paths[0]) 
               for paths in user["shortest_paths"].values())
                   
for user in users:
    user["closeness_centrality"] = 1 / farness(user)

#
# eigenvector centrality
#

def entry_fn(i, j):
    return 1 if (i, j) in friendships or (j, i) in friendships else 0
n = len(users)
adjacency_matrix = make_matrix(n, n, entry_fn)
eigenvector_centralities, _ = find_eigenvector(adjacency_matrix)   

#endorments
#
# directed graphs
#

endorsements = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1), (1, 3),
                (2, 3), (3, 4), (5, 4), (5, 6), (7, 5), (6, 8), (8, 7), (8, 9)]

for user in users:
    user["endorses"] = []       # add one list to track outgoing endorsements
    user["endorsed_by"] = []    # and another to track endorsements
    
for source_id, target_id in endorsements:
    users[source_id]["endorses"].append(users[target_id])
    users[target_id]["endorsed_by"].append(users[source_id])
    
endorsements_by_id = [(user["id"], len(user["endorsed_by"]))
                      for user in users]

sorted(endorsements_by_id, 
       key=lambda (user_id, num_endorsements): num_endorsements,
       reverse=True)
'''
A better metric would take into account who endorses you. 
Endorsements from peo‐
ple who have a lot of endorsements should somehow count 
more than endorsements
from people with few endorsements. This is the essence of the PageRank algorithm,
used by Google to rank websites based on which other websites link to them, which
other websites link to those, and so on.
(If this sort of reminds you of the idea behind eigenvector centrality, it should.)
A simplified version looks like this:
1. There is a total of 1.0 (or 100%) PageRank in the network.
2. Initially this PageRank is equally distributed among nodes.
3. At each step, a large fraction of each node’s PageRank 
is distributed evenly among
its outgoing links.
4. At each step, the remainder of each node’s PageRank is 
distributed evenly among
all nodes.
'''      
def page_rank(users, damping = 0.85, num_iters = 100):
    
    # initially distribute PageRank evenly
    num_users = len(users)
    pr = { user["id"] : 1 / num_users for user in users }

    # this is the small fraction of PageRank
    # that each node gets each iteration
    base_pr = (1 - damping) / num_users
    
    for __ in range(num_iters):
        next_pr = { user["id"] : base_pr for user in users }
        for user in users:
            # distribute PageRank to outgoing links
            links_pr = pr[user["id"]] * damping
            for endorsee in user["endorses"]:
                next_pr[endorsee["id"]] += links_pr / len(user["endorses"])

        pr = next_pr
        
    return pr   