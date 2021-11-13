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

P3D_LINK = "https://www.panda3d.org/download/panda3d-runtime-1.0.4/Panda3D-Runtime-1.0.4.exe"

TITLE_EN = "Please install Panda3D plugin"
TITLE_PT = "Por favor, instale o plugin do Panda3D"
TITLE_FR = "Merci d'installer le plugin Panda3D"

MSG_EN = "You need to install Panda3D plugin to play Toontown House. <a href={0}>Click here</a> to download it and press continue after it's been installed!"
MSG_PT  = "Você precisa instalar o plugin do Panda3D para jogar Toontown House. <a href={0}>Clique aqui</a> para baixá-lo e clicar em continuar depois que ele for instalado!"
MSG_FR  = "Vous devez installer le plugin Panda3D pour jouer à Toontown House. <a href={0}>Cliquez ici </a> pour le télécharger et cliquez sur 'continue' après l'installation!"

TITLE = {'pt':TITLE_PT,'en':TITLE_EN,'fr':TITLE_FR}[lang]
MSG = {'pt':MSG_PT,'en':MSG_EN,'fr':MSG_FR}[lang].format(P3D_LINK)

AI_EN = "Already installed and not working? Try the following:</p><ul><li>Restart your browser</li><li>Restart your computer</li></ul><p>If none of those work, <a href='bugreport.py'>report a bug</a>."
AI_PT  = "Já instalou e não está funcionando? Tente o seguinte:</p><ul><li>Reinicie seu navegador</li><li>Reinicie seu computador</li></ul><p>Se nada disso funcionar, <a href='bugreport.py'>reporte um bug</a>."
AI_FR  = "Déjà installé et le jeu ne se lance pas? Essayez ceci : </p><ul><li>Redémarrez votre navigateur</li><li>Redémarrez votre ordinateur</li></ul><p>Si aucune de ces actions ne marchent, merci de<a href='bugreport.py'>signaler un bug</a>."
AI = {'pt':AI_PT,'en':AI_EN,'fr':AI_FR}[lang].format(P3D_LINK)

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
                <p>{2}</p>
                <h3><a href="/play">{3}</a></h3>
            </div>
        </div>
    </body>
</html>
""".format(TITLE,MSG,AI,{'en':'Continue','fr':'Continuer','pt':'Continuar'}[lang])
