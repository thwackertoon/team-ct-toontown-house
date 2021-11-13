"""
File: Blob.py
    Module: tth.datahnd
Author: Nacib
Date: JULY/25/2013
Description: Blob for storing data, a VFS into a single file
FROM COGTOWN
"""

import zlib
from base64 import *

class Blob:
    def __init__(self,file):
        self.file = file
        try:
            with open(file,"rb") as f: 
                self.data=f.read()
                if self.data: self.data=zlib.decompress(self.data)
        except Exception,e: raise Exception, e
        #print self.data
        self.data = self.data.split(chr(1))[1:]
        #self.data = self.data[:-1]
        self.files={}
        for i in range(0,len(self.data),2):
            key = self.data[i]
            #print "key:",key
            val = self.data[i+1]
            #print "val:",val
            decodedval = b64decode(val)
            #print decodedval
            self.files[key] = decodedval
        del self.data
        
    def bake(self):
        o=''
        for file in self.files.keys():
            o+=chr(1)+file+chr(1)+b64encode(self.files[file])
        return zlib.compress(o)
    
    def read(self,file):
        if not file in self.files:
            return ""
        return self.files[file]
    
    def write(self,file,data,append=True):
        if not file in self.files: 
            self.files[file]=data
            return
        if append:
            self.files[file]+=data
        else:
            self.files[file]=data
            
    def exists(self,file): return file in self.files
    
    def flush(self):
        with open(self.file,"wb") as f:
            f.write(self.bake())
            
    def all(self): return self.files
    
    def newToon(self,*a): pass
            
def newBlob(file):
    with open(file,"w") as f:pass #create
    return Blob(file)
    