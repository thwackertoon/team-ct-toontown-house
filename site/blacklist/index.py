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
   
user = None   
if SESS.exists('user'): user = SESS.read('user')

topText = ""

def _getHeader():
    greetingText = {
        'en':'Add a work to blacklist',
        'fr':'Ajouter un travail à la liste noire',
        'pt':'Adicionar uma palavra à lista negra'
        }[lang]
        
        
    data = '<img src="header.png"></img>{0}<hr><h1>{1}</h1>'.format(topText,greetingText)
    return data

print """
<!DOCTYPE html>
<html>
    <head>
        <title>Toontown House</title>
    </head>
    <body style="background-image:url(bg.png);background-size:100% 100%;height:100%;background-repeat:no-repeat;background-attachment:fixed;">
        <div id="wrapper" style="text-align: center; width: 50%; height: 100%; display: table; margin: 0px auto; background-color: rgba(255, 255, 255, .75);">
            <div id="header">
            {0}
            </div>
            <form action="index.py" method="POST">
                <p>{1}</p>
                <input type="text" name="theword" autocomplete="off"></input><br>
                <p>{2}</p>
                <input type="text" name="theword"></input><br>
            </form>
        </div>
    </body>
</html>
""".format(_getHeader(),{'pt':'Jogar agora!','en':'Play now!','fr':'Jouer maintenant!'}[lang])