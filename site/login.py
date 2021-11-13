#!/usr/bin/python
#coding: latin-1

import cgitb
cgitb.enable()

import sys, os, hashlib
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

__FAILED,__USERNAME,__PASSWD = map(lambda x:x[lang],(
                                                                     {
                                                                      'en':('Login failed!','This account hasn\'t been activated yet! Verify your activation email!'),
                                                                      'fr':('Connexion échouée!','Ce compte n\'a pas encore été activé ! Vérifiez votre email d\'activation!'),
                                                                      'pt':('O login falhou!','Essa conta ainda não foi ativada! Verifique seu email de ativação!</a>'),
                                                                     },
                                                                     {
                                                                      'en':'Username',
                                                                      'fr':'Pseudonyme',
                                                                      'pt':'Usuário',
                                                                     },
                                                                     {
                                                                      'en':'Password',
                                                                      'fr':'Mot de passe',
                                                                      'pt':'Senha',
                                                                     },                                               
                                                                    ))
    
def _getHeader():
    data = '<img src="header.png"></img>'
    return data

def error(code):
    print("""
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
            <div id="theform">
                <span id="error" width="100%" style="background-color:#FF0000;font-color:#FFFFFF;">{1}</span>
                <h1>Login</h1>
                <form action="login.py" method="POST">
                    <span id="s">{2}:</span><br><input type="text" name="user" id="user"></input><br><br>
                    <span id="s">{3}:</span><br><input type="password" name="password" id="password"></input><br><br>
                    <br>
                    <input type="submit"></input>
                <form/>
            </div>
        </div>
    </body>
    </html>
    """.format(_getHeader(),__FAILED[code],__USERNAME,__PASSWD))
    sys.exit()
    
def success(user):
    SESS.write('user',user,0)
    SESS.flush()
    print """
    <!DOCTYPE html>
    <html><head><META http-equiv="refresh" content="0;URL=/"> </head></html>
    """
    sys.exit()
    
user = spsl.get('user')
if user:
    passw = spsl.get('password')
    passw = hashlib.md5(hashlib.sha256(passw).digest()).hexdigest()[::-1]
    
    if not os.path.isfile('C:/temp/Web_Server/www/127.0.0.1/ToontownHouse/var/game/blob/'+user+'.blob'):
        error(0)
        
    b = spsl.Blob('C:/temp/Web_Server/www/127.0.0.1/ToontownHouse/var/game/blob/'+user+'.blob')
    acc_passw = b.read('acc_passwd')
    if passw != acc_passw:
        error(0)
        
    if b.read('acc_email_act') == '0':
        error(1)

    success(user)

print("""
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
            <div id="theform">
                <h1>Login</h1>
                <form action="login.py" method="POST">
                    <span id="s">{1}:</span><br><input type="text" name="user" id="user"></input><br><br>
                    <span id="s">{2}:</span><br><input type="password" name="password" id="password"></input><br><br>
                    <br>
                    <input type="submit"></input>
                <form/>
            </div>
        </div>
    </body>
    </html>
    """.format(_getHeader(),__USERNAME,__PASSWD))
