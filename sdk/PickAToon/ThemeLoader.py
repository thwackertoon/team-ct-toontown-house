from direct.gui.DirectGui import OnscreenImage
import os

class ThemeLoaderError(Exception): pass
class ThemeRuntimeError(Exception): pass

themebasepath = 'themes/'

class Theme:
    def __init__(self,path):
        self.bg = None
        self.scr = None
        self.path = path
        
    def __makeBuiltins(self,patMgr=None):
        b = __builtins__.copy() #{}
        
        funcs = [len,map,filter,dict,list,tuple,set,str,int,float,xrange,range]
        
        b["__import__"] = self.__hookedImport
        b["patMgr"] = patMgr
        b["__name__"] = "__main__"
        
        for x in funcs:
            b[str(x).split()[-1][:-1]] = x
        
        return b
        
    def __hookedImport(self,*args,**kw):
        raise ThemeRuntimeError("\nImport is disable for security reasons.\nIf you wanna use other modules, see patMgr.modules")
        
    def enter(self,patMgr):
        patMgr.setTheme(self)
        self.bg.reparentTo(base.cam2d) #render2d
        
        with open(self.scr) as f: 
            data = f.read()
            
            bt = self.__makeBuiltins(patMgr)
            exec data in {"__builtins__":bt},{}
        
def parseInfo(data):
    res = {}
    for i,x in enumerate(map(lambda x: x.strip(),data.replace('\r\n','\n').split('\n'))):
        x = x.split('//')[0]
        if not x: continue
        
        try: field,info = map(lambda x:x.strip(),x.split('=',1))
        except ValueError: raise ThemeLoaderError('Unable to parse line %s, badly formatted!' % str(i+1))
        
        res[field] = info
        
    return res

def loadTheme(name):
    if not os.path.exists(themebasepath+name):
        raise ThemeLoaderError("Unknown theme: "+name)
      
    themepath = themebasepath+name+'/'
    
    #read info
    if not os.path.exists(themepath+'info.pat'): raise ThemeLoaderError("Theme %s doesn't have info" % name)
    
    data = parseInfo(open(themepath+'info.pat','rb').read())
    
    #test data
    name = data.get("name")
    script = data.get("script")
    
    if not name: raise ThemeLoaderError('Invalid or not set name (%s)' % name)
    if not script: raise ThemeLoaderError('Invalid or not set script (%s)' % script)
    
    #fetch data folder
    if not os.path.exists(themepath+'data'): raise ThemeLoaderError("Theme %s doesn't have data" % name)
        
    datapath = themepath+'data/'
    _theme = Theme(themepath) 
    _theme.scr = themepath+script
    
    #get bg
    if not os.path.exists(datapath+'bg.png'): raise ThemeLoaderError("Theme %s doesn't have background" % name)
    _theme.bg = OnscreenImage(image=datapath+'bg.png',parent=hidden)
    
    return _theme