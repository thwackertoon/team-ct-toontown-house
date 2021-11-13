#!/usr/bin/python
#coding: latin-1

import cgitb
cgitb.enable()

import sys, os
sys.path.append('/var/game')
import spsl

print "Content-Type: text/html"
spsl.init()


if not SESS.exists('lang'):
    #determine
    lang = spsl.get('lang')
    if not lang:
        if "HTTP_ACCEPT_LANGUAGE" in os.environ:
            lang = os.environ["HTTP_ACCEPT_LANGUAGE"][:2] 
    if not lang in ['pt','en','fr']: lang = 'en'
    
    SESS.write('lang',lang,0)
    SESS.flush()
    
lang = SESS.read('lang')

if not SESS.exists('user'):
    print '<!DOCTYPE html><html><head><META http-equiv="refresh" content="0;URL=/login.py"> </head></html>'
    sys.exit()
    
SESS.write('verified',"ok",0)
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