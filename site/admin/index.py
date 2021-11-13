#!/usr/bin/python
#coding: latin-1

import cgitb
cgitb.enable()

import sys, os
sys.path.append('/var/game')
import spsl

print "Content-Type: text/html"
spsl.init()

if not SESS.exists('user'):
    print '<!DOCTYPE html><html><head><META http-equiv="refresh" content="0;URL=/login.py"> </head></html>'
    sys.exit()
    
user = spsl.Blob('/var/game/data/blobs/'+SESS.read('user')+'.blob')
hasAdminRights = user.exists('acc_admin')
if not hasAdminRights:
    print '<!DOCTYPE html><html><head><META http-equiv="refresh" content="0;URL=/"> </head></html>'
    sys.exit()
    
SESS.write('admin','yes',0)
SESS.flush()

print """
<!DOCTYPE html>
<html>
    <head>
        <title>Toontown House</title>
        <script src="DetectPanda3D.js" language="javascript"></script>
        <script src="RunPanda3D.js" type="text/javascript"></script>
        <script>
            detectPanda3D('plugin.py',false);
            if (navigator.appVersion.indexOf("Win")==-1) window.location.replace('badOS.py');
            setTimeout(function(){{window.location.replace('play2.py')}},4000);
        </script>
    </head>
    <body style="background-image:url(/bg.png);background-size:100% 100%;height:100%;background-repeat:no-repeat;background-attachment:fixed;">
        <div id="wrapper" style="text-align: center; width: 50%; height: 100%; display: table; margin: 0px auto; background-color: rgba(255, 255, 255, .75);">
            <div id="header">
                <img src="/header.png"></img>
            </div>
            <span>{0}</span>
        </div>
    </body>
</html>
""".format({'en':'Verifying your system...','fr':'Vérification de votre système...','pt':'Verificando seu sistema...'}[lang])