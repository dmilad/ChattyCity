# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 10:36:27 2014

@author: Milad
"""

import re
from aws_milad_keys import *
from boto.s3.connection import S3Connection
import os
from time import ctime

def main():
    #if input file name is XX.txt, output file is csvXX.csv
    conn = S3Connection(keyid2,secret2)
    
    #bucket = conn.get_bucket('miladsbucket1')
    bucket = conn.get_bucket('test-mysentimentjob')
    blist = bucket.list()
    log = "id_logfile.txt"
    
    #check input and output against each other
    worklist = []
    for i in blist:
        klist = str(i.name).split("/")
        if klist[0] == 'output2' and klist[1] != '':
            worklist.append(klist[1])
    
    for textfile in worklist:
        key = bucket.get_key("output2/%s"%textfile)      
    
    #download file to local directory. name will be same as what it is on S3
        key.get_contents_to_filename(textfile)
        # write to log file
        with open(log,"a") as logfile:
            logfile.write("%s downloaded at %s.\n"%(textfile, str(ctime())))
    
        idhashtextfile = "id%s"%textfile
        
        with open("max_id_count2.txt","r") as idc:
            uid = idc.readline()
        
        uid = int(uid)+1
        
        with open(textfile,"r") as readfile:
            with open(idhashtextfile,"w") as writefile:
                header = readfile.readline()        
                writefile.write("uid\t"+header)
                for line in readfile:
                    writefile.write(str(uid)+"\t"+line)
                    uid += 1
        
        with open("max_id_count2.txt","w") as idc:
            idc.write(str(uid-1))

        #write to log file
        with open(log,"a") as logfile:
            logfile.write("%s created at %s.\n"%(idhashtextfile, str(ctime())))
        
    #write file to s3
        #key = bucket.new_key("output/%s"%idhashtextfile)
        key.set_contents_from_filename(idhashtextfile)
        key.make_public()
        #Write to log file
        with open(log,"a") as logfile:
            logfile.write("%s written to S3 at %s.\n"%(idhashtextfile, str(ctime())))
        
    #delete originally downloaded file and cleaned file from local directory
        os.remove(textfile)
        os.remove(idhashtextfile)
        #write to log file
        with open(log,"a") as logfile:
            logfile.write("%s and %s removed at %s.\n\n"%(textfile, idhashtextfile, str(ctime())))    

if __name__ == "__main__":
    main()
        