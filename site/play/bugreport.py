#!/usr/bin/python
#coding: latin-1

import cgitb
cgitb.enable()

import sys, os, datetime
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

TITLE_EN = "Report a bug"
TITLE_PT = "Reportar um bug"
TITLE_FR = "Signaler un bug"

TITLE = {'pt':TITLE_PT,'en':TITLE_EN,'fr':TITLE_FR}[lang]

SUCCESS_EN = "Your bug report was sent!"
SUCCESS_PT = "Seu relatório de bug foi enviado!"
SUCCESS_FR = "Votre rapport de bug a été envoyé!"

SUCCESS = {'pt':SUCCESS_PT,'en':SUCCESS_EN,'fr':SUCCESS_FR}[lang]

DESC_EN = "Describe what happened:"
DESC_PT = "Descreva o que aconteceu:"
DESC_FR = "Décrire ce qui s'est passé:"

DESC = {'pt':DESC_PT,'en':DESC_EN,'fr':DESC_FR}[lang]

if not SESS.exists('user'):
    print '<!DOCTYPE html><html><head><META http-equiv="refresh" content="0;URL=/login.py"> </head></html>'
    sys.exit()

user = SESS.read('user')

desc = spsl.get('desc')
if desc:
    _name = user+"_at_"+datetime.datetime.now().strftime("%d%m%y%H%M%S")
    with open('/var/bugs/'+_name+'.bug','wb') as f:
        f.write(desc)

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
                <p>{1}</p>
                <h3><a href="/">{2}</a></h3>
            </div>
        </div>
    </body>
    </html>
    """.format(TITLE,SUCCESS,{'en':'Go back','fr':'Retourner','pt':'Voltar'}[lang])
    sys.exit()

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
                <form action="bugreport.py" method="POST">
                    <p>{1}</p>
                    <textarea name="desc" cols="40" rows="7"></textarea><br>
                    <input type="submit"></input>
                <form>
            </div>
        </div>
    </body>
    </html>
""".format(TITLE,DESC)