def split_data(data, prob):
    """split data into fractions [prob, 1 - prob]"""
    results = [], []
    for row in data:
        results[0 if random.random() < prob else 1].append(row)
    return results
    
def train_test_split(x, y, test_pct):
    data = zip(x, y)# pair corresponding values
    train, test = split_data(data, 1 - test_pct) # split the data set of pairs
    x_train, y_train = zip(*train)# magical un-zip trick
    x_test, y_test = zip(*test)
    return x_train, x_test, y_train, y_test
    
    
#how to use the above code
model = SomeKindOfModel()
x_train, x_test, y_train, y_test = train_test_split(xs, ys, 0.33)
model.train(x_train, y_train)
performance = model.test(x_test, y_test)


