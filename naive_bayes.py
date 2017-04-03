'''
Now we have all the pieces we need to build our classifier. First, let’s create a simple
function to tokenize messages into distinct words. We’ll first convert each message to
lowercase; use re.findall() to extract “words” consisting of letters, numbers, and
apostrophes; and finally use set() to get just the distinct words:
'''
def tokenize(message):
    message = message.lower()# convert to lowercase
    all_words = re.findall("[a-z0-9']+", message)# extract the words
    return set(all_words)# remove duplicates
    
'''    
Our second function will count the words in a labeled training set of messages. We’ll
have it return a dictionary whose keys are words, and whose values are two-element
lists [spam_count, non_spam_count] corresponding to how many times we saw that
word in both spam and nonspam messages:
{"viagra":[21,32],"rolex":[12,54],...}

the training_set is a list like [(message, is_spam),...] like ["bjd ajh jsd" ,0]
0 means it is not a spam
'''
def count_words(training_set):
    '''counts is dictionary that ewhenever encounter a new
    It never saw it creates a key for ait and assign [0,0] to it
    for example when it sees "fucker" for the first time
    it will be like counts={"viagra":[12,23],"fucker":[0,0]}      
    '''
    counts = defaultdict(lambda: [0, 0])
    for message, is_spam in training_set:
        for word in tokenize(message):
            counts[word][0 if is_spam else 1] += 1
    return counts

'''
Our next step is to turn these counts into estimated probabilities using the smoothing
we described before. Our function will return a list of triplets containing each word,
the probability of seeing that word in a spam message, and the probability of seeing
that word in a nonspam message:
[("viagra",0.21,0.54),("rolex",0.13,0.23),...]
This will be used when training our data
'''
def word_probabilities(counts, total_spams, total_non_spams, k=0.5):
    """turn the word_counts into a list of triplets
    w, p(w | spam) and p(w | ~spam)"""
    return [(w,
        (spam + k) / (total_spams + 2 * k),
        (non_spam + k) / (total_non_spams + 2 * k))
        for w, (spam, non_spam) in counts.iteritems()]
'''
The last piece is to use these word probabilities 
(and our Naive Bayes assumptions) to
assign probabilities to messages:
'''
def spam_probability(word_probs, message):
    message_words = tokenize(message)
    log_prob_if_spam = log_prob_if_not_spam = 0.0
    # iterate through each word in our vocabulary
    for word, prob_if_spam, prob_if_not_spam in word_probs:
        # if *word* appears in the message,
        # add the log probability of seeing it
        if word in message_words:
            log_prob_if_spam += math.log(prob_if_spam)
            log_prob_if_not_spam += math.log(prob_if_not_spam)
        # if *word* doesn't appear in the message
        # add the log probability of _not_ seeing it
        # which is log(1 - probability of seeing it)
        else:
            log_prob_if_spam += math.log(1.0 - prob_if_spam)
            log_prob_if_not_spam += math.log(1.0 - prob_if_not_spam)
    
    prob_if_spam = math.exp(log_prob_if_spam)
    prob_if_not_spam = math.exp(log_prob_if_not_spam)
    return prob_if_spam / (prob_if_spam + prob_if_not_spam)
'''
First we train the data using the train method with training_set
the training_set is a list like [(message, is_spam),...]
'''
class NaiveBayesClassifier:
    def __init__(self, k=0.5):
        self.k = k
        self.word_probs = []
        
    def train(self, training_set):
        # count spam and non-spam messages
        num_spams = len([is_spam
        for message, is_spam in training_set
            if is_spam])
            num_non_spams = len(training_set) - num_spams
            
            # run training data through our "pipeline"
            word_counts = count_words(training_set)
            self.word_probs = word_probabilities(word_counts,
                                                num_spams,
                                                num_non_spams,
                                                self.k)
    def classify(self, message):
        return spam_probability(self.word_probs, message)


