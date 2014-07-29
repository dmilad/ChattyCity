# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 11:08:38 2014

@author: Milad
"""

import re
import simplejson
from textblob import TextBlob
from cities import cities_l
import time

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

def parse(g, data, uid):
    try:
        data = simplejson.loads(data, cls=ConcatJSONDecoder)
        n = 0
        with open(g,"a") as writefile:
            
            tweet = repr(data[n]["text"]).replace("\n"," - ")
            hashtags = " ".join(re.findall(r"#([\w]+)", tweet))
            if hashtags == "":
                hashtags = "None"
            writefile.write(str(uid)+"\t"+hashtags+"\t")
            uid += 1
               
            dt = time.strptime(data[n]["created_at"], '%a %b %d %H:%M:%S +0000 %Y') # reformat date
            writefile.write(time.strftime('%Y-%m-%dT%H:%M:%S.000Z',dt)+"\t") #tstamp
            
            src_place = repr(data[n]["place"]["name"]).lower() if data[n]["place"] is not None else "None"
            src_usrloc = repr(data[n]["user"]["location"]) if data[n]["user"]["location"] is not u'' else "None"
    
            writefile.write(src_place+"\t")#src_city_place
            writefile.write(src_usrloc+"\t")#src_city_user
            writefile.write(find_loc(src_place if src_place != "None" else src_usrloc)+"\t")#src_city
            
            writefile.write(find_loc(tweet)+"\t") #src_dest
            writefile.write(tweet+"\t")#tweet
            writefile.write(str(TextBlob(data[n]["text"]).sentiment[0])+"\n")#sentiment
            

    except:
        pass
    
    return uid

def clean_file(f):
    curser = 0  
    count = 0 #count number of tweets
    middle = True
    
    with open("max_id_count.txt","r") as idc:
        uid = idc.readline()
    
    uid = int(uid) + 1    
    
    with open(f,"r") as readfile:
        g = "clean"+f
        with open(g, "w") as writefile:
            writefile.write("uid\thashtags\tstamp\tsrc_city_place\tsrc_city_user\tsrc_city\tdest_city\ttweet\tsentiment\n")
        while middle:
            text = readfile.read(500000)
            ret = ['{'+x+'}' for x in text.strip('{}').split('}{')]
            if len(ret) > 1:
                ret.pop()
            else:
                middle = False
            for i in ret:
                uid = parse(g, i, uid)
                count += 1
                curser += len(i)
    
            readfile.seek(curser)
            
    with open("max_id_count.txt","w") as idc:
        idc.write(str(uid-1))

if __name__ == "__main__":
    pass