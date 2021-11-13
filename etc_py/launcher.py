#!!! NEED PYGTK AND IMPRESSBT FONT INSTALLED!!!
#DONT EVEN TRY TO EDIT THIS FILE !!!
import pygtk
pygtk.require('2.0')
import gtk

try:
    newsfile = urllib2.urlopen('http://toontownhouse.org/d3v/news.xml')
    newstext = newsfile.read()
    newsfile.close()
    connected = True
except urllib2.URLError:
    connected = False

if connected != False:
    dom = parseString(newstext)
    print("news.xml parsed")
#Classing all tags
    page = dom.getElementsByTagName('page')[0].toxml()
    titletag = dom.getElementsByTagName('title')[0].toxml()
    desctag = dom.getElementsByTagName('desc')[0].toxml()
#Getting data from tags only
    pagect = page.replace('<page>','').replace('</page>','')
    titles = titletag.replace('<title>','').replace('</title>','')
    descs = desctag.replace('<desc>','').replace('</desc>','')
    print("Got news.xml content")
else:
    print("Can't parse XML, no connexion to server")
    
    
class Launcher:
    def destroy(self, widget, data=None):
        gtk.main_quit()
        
    def __init__(self):
        self.window = gtk.Window()
        self.window.connect("destroy", self.destroy)
        self.window.set_title("Toontown House Launcher")
        #self.window.set_decorated(False) (remove the frame)
        #creating boxes
        self.winvbox = gtk.VBox(False, 10)
        self.inputs = gtk.VBox(False, 0)
        self.user = gtk.HBox(False, 0)
        self.paswd = gtk.HBox(False, 0)
        self.logo = gtk.Image()
        #self.logo.set_from_file("tth_logo.png")
        #inputs
        self.usne = gtk.Entry()
        self.lusne = gtk.Label("Username :")
        self.conbut = gtk.Button("Connect")
        self.lpswd = gtk.Label("Password :")
        self.opbut = gtk.Button("Options")
        self.pswd = gtk.Entry()
        self.pswd.set_invisible_char("*")
        self.pswd.set_visibility(False)
        self.checknos = gtk.CheckButton("Play in Nostalgia mode ?")
        #news
        self.lister = gtk.TextView(self.news)
        #adding the content into the window
        self.window.get_settings().set_string_property('gtk-font-name', 'Impress BT 20','');
        self.winvbox.pack_start(self.logo, True, False, 0)
        self.user.pack_start(self.lusne, True, False, 0)
        self.user.pack_start(self.usne, True, False, 0)
        self.user.pack_start(self.conbut, True, False, 0)
        self.paswd.pack_start(self.lpswd, True, False, 0)
        self.paswd.pack_start(self.pswd, True, False, 0)
        self.paswd.pack_start(self.opbut, True, False, 0)
        self.inputs.pack_start(self.user, True, False, 0)
        self.inputs.pack_start(self.paswd, True, False, 0)
        self.inputs.pack_start(self.checknos, True, False, 0)
        self.winvbox.pack_start(self.inputs, True, False, 0)
        self.winvbox.pack_start(self.lister, True, False, 0)
        self.window.add(self.winvbox)
        self.window.show_all()
    def main(self):
           gtk.main()

if __name__ == "__main__":
    Launch = Launcher()
    Launch.main()