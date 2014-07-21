# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 20:53:51 2014

@author: Milad
"""

from textblob import TextBlob
import time
from cities import *

tweet = TextBlob(u"my tweet is very positive :)")

print tweet.words
print TextBlob(u"my tweet is very positive :)").sentiment[0]

p = ["san francisco", "austin"]

t = "whats up #san francisco whats crackin austin"
for i in p:
    if i in t:
        print i
        break