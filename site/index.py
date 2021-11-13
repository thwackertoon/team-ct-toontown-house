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

def _getHeader():
    greetingText = {
        'en':'Register | Login',
        'fr':'S\'enregistrer | Connexion',
        'pt':'Registar | Entrar'
        }[lang]
        
    if SESS.exists('user'):
        #oh we got an user logged, say hi
        greetingText = {
        'en':'Hi, ',
        'fr':'Bonjour, ',
        'pt':'Oi, '
        }[lang]+SESS.read('user')+'! <span style="font-size:20px;"><a href="/logout.py">{0}</a></span>'.format(
                                                                                                        {
                                                                                                        'pt':'Sair',
                                                                                                        'en':'Logout',
                                                                                                        'fr':'Déconneter',
                                                                                                        }[lang])
        
    else:
        greetingText = '<a href="register.py">'+greetingText.replace(' | ','</a> | <a href="login.py">')+'</a>'
        
    data = '<img src="header.png"></img> \
            <div style="font-size:40px;">{0}</div> \
            </img>'.format(greetingText)
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
            <h2><a href="/play">{1}</a></h2>
        </div>
    </body>
</html>
""".format(_getHeader(),{'pt':'Jogar agora!','en':'Play now!','fr':'Jouer maintenant!'}[lang])