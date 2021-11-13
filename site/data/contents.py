#!/usr/bin/python
#coding: latin-1

import cgitb
cgitb.enable()

import sys, os, hashlib

print "Content-Type: text/plain"
print

def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    f = open(f,'rb')
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()
    
def process(x,l = []):
    if os.path.isfile(x):
        l.append((x[5:],md5_for_file(x),str(os.path.getsize(x))))
        
    else:
        for a in os.listdir(x):
            process(os.path.join(x,a),l)
            
    return l
    
c = process('data')
print ','.join(map(lambda x:'*'.join(x),c))