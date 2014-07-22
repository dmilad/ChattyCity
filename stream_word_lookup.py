"""
Using Twitter stream API, print all the tweets containing a certain term for a certain amount of time

"""
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twitter_credentials import *
from time import time,ctime
import simplejson
import sys
from pprint import pprint as pp

class StdOutListener(StreamListener):
   
    def __init__(self, timer, phrase, exact = False):
        self.inc = 0
        StreamListener.__init__(self)
        print "Gathering data at %s"%(str(ctime()))
        self.startTime = time()
        print "Start Time = %s"%(str(ctime()))
        self.timer = timer
        self.count = 0
        self.phrase = phrase
        self.exact = exact
        self.tweetlist = []
        if self.exact:
            print "Looking for tweets with: %s (exact)" % self.phrase
        else:
            print "Looking for tweets with: %s" % self.phrase        
       

    def on_data(self, data):
        try:
            self.endTime = time()
            self.elapsedTime = self.endTime - self.startTime
            if self.elapsedTime <= self.timer:
                self.dataJson =simplejson.loads(data[:-1])
                if self.exact:
                    self.dataJsonText = self.dataJson["text"]
                else:
                    self.dataJsonText = self.dataJson["text"].lower()
                pp(self.dataJson)
                self.tweetlist.append(self.dataJsonText)
                self.count += 1
                if self.phrase in self.dataJsonText:
                    print "\t"+self.dataJsonText
                    self.inc += 1

            else:
                print "Total tweets sampled: ",self.count
                print "# of tweets with %s: %d" % (self.phrase, self.inc)
                print "End Time = %s"%(str(ctime()))
                print "Elapsed Time = %s\n"%(str(self.elapsedTime))
                print self.tweetlist

                return False
            return True
        except Exception, e:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status):
        print ("ERROR :",status)

if __name__ == '__main__':
    # to collect the data for 1 min

    l = StdOutListener(2,"san francisco")
    mystream = Stream(auth, l, timeout=60)
    mystream.filter(track=['san francisco,sf,los angeles'])
        