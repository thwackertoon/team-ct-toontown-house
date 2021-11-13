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

TITLE_EN = "Thanks for playing Toontown House!"
TITLE_PT = "Obrigado por jogar Toontown House!"
TITLE_FR = "Merci d'avoir joué à Toontown House!"

TITLE = {'pt':TITLE_PT,'en':TITLE_EN,'fr':TITLE_FR}[lang]

print """
<!DOCTYPE html>
<html>
    <head>
        <title>Toontown House</title>
    </head>
    <body style="background-image:url(/bg.png);background-size:100% 100%;height:100%;background-repeat:no-repeat;background-attachment:fixed;">
        <div id="wrapper" style="text-align: center; width: 50%; height: 100%; display: table; margin: 0px auto; background-color: rgba(255, 255, 255, .75);">
            <div id="header">
                <img src="/header.png"></img>
            </div>
            <div id="msg">
                <h1>{0}</h1>
                <h3><a href="/">{1}</a></h3>
            </div>
        </div>
    </body>
</html>
""".format(TITLE,{'en':'Go back','fr':'Retourner','pt':'Voltar'}[lang])