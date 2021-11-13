#!/usr/bin/python
#coding: latin-1

import cgitb
cgitb.enable()

import sys, os
sys.path.append('/var/game')
import spsl
print 'Content-Type: text/html'
spsl.init()

nf = {}
of = SESS.files

for f,c in of.items():
    if f != 'user': nf[f] = c
    
SESS.files = nf
SESS.flush()
        
print """
<!DOCTYPE html>
<html><head><META http-equiv="refresh" content="0;URL=/"> </head></html>
"""