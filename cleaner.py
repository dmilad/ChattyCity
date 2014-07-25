# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 18:07:37 2014

@author: Milad
"""
from aws_milad_keys import *
from boto.s3.connection import S3Connection
import os
import clean_tweets
from time import ctime

def main():
    #if input file name is XX.txt, output file is cleanXX.txt
    conn = S3Connection(keyid2,secret2)
    
    #bucket = conn.get_bucket('miladsbucket1')
    bucket = conn.get_bucket('test-mysentimentjob')
    blist = bucket.list()
    
    #check input and output against each other
    inputlist, outputlist = [], []
    for i in blist:
        klist = str(i.name).split("/")
        if klist[0] == 'input' and klist[1] != '':
            inputlist.append(klist[1])
        if klist[0] == 'output' and klist[1] != '':
            outputlist.append(klist[1][5:])
        
    worklist = []
    for i in inputlist:
        if i not in outputlist:
            worklist.append(i)
    
    for textfile in worklist:
        with open("cleaning_logfile.txt","a") as logfile:
        key = bucket.get_key("input/%s"%textfile)
        
    #download file to local directory. name will be same as what it is on S3
        key.get_contents_to_filename(textfile)
        # write to log file
        with open("cleaning_logfile.txt","a") as logfile:
            logfile.write("%s downloaded at %s.\n"%(textfile, str(ctime())))
    
    #clean file: create a new file named "clean" concatenated to beginning. go
    #through file and parse json objects to tab delimited format
        clean_tweets.clean_file(textfile)
        cleantextfile = "clean%s"%textfile
        #write to log file
        with open("cleaning_logfile.txt","a") as logfile:
            logfile.write("%s created at %s.\n"%(cleantextfile, str(ctime())))
        
    #write file to s3
        key = bucket.new_key("output/%s"%cleantextfile)
        key.set_contents_from_filename(cleantextfile)
        key.make_public()
        #Write to log file
        with open("cleaning_logfile.txt","a") as logfile:
            logfile.write("%s written to S3 at %s.\n"%(cleantextfile, str(ctime())))
        
    #delete originally downloaded file and cleaned file from local directory
        os.remove(textfile)
        os.remove(cleantextfile)
        #write to log file
        with open("cleaning_logfile.txt","a") as logfile:
            logfile.write("%s and %s removed at %s.\n\n"%(textfile, cleantextfile, str(ctime())))    

if __name__ == "__main__":
    main()