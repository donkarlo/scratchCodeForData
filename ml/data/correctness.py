def accuracy(tp, fp, fn, tn):
    correct = tp + tn
    total = tp + fp + fn + tn
    return correct / total
print accuracy(70, 4930, 13930, 981070) # 0.98114

#Precision measures how accurate our positive predictions were
def precision(tp, fp, fn, tn):
    return tp / (tp + fp)
print precision(70, 4930, 13930, 981070) # 0.014

#recall measures what fraction of the positives our model identified
def recall(tp, fp, fn, tn):
    return tp / (tp + fn)
print recall(70, 4930, 13930, 981070) # 0.005

#Sometimes precision and recall are combined into the F1 score, which is defined as:
def f1_score(tp, fp, fn, tn):
    p = precision(tp, fp, fn, tn)
    r = recall(tp, fp, fn, tn)
    return 2 * p * r / (p + r)


