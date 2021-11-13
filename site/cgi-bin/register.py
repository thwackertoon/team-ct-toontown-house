#! /usr/bin/python
import cgitb
cgitb.enable()
import cgi, sys, os

print 'Content-Type: text/html;'
print

form = cgi.FieldStorage()

def _REQ(f):
    if not f in form:
        return ''
    return form[f].value
    
lang = _REQ('lang')
if not lang:
    if "HTTP_ACCEPT_LANGUAGE" in os.environ:
        lang = os.environ["HTTP_ACCEPT_LANGUAGE"][:2]
        
if not lang in ['pt','en']: lang = 'en'

link="/play"
        
def error(id):
    print (('Invalid fields! <a href="register.cgi">Go back</a>','Campos invalidos! <a href="register.cgi">Voltar</a>'),
           ('This username already exists! <a href="register.cgi">Go back</a>','Esse usuario ja existe!<a href="register.cgi">Voltar</a>'),
           ("Success! <a href="+link+">Download Toontown House</a>","Sucesso! <a href="+link+">Baixar Toontown House</a>"))[id][lang!='en']
           
    if error < 2: print_form()
    sys.exit()
    
if _REQ("do"):
    #register
    #check fields
    
    if not all((_REQ(x) for x in ['user','passwd'])): error(0)
    
    sys.path.append('/var/game')
    
    from Blob import newBlob
    if os.path.isfile('/var/game/data/blobs/'+_REQ('user')+'.blob'):
        error(1)
        
    b = newBlob('/var/game/data/blobs/'+_REQ('user')+'.blob')
    b.write('acc_passwd',_REQ('passwd'))
    b.write('acc_lang',lang)
    b.flush()
    
    error(2)
    
def print_form():
    _user = ("User","Usuario")[lang!='en']
    _pass = ("Password","Senha")[lang!='en']
    print """
    <html>
    <head><title>Toontown House</title></head>
    <body>
    <form action="register.cgi" method="POST">
    <input type="hidden" name="do" value="1">
    {0}: <input type="text" name="user"><br>
    {1}: <input type="password" name="passwd"><br>
    <input type="submit">
    </form>
    </body>
    </html>
    """.format(_user,_pass)
    
print_form()