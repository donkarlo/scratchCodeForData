# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup 
import requests
import re
from collections import defaultdict
import random
'''
The first is that the apostrophes in the text are actually 
the Unicode character
u"\u2019". We’ll create a helper 
function to replace them with normal apostrophes:
'''
def fix_unicode(text):
    return text.replace(u"\u2019", "'")


'''
The second issue is that once we get the 
text of the web page, we’ll want to split it into
a sequence of words and periods 
(so that we can tell where sentences end). We can do
this using re.findall():
'''
url = "http://radar.oreilly.com/2010/06/what-is-data-science.html"
html = requests.get(url).text
soup = BeautifulSoup(html, 'html5lib')

content = soup.find("div", "article-body")# find entry-content div
regex = r"[\w']+|[\.]"# matches a word or a period
document = []
for paragraph in content("p"):
    words = re.findall(regex, fix_unicode(paragraph.text))
    document.extend(words)
''' from here document contains the list of words'''
bigrams = zip(document, document[1:])
'''-So transitions will look like {'does':['he','she',...]
,'book':['is','over',...],...}'''
transitions = defaultdict(list)
for prev, current in bigrams:
    transitions[prev].append(current)
    
def generate_using_bigrams():
    current = "."
     # this means the next word will start a sentence
    result = []
    while True:
        next_word_candidates = transitions[current]#bigrams (current, _)
        current = random.choice(next_word_candidates)#choose one at random
        result.append(current)#append it to results
        if current == ".": 
            return " ".join(result)#if "." we're done
        

#print generate_using_bigrams()
#print "..................................."

trigrams = zip(document, document[1:], document[2:])
trigram_transitions = defaultdict(list)
starts = []
for prev, current, next in trigrams:
    if prev == ".": # if the previous "word" was a period
        starts.append(current) # then this is a start word
    trigram_transitions[(prev, current)].append(next)
    
def generate_using_trigrams():
    current = random.choice(starts)# choose a random starting word
    prev = "."# and precede it with a '.'
    result = [current]
    while True:
        next_word_candidates = trigram_transitions[(prev, current)]
        next_word = random.choice(next_word_candidates)
        prev, current = current, next_word
        result.append(current)
        if current == ".":
            return " ".join(result)

#print generate_using_trigrams()
