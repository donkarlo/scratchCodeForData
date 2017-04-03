import random
# -*- coding: utf-8 -*-
'''
- I made up the convention that names 
starting with underscores refer to rules that
need further expanding, and that other names are 
terminals that don’t need further
processing.
So, for example, "_S" is the “sentence” rule, which 
produces a "_NP" (“noun phrase”)
rule followed by a "_VP" (“verb phrase”) rule.
The verb phrase rule can produce either the "_V" 
(“verb”) rule, or the verb rule 
followed by the noun phrase rule.
Notice that the "_NP" rule contains itself in 
one of its productions. Grammars can be
recursive, which allows even finite grammars 
like this to generate infinitely many different sentences.'''
grammar = {
    "_S" : ["_NP _VP"],
    "_NP" : ["_N",
             "_A _NP _P _A _N"],
    "_VP" : ["_V",
             "_V _NP"],
    "_N" : ["data science", "Python", "regression"],
    "_A" : ["big", "linear", "logistic"],
    "_P" : ["about", "near"],
    "_V" : ["learns", "trains", "tests", "is"]
}

'''I made up the convention that names starting 
with underscores refer to rules that
need further expanding, and that other 
names are terminals that don’t need further
processing.
So, for example, "_S" is the “sentence” 
rule, which produces a "_NP" (“noun phrase”)
rule followed by a "_VP" (“verb phrase”) rule.
The verb phrase rule can produce either 
the "_V" (“verb”) rule, or the verb rule followed 
by the noun phrase rule.
Notice that the "_NP" rule contains itself 
in one of its productions. Grammars can be
recursive, which allows even finite grammars 
like this to generate infinitely many dif‐
ferent sentences.
How do we generate sentences from this grammar? 
We’ll start with a list containing
the sentence rule ["_S"]. And then 
we’ll repeatedly expand each rule by replacing it
with a randomly chosen one of 
its productions. We stop when we have a list consist‐
ing solely of terminals.
For example, one such progression might look like:
'''
['_S']
['_NP','_VP']
['_N','_VP']
['Python','_VP']
['Python','_V','_NP']
['Python','trains','_NP']
['Python','trains','_A','_NP','_P','_A','_N']
['Python','trains','logistic','_NP','_P','_A','_N']
['Python','trains','logistic','_N','_P','_A','_N']
['Python','trains','logistic','data science','_P','_A','_N']
['Python','trains','logistic','data science','about','_A', '_N']
['Python','trains','logistic','data science','about','logistic','_N']
['Python','trains','logistic','data science','about','logistic','Python']

def is_terminal(token):
    return token[0] != "_"

def expand(grammar, tokens):
    for i, token in enumerate(tokens):
        # skip over terminals
        if is_terminal(token): continue
        # if we get here, we found a non-terminal token
        # so we need to choose a replacement at random
        replacement = random.choice(grammar[token])
        if is_terminal(replacement):
            tokens[i] = replacement
        else:
            tokens = tokens[:i] + replacement.split() + tokens[(i+1):]
        # now call expand on the new list of tokens
        return expand(grammar, tokens)
    # if we get here we had all terminals and are done
    return tokens
    
def generate_sentence(grammar):
    return expand(grammar, ["_S"])
    
print generate_sentence(grammar) 

