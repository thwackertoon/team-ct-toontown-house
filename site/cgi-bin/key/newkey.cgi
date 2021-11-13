#! /usr/bin/python
import cgitb
cgitb.enable()

import cgi, sys, os
import string
import random

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

def error(id):
    print id
    sys.exit()

if not all((_REQ(x) for x in ['user','passwd'])): error(0)

sys.path.append('/var/game')
from Blob import Blob
if not os.path.isfile('/var/game/data/blobs/'+_REQ('user')+'.blob'):
    error(0)
    
if Blob('/var/game/data/blobs/'+_REQ('user')+'.blob').read('acc_passwd') != _REQ('passwd'):
    error(0)
    
#if wanna disable: error("2!message ....")
#if _REQ('user') != "__DEV": error("2!"+('DOWN FOR UPDATE!','FECHADO P/ ATAULIZACAO!')[lang!='en'])
    
def newKey(size=6, chars=string.ascii_uppercase + string.digits):
    _k = ''.join(random.choice(chars) for x in range(size))
    while os.path.isfile('/var/keys/'+_k): _k = ''.join(random.choice(chars) for x in range(size))
    with open('/var/keys/'+_k,'wb') as f:f.write(_REQ('user'))
    return _k
    
error(newKey(32))