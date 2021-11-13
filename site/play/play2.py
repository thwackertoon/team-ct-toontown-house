#!/usr/bin/python
#coding: latin-1

import cgitb
cgitb.enable()

import sys, os, random, string
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
user = SESS.read('user')

if not SESS.exists('user') or not SESS.exists('verified'):
    print '<!DOCTYPE html><html><head><META http-equiv="refresh" content="0;URL=/login.py"> </head></html>'
    sys.exit()

def newKey(size=6, chars=string.ascii_uppercase + string.digits):
    _k = ''.join(random.choice(chars) for x in range(size))
    while os.path.isfile('/var/keys/'+_k): _k = ''.join(random.choice(chars) for x in range(size))
    with open('/var/keys/'+_k,'wb') as f:f.write(user+"\n"+lang)
    return _k
    
key = newKey(32)
    
print """
<!DOCTYPE html>
<html>
    <head>
        <title>Toontown House</title>
        <script src="DetectPanda3D.js" language="javascript"></script>
        <script src="RunPanda3D.js" type="text/javascript"></script>
        <script>
            crashed = 1;
            function setNonCrash() {{crashed=0;}}
            function end() {{
                if (crashed==0) window.location.replace('thx.py');
                else window.location.replace('bugreport.py?plugin=1');
            }}
            
        </script>
    </head>
    <body style="background-image:url(/bg.png);background-size:100% 100%;height:100%;background-repeat:no-repeat;background-attachment:fixed;">
        <div id="wrapper" style="text-align: center; width: 50%; height: 100%; display: table; margin: 0px auto; background-color: rgba(255, 255, 255, .75);">
            <div id="header">
                <img src="/header.png"></img>
            </div>
            <div id="play">
                <script type="text/javascript">
                    P3D_RunContent('data', 'TTHL.p3d', 'id', 'p3dobject','width', '800', 'height', '600', 'key', '{0}' ,'auto_start','1',"splash_img","logo.png","onWindowOpen","setNonCrash();","onPythonStop","end();");
                </script>
            </div>
        </div>
    </body>
</html>
""".format(key)