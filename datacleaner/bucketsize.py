# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 17:37:09 2014

@author: Milad
"""

from aws_milad_keys import *
from boto.s3.connection import S3Connection

conn = S3Connection(keyid2,secret2)

bucket = conn.get_bucket('test-mysentimentjob')
blist = bucket.list()

inputbytes, outputbytes = 0, 0
for i in blist:
    klist = str(i.name).split("/")
    if klist[0] == 'input' and klist[1] != '':
        inputbytes += int(i.size)
    if klist[0] == 'output' and klist[1] != '':
        outputbytes += int(i.size)

print "input: %s GB"%str(round(float(inputbytes) / 1024**3, 2))
print "output: %s GB"%str(round(float(outputbytes) / 1024**3, 2))
