#!/usr/bin/python
#coding: latin-1

import cgitb
cgitb.enable()

import sys, os, struct, zlib
from cPickle import dumps
from base64 import *
#print "Content-Type: text/plain"

sys.path.append('/var/game')
import spsl

def testUA(ua):
    try:
        stamp,ua = ua.split('.')
        _house,dump = ua.split('/')
    except:
        return False #didnt split, bad format, invalid
        
    if stamp != str(struct.unpack("<I",b64decode(dump))[0]): return False
    if _house != "House": return False
    return True

_userAgent = os.environ["HTTP_USER_AGENT"]
_key = spsl.get('key')

#if not testUA(_userAgent) or not _key:
 #   print "BAD AGENT!"
  #  sys.exit()
    
_key = '/var/keys/'+_key
if not os.path.exists(_key):
    print "BAD KEY!"
    sys.exit()
    
f = open(_key,'rb')
data = dict(zip(("u","lang"),f.read().strip().split('\n')))
f.close()

make_buffer = lambda data: zlib.compress(dumps(data)).encode('base64')
print make_buffer(data)