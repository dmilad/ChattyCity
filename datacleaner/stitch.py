# -*- coding: utf-8 -*-
"""
Created on Wed Aug 06 23:20:14 2014

@author: Milad
"""

from aws_milad_keys import *
from boto.s3.connection import S3Connection
import os
from time import ctime

def main():
    #if input file name is XX.txt, output file is cleanXX.txt
    conn = S3Connection(keyid2,secret2)
    
    #bucket = conn.get_bucket('miladsbucket1')
    bucket = conn.get_bucket('test-mysentimentjob')
    blist = bucket.list()
    
    log = "stitch_logfile.txt"
    
    #check input and output against each other
    worklist = []
    for i in blist:
        klist = str(i.name).split("/")
        if klist[0] == 'output2' and klist[1] != '':
            worklist.append(klist[1])

    onetextfile = "one.txt"    
    with open(onetextfile,"w") as writefile:
        writefile.write("uid\thashtags\tstamp\tsrc_city_place\tsrc_city_user\tsrc_city\tdest_city\ttweet\tsentiment\n")
        
    for textfile in worklist:
        key = bucket.get_key("output2/%s"%textfile)      
    
    #download file to local directory. name will be same as what it is on S3
        key.get_contents_to_filename(textfile)
        # write to log file
        with open(log,"a") as logfile:
            logfile.write("%s downloaded at %s.\n"%(textfile, str(ctime())))
    
        with open(textfile,"r") as readfile:
            readfile.readline()
            with open(onetextfile,"a") as writefile:
                for line in readfile:
                    writefile.write(line)
                    
        #write to log file
        with open(log,"a") as logfile:
            logfile.write("%s stitched at %s.\n"%(textfile, str(ctime())))
        
        #delete originally downloaded file from local directory
        os.remove(textfile)
        #write to log file
        with open(log,"a") as logfile:
            logfile.write("%s removed at %s.\n\n"%(textfile, str(ctime())))   

    #write file to s3
    key = bucket.new_key("onefile/%s"%onetextfile)
    key.set_contents_from_filename(onetextfile)
    key.make_public()
    #Write to log file
    with open(log,"a") as logfile:
        logfile.write("%s written to S3 at %s.\n"%(onetextfile, str(ctime())))
    
 

if __name__ == "__main__":
    main()