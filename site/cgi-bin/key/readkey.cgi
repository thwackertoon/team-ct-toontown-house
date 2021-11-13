#! /usr/bin/python
import cgitb
cgitb.enable()

import cgi, sys, os, zlib
from cPickle import dumps as dp

print 'Content-Type: text/html;'
print

form = cgi.FieldStorage()

def _REQ(f):
    if not f in form:
        return ''
    return form[f].value
    
lang = _REQ('lang')
if not lang:
    if "HTTP_ACCEPT_LANGUAGE" in os.environ:
        lang = os.environ["HTTP_ACCEPT_LANGUAGE"][:2]
        
if not lang in ['pt','en']: lang = 'en'

def _exit(msg):
    print zlib.compress(dp(msg)).encode('base64').replace('\r','').replace('\n','')
    sys.exit()

if not all((_REQ(x) for x in ['key'])): _exit({"error":-2})

_key = _REQ('key').replace('/','').replace('.','')
sys.path.append('/var/game')
from Blob import Blob
    
if not os.path.isfile('/var/keys/'+_key):
    _exit({"error":-1})
    
with open('/var/keys/'+_key,'rb') as f: _user = f.read()
b = Blob('/var/game/data/blobs/'+_user+'.blob')
l = b.read('acc_lang')

_exit({"u":_user,"lang":l})