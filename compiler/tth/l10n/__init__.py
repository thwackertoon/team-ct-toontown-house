#Translation system
from random import choice
import locale
#from direct.stdpy.file import open

findpath = lambda x: x #gamebase.findpath

class l10n:
    def __init__(self,language):
        self.languages = {
                          'pt':'pt.l10n',
                          'en':'english.l10n',
						  'fr':'french.l10n',
                          }
                          
        self._sleeve = None
        self.setLanguage(language)
        #self.buildDB()
        
    def buildDB(self):
        self.db = {}
        f = open(findpath('data/etc/languages/'+self.languages[self.language]),'rb')
        for line in f.read().replace('\r','\n').split('\n'):
            line = line.strip('\r\n')
            if not line or line.startswith('#'): continue
            _d = line.split('#',1)[0].split(' ',1)
            #print _d
            self.db[_d[0]] = unicode(_d[1].decode('latin-1'))
            
    def sc_buildDB(self):
        self.sc_db = {}
        f = open(findpath('data/etc/languages/speedchat_'+self.language.upper()+'.l10n'),'rb')
        for line in f.read().replace('\r','\n').split('\n'):
            line = line.strip('\r\n')
            if not line or line.startswith('#'): continue
            _d = line.split('#',1)[0].split(' ',1)
            #print _d
            self.sc_db[_d[0]] = unicode(_d[1].decode('latin-1'))
            
    def sc_fetch(self,_str):
        #print 'fetching',_str
        rs = []
        if _str.endswith("*"):
            for item,val in self.sc_db.items():
                if item.startswith(_str[:-1]):
                    rs.append((val,item))
        
        elif _str.endswith("%"):
            for item,val in self.sc_db.items():
                if item.startswith(_str[:-1]) and not '_' in item[len(_str):] and len(self.sc_fetch(item+"_*"))<=1:
                    #print 'L10N::_%',item,item[len(_str):]
                    rs.append((val,item))
                    
        else:
            if not _str in self.sc_db:
                print ":l10n:SC: Unknown: {0} (LANG={1})".format(_str,self.language)
                rs.append(u"L10N 0x001: NOT FOUND")
            else:
                rs.append((self.sc_db[_str],_str))
                
        return rs
        
    def getSleeveTexture(self):
        if self._sleeve: return self._sleeve
        country = locale.getdefaultlocale()[0][3:].lower()
        print ':l10n: Setting sleeve flag for',country
        self._sleeve = (country,loader.loadTexture("data/models/toons/sleeves/{0}.png".format(country)))
        return self._sleeve
            
    def tip(self): #returns a random tip in selected language
        messages=[unicode(m.decode('latin-1')) for m in open(findpath("data/etc/languages/{0}.tips").format(self.language)).readlines()]
        if not messages:
            raise ToontownHouseError('l10n 0x002: NO TIPS AVAIABLE FOR '+self.language)
        
        return choice(messages)
        
    def setLanguage(self,language):
        if not language in self.languages:
            raise ToontownHouseError('l10n 0x000: Invalid language!')
            
        self.language = language
        self.buildDB()
        self.sc_buildDB()
        
    def __call__(self,_str):
        if not _str in self.db:
            print ":l10n: Unknown: {0} (LANG={1})".format(_str,self.language)
            return u"L10N 0x001: NOT FOUND"
        return self.db[_str]