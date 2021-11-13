#!/usr/bin/python
#coding: latin-1

import cgitb
cgitb.enable()

import sys, os, hashlib
sys.path.append('C:/temp/Web_Server/www/127.0.0.1/ToontownHouse/var/game')
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

__REGISTER,__USERNAME,__PASSWD,__CONF_PASSWD,PWDRULES,EMAILRULES = map(lambda x:x[lang],(
                                                                     {
                                                                      'en':'Register',
                                                                      'fr':'Enregistrer',
                                                                      'pt':'Registro',
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
                                                                     {
                                                                      'en':'Retype the password',
                                                                      'fr':'Retapez le mot de passe',
                                                                      'pt':'Redigite a senha',
                                                                     },
                                                                     {
                                                                      'en':'Must have only letters and/or numbers and 6-20 chars',
                                                                      'fr':'Doit avoir que des lettres et/ou chiffres et de 6 à 20 caractères',
                                                                      'pt':'Deve ter apenas letras e/ou números e de 6 a 20 caracteres',
                                                                     },
                                                                     {
                                                                      'en':'We/'ll send the activation code to this email!',
                                                                      'fr':'Nous enverrons le code d/'activation à cet e-mail!',
                                                                      'pt':'Vamos enviar o código de ativação pra esse email!',
                                                                     },
                                                                    )
                                                                    )
    
def _getHeader():
    data = '<img src="header.png"></img>'
    return data

def error_inuse():
    print("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Toontown House</title>
        <script>
            function isValidUser(u) {{
                return (/[^a-zA-Z0-9]/.test(u) == false) && u.length >= 6 && u.length <= 20;
            }}
            function checkUser() {{
               u = document.getElementById('user');
               p = u.value;
               if (!isValidUser(p)) u.style.backgroundColor = "#FF0000";
               else u.style.backgroundColor = "#00FF00";
            }}
            function checkPwd() {{
               u = document.getElementById('password');
               p = u.value;
               if (!isValidUser(p)) u.style.backgroundColor = "#FF0000";
               else u.style.backgroundColor = "#00FF00";
            }}
            function checkPwd2() {{
               u = document.getElementById('password');
               u2 = document.getElementById('password2');
               p = u.value;
               p2 = u2.value;
               console.debug(p+' -> '+p2+(p==p2));
               if ((p==p2) && (p.length > 1)) u2.style.backgroundColor = "#00FF00";
               else u2.style.backgroundColor = "#FF0000";
            }}
            function isGoodToGo() {{
               u = document.getElementById('password').value;
               u2 = document.getElementById('password2').value;
               u3 = document.getElementById('user').value;
               if (isValidUser(u3) && isValidUser(u) && (u2==u)) return true;
               else {{alert('Please review the fields!');return false;}}
               
            }}
        </script>
    </head>
    <body style="background-image:url(bg.png);background-size:100% 100%;height:100%;background-repeat:no-repeat;background-attachment:fixed;">
        <div id="wrapper" style="text-align: center; width: 50%; height: 100%; display: table; margin: 0px auto; background-color: rgba(255, 255, 255, .75);">
            <div id="header">
            {0}
            </div>
            <div id="theform">
                <span id="error" width="100%" style="background-color:#FF0000;font-color:#FFFFFF;">{7}</span>
                <h1>{1}</h1>
                <form action="register.py" method="POST" onSubmit="return isGoodToGo();">
                    <span id="s">{2}:</span><br><input type="text" name="user" id="user" onchange="checkUser();"></input><br><span>{5}</span><br><br>
                    <span id="s">{3}:</span><br><input type="password" name="password" id="password" onchange="checkPwd();"></input><br><span>{5}</span><br><br>
                    <span id="s">{4}:</span><br><input type="password" name="password2" id="password2" onkeyup="checkPwd2();"></input><br><br>
                    <span id="s">E-mail:</span><br><input type="email" name="email" id="email"></input><br><span>{6}</span><br><br>
                    <br>
                    <input type="submit"></input>
                <form/>
            </div>
        </div>
    </body>
    </html>
    """.format(_getHeader(),__REGISTER,__USERNAME,__PASSWD,__CONF_PASSWD,PWDRULES,EMAILRULES,{'en':'This username is already in use!','fr':'Ce nom d/'utilisateur est déjà utilisé!','pt':'Esse usuário já está em uso!'}[lang]))
    sys.exit()
    
def success(email):
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
            <span>{1}</span>
        </div>
    </body>
    </html>
    """.format(_getHeader(),{'en':'An email has been sent to {0}. Please check your mailbox to continue!',
                         'pt':'Um email foi enviado para {0}. Verifique sua caixa de entrada para continuar!',
                         'fr':'Un e-mail a été envoyé à {0}. S/'il vous plaît vérifier votre boîte aux lettres pour continuer!'}[lang].format(email)))
    sys.exit()
    
def sendTheEmail(email,user,link):
    import smtplib

    SERVER = "localhost"

    FROM = "donotreply@toontownhouse.net"
    TO = [email] # must be a list

    SUBJECT = {
                "en":"Account activation at Toontown House",
                "pt":"Ativação de conta em Toontown House",
                "fr":"Activez votre compte sur Toontown House",
              }[lang]

    TEXT = {
            "en":"Hi, {0}!/nYou have created an account at Toontown House!/nPlease click on the following link to activate /
                  your account:/n/n{1}/n/nIf you can't click this link, copy and paste in your browser./n/nHave fun,/nTeam CT",
            "pt":"Oi, {0}!/nVocê criou uma conta em Toontown House!/nPor favor, clique no link a seguir para ativar /
                  sua conta:/n/n{1}/n/nSe você não consegue clicar nesse link, copie e cole no seu navegador./n/nDivirta-se,/nTeam CT",
            "fr":"Salut, {0}!/nVous avez créé un compte sur Toontown House!/nS'il vous plaît cliquer sur le lien ci-dessous pour activer /
                  votre compte:/n/n{1}/n/nSi vous ne pouvez pas cliquer sur ce lien, copier et coller sur votre navigateur./n/nProfitez-en, l'équipe CT",
            }[lang].format(user,link)

    # Prepare actual message

    message = """/
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    # Send the mail

    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, message)
    server.quit()
    
user = spsl.get('user')
if user:
    passw = spsl.get('password')
    email = spsl.get('email')
    
    if os.path.isfile('C:/temp/Web_Server/www/127.0.0.1/ToontownHouse/var/game/blob/'+user+'.blob'):
        error_inuse()
        
    b = spsl.newBlob('C:/temp/Web_Server/www/127.0.0.1/ToontownHouse/var/game/blob/'+user+'.blob')
    passw = hashlib.md5(hashlib.sha256(passw).digest()).hexdigest()[::-1]
    b.write('acc_passwd',passw)
    b.write('acc_email',email)
    b.write('acc_email_act','0')
    b.flush()
    
    _file=""
    while os.path.exists(os.path.join("/var/tmp/mailcodes",_file)):
        _file = os.urandom(24).encode('base64').strip().replace(' ','1').replace('/','2').replace('+','3')
    
    open(os.path.join("/var/tmp/mailcodes",_file),"wb").write(user)
    link = 'https://www.toontownhouse.net/ec.py?code='+_file
    sendTheEmail(email,user,link)
    success(email)

print """
<!DOCTYPE html>
<html>
    <head>
        <title>Toontown House</title>
        <script>
            function isValidUser(u) {{
                return (/[^a-zA-Z0-9]/.test(u) == false) && u.length >= 6 && u.length <= 20;
            }}
            function checkUser() {{
               u = document.getElementById('user');
               p = u.value;
               if (!isValidUser(p)) u.style.backgroundColor = "#FF0000";
               else u.style.backgroundColor = "#00FF00";
            }}
            function checkPwd() {{
               u = document.getElementById('password');
               p = u.value;
               if (!isValidUser(p)) u.style.backgroundColor = "#FF0000";
               else u.style.backgroundColor = "#00FF00";
            }}
            function checkPwd2() {{
               u = document.getElementById('password');
               u2 = document.getElementById('password2');
               p = u.value;
               p2 = u2.value;
               console.debug(p+' -> '+p2+(p==p2));
               if ((p==p2) && (p.length > 1)) u2.style.backgroundColor = "#00FF00";
               else u2.style.backgroundColor = "#FF0000";
            }}
            function isGoodToGo() {{
               u = document.getElementById('password').value;
               u2 = document.getElementById('password2').value;
               u3 = document.getElementById('user').value;
               if (isValidUser(u3) && isValidUser(u) && (u2==u)) return true;
               else {{alert('Please review the fields!');return false;}}
               
            }}
        </script>
    </head>
    <body style="background-image:url(bg.png);background-size:100% 100%;height:100%;background-repeat:no-repeat;background-attachment:fixed;">
        <div id="wrapper" style="text-align: center; width: 50%; height: 100%; display: table; margin: 0px auto; background-color: rgba(255, 255, 255, .75);">
            <div id="header">
            {0}
            </div>
            <div id="theform">
                <h1>{1}</h1>
                <form action="register.py" method="POST" onSubmit="return isGoodToGo();">
                    <span id="s">{2}:</span><br><input type="text" name="user" id="user" onchange="checkUser();"></input><br><span>{5}</span><br><br>
                    <span id="s">{3}:</span><br><input type="password" name="password" id="password" onchange="checkPwd();"></input><br><span>{5}</span><br><br>
                    <span id="s">{4}:</span><br><input type="password" name="password2" id="password2" onkeyup="checkPwd2();"></input><br><br>
                    <span id="s">E-mail:</span><br><input type="email" name="email" id="email"></input><br><span>{6}</span><br><br>
                    <br>
                    <input type="submit"></input>
                <form/>
            </div>
        </div>
    </body>
</html>
""".format(_getHeader(),__REGISTER,__USERNAME,__PASSWD,__CONF_PASSWD,PWDRULES,EMAILRULES)
