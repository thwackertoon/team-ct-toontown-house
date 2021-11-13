from panda3d.core import *
from direct.showbase.DirectObject import *
from direct.gui.DirectGui import *
import types

def delFunc(cls,func):
    def _getname(obj): return str(obj).split()[2]
    def _hooked(name): raise AttributeError("this function (%s) has been disabled!" % name)
    name = _getname(func)
    setattr(cls,name,lambda *a,**kw:_hooked(name))

class ToonSpot:
    def __init__(self,index,data = {}):
        self.head = None
        self.name = None
        self.exists = False
        self.index = index
        self.data = data
        
    def __repr__(self):
        s = 'ToonSpot @ index %s;' % self.index
        s += 'Exists = %s;' % str(self.exists)
        if self.exists: s += 'Name = %s;' % str(self.name)
        if self.data: s += 'Data = %s;' % str(self.data)
        
        return s
        
class VirtualNP(NodePath):
    
    whitelist = (
                 'setPos','setX','setY','setZ',
                 'setHpr','setH','setP','setR',
                 'setScale','setSx','setSy','setSz',
                 'reparentTo','wrtReparentTo',
                 'copyTo','instanceTo',
                 'getTightBounds','calcTightBounds',
                 )

    def __init__(self,*a,**kw):
        NodePath.__init__(self,*a,**kw)
        
        for x in dir(self):
            if not x.startswith('__'): 
                if not x in self.whitelist:
                    x = getattr(self,x)
                    if type(x) == types.BuiltinMethodType:
                        delFunc(self,x)
                
class PATMgr(DirectObject):

    headEmotions = ("Normal","Angry","Sad","Smile","Laugh","Surprise")
    
    class modules:
        all = ['math']
        
        math = __import__("math")
    
    class HeadUtil:
        @staticmethod
        def getSize(head):
            p1, p2 = map(lambda x:x[2],head.getTightBounds())
            d = p2-p1
            return max(d,-d)
    
    def __init__(self,spots):
        self.spots = spots
        
        self.heads = []
        self.theme = None
        
        from direct.gui import DirectGui
        
        self.gui = DirectGui
        
    def selected(self,index):
        print 'selected',index
        
    def setTheme(self,theme):
        self.theme = theme
        
    def loadImage(self,image,transparent=False):
        x = OnscreenImage(self.theme.path+image,parent = hidden)
        if transparent: x.setTransparency(TransparencyAttrib.MAlpha)
        return x
 
    def _generateHeads(self,generator):
        for spot in self.spots:
            _head = None
            if spot.exists:
                data = map(spot.data.get,("toontype","color1","color2","color3","numb","gender"))
                _head = generator(*data)
                _head.setH(180)
                
                _head = VirtualNP(_head)
                
            self.heads.append(_head)
            
        delFunc(self,self._generateHeads)
