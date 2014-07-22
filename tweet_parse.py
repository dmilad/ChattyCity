# -*- coding: utf-8 -*-
"""
Created on Tue Jul 08 17:31:44 2014

@author: Milad
"""

import re
import simplejson
from pprint import pprint
from textblob import TextBlob
import os
import time
from cities import cities_l

#time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(data[n]['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

#some inspiration here: 
#http://stackoverflow.com/questions/8730119/retrieving-json-objects-from-a-text-file-using-python


FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)

class ConcatJSONDecoder(simplejson.JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        s_len = len(s)

        objs = []
        end = 0
        while end != s_len:
            obj, end = self.raw_decode(s, idx=_w(s, end).end())
            end = _w(s, end).end()
            objs.append(obj)
        return objs

def find_loc(p1):
    if p1 != "None":
        for city in cities_l:
            if city in p1.lower():
                return city
    return "None"

indir = os.getcwd()+"/tweetfiles"
for root, dirs, filenames in os.walk(indir):
        for f in filenames:
            f2 = os.path.join(indir,f)
            print f
            with open(f2,"r") as readfile:
                text = readfile.read()
                data = simplejson.loads(text, cls=ConcatJSONDecoder)
            g = os.path.join(indir, f+"_parsed.txt")
            print g
            with open(g,"w") as writefile:
                writefile.write("tstamp\tsrc_city_place\tsrc_city_user\tsrc_city\tdest_city\ttweet\tsentiment\n")                
                for n in range(len(data)):
                    writefile.write(data[n]["created_at"]+"\t") #tstamp
                    
                    src_place = repr(data[n]["place"]["name"]).lower() if data[n]["place"] is not None else "None"
                    src_usrloc = repr(data[n]["user"]["location"]) if data[n]["user"]["location"] is not u'' else "None"

                    writefile.write(src_place+"\t")#src_city_place
                    writefile.write(src_usrloc+"\t")#src_city_user
                    writefile.write(find_loc(src_place if src_place != "None" else src_usrloc)+"\t")#src_city
                    
                    tweet = repr(data[n]["text"]).replace("\n"," - ")
                    
                    writefile.write(find_loc(tweet)+"\t") #src_dest
                    writefile.write(tweet+"\t")#tweet
                    writefile.write(str(TextBlob(data[n]["text"]).sentiment[0])+"\n")#sentiment
