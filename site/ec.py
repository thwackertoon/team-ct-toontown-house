#!/usr/bin/python
#coding: latin-1

import cgitb
cgitb.enable()

import sys, os
sys.path.append('/var/game')
import spsl
print 'Content-Type: text/html'
spsl.init()

def validate(c):
    return c.rsplit('/')[-1]
    
code = spsl.get('code')
if code:
    #check code
    code = validate(code)
    
    if os.path.isfile('/var/tmp/mailcodes/'+code):
        with open('/var/tmp/mailcodes/'+code,'rb') as f: user = f.read()
        b = spsl.Blob('/var/game/data/blobs/{0}.blob'.format(user))
        b.write('acc_email_act','1',0)
        b.flush()
        SESS.write('user',user,0)
        SESS.flush()
        os.unlink('/var/tmp/mailcodes/'+code)
        
print """
<!DOCTYPE html>
<html><head><META http-equiv="refresh" content="0;URL=/"> </head></html>
"""