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

GoodOSes = ["Microsoft Windows"]

osListData = "<ul>"
for os in GoodOSes: osListData += "<li>"+os+"</li>"
osListData += "</ul>"

TITLE_EN = "Your OS is not supported"
TITLE_PT = "Seu sistema operacional não é suportado"
TITLE_FR = "Votre système d'exploitation n'est pas pris en charge"

MSG_EN = "You are playing from an unsupported OS! Currently, only the following operating system(s) are supported:</p> {0} <p> We plan to expand our support soon."
MSG_PT  = "Você está jogando de um sistema que não é suportado! Atualmente, apenas o(s) seguinte(s) sistema(s) é(são) suportado(s):</p> {0} <p> Nós planejamos expandir nosso suporte em breve."
MSG_FR  = "Vous jouez d'un OS non pris en charge! Actuellement, seul le système d'exploitation suivant (s) sont pris en charge:</p> {0} <p> Nous prévoyons d'étendre notre soutien bientôt."

TITLE = {'pt':TITLE_PT,'en':TITLE_EN,'fr':TITLE_FR}[lang]
MSG = {'pt':MSG_PT,'en':MSG_EN,'fr':MSG_FR}[lang].format(osListData)

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
""".format(TITLE,MSG,{'en':'Go back','fr':'Retourner','pt':'Voltar'}[lang])