# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 21:08:49 2014

@author: Milad
"""

from twitter_credentials import *
import tweepy
from textblob import TextBlob
from pprint import pprint
import simplejson

public_tweets = api.home_timeline()

l = []
for tweet in public_tweets:
    l.append([tweet.text,TextBlob(tweet.text).sentiment[0]])

for s in l:
    print s
    

