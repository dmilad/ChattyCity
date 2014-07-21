"""
Using Twitter stream API, print all the tweets containing a certain term for a certain amount of time

"""
from tweepy.streaming import StreamListener
#from tweepy import OAuthHandler
from tweepy import Stream
from twitter_credentials import *
from time import time,ctime
import simplejson
#import sys
from pprint import pprint as pp
from cities import *
import re

class StdOutListener(StreamListener):
   
    def __init__(self, timer):
        StreamListener.__init__(self)
        print "Gathering data at %s"%(str(ctime()))
        self.startTime = time()
        print "Start Time = %s"%(str(ctime()))
        self.timer = timer
        self.count = 0
        self.tweetlist = []   
        self.textfile = open("stream_text.txt","w")
       

    def on_data(self, data):
        try:
            self.endTime = time()
            self.elapsedTime = self.endTime - self.startTime
            if self.elapsedTime <= self.timer:
                self.dataJson =simplejson.loads(data[:-1])

                self.dataJsonText = self.dataJson["text"].replace("\n"," - ")
                for city in cities_l:
                    if city in self.dataJsonText.lower():
                        self.dataJsonDestLoc = city
                        break
                else:
                    self.dataJsonDestLoc = "None"
                        
                self.dataJsonSrcLoc = self.dataJson["user"]["location"].lower()
                self.loc1 = re.findall(r"([\w]+)",self.dataJsonSrcLoc)
                self.loc2 = re.findall(r"([\w]+.?[\w]+)",self.dataJsonSrcLoc)
                self.foundLoc = False
                for loc in self.loc1:
                    if loc in cities_ln:
                        self.dataJsonSrcLoc = loc
                        self.foundLoc = True
                for loc in self.loc2:
                    if not self.foundLoc and loc in cities_ln:
                        self.dataJsonSrcLoc = loc
                        self.foundLoc = True

                #self.tweetlist.append([str(ctime()), self.dataJsonSrcLoc, self.dataJsonDestLoc, self.dataJsonText, TextBlob(self.dataJsonText).sentiment[0]])
                if self.foundLoc:                
                    with open("stream_text.txt","a") as self.textfile:                
                        self.textfile.write(str(ctime())+"\t"+self.dataJsonSrcLoc+"\t"+self.dataJsonDestLoc+"\t"+self.dataJsonText+"\t"+str(TextBlob(self.dataJsonText).sentiment[0])+"\n")
                self.count += 1

            else:
                print "Total tweets sampled: ",self.count
                print "End Time = %s"%(str(ctime()))
                print "Elapsed Time = %s\n"%(str(self.elapsedTime))
                #pp(self.tweetlist)

                return False
            return True
        except Exception, e:
            pass

    def on_error(self, status):
        print ("ERROR :",status)

if __name__ == '__main__':

    l = StdOutListener(60)
    mystream = Stream(auth, l, timeout=60)
    mystream.filter(track = cities_filter)

#location: there are 3 locations associated with a tweet. all are nullable: 
#[coordinates] (if geotagged), 
#[place][name] if tweet associated with a place, and 
#[user][location] if user sets a location

#problem with name of cities that are really common: jackson
#mostly alleviated since we can filter on source city, and also if we filter on sentiment <>0
#there will still be an unusual volume for jackson

#huge volume of cities talking about themselves