#simple python session layer
#by nacib
#module used to let python have session
#like php

import sys, os, random, Cookie, __builtin__, cgi
SPSL_SESPATH = "/var/tmp/sess/"

sys.path.append('/var/game')
from Blob import *

def new():
    _file=""
    while os.path.exists(os.path.join(SPSL_SESPATH,_file)):
        _file = os.urandom(24).encode('base64').strip().replace(' ','1').replace('/','2').replace('+','3')
    
    return newBlob(os.path.join(SPSL_SESPATH,_file))
    
def request(sess):
    if not os.path.exists(os.path.join(SPSL_SESPATH,sess)):
        raise Exception('invalid sessid! '+os.path.join(SPSL_SESPATH,sess)) #return new()
        
    return Blob(os.path.join(SPSL_SESPATH,sess))
    
def init():
    cookie = Cookie.SimpleCookie(*filter(None,[os.environ.get("HTTP_COOKIE",[])]))

    if "sessid" in cookie:
        sessid = cookie["sessid"].value
        
    try:
        SESS = request(sessid)
    
    except Exception as e:
        SESS = new()
        cookie["sessid"] = os.path.basename(SESS.file)
        print cookie.output()
        
        #print
        #print 'SET!!',cookie["sessid"].value,'<br>'
        #print 'E:',e,'<br>'
        #print 'DETECTED SESSID:',sessid,'<br>'
        #print 'HTTP_COOKIE:',os.environ.get("HTTP_COOKIE",[]),'<br>'
        
    print #end headers
    __builtin__.SESS = SESS
    __builtin__.cookie = cookie

form = cgi.FieldStorage()

def get(f):
    if not f in form:
        return ''
    return form[f].value