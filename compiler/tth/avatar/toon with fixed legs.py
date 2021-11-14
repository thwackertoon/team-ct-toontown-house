from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
#from direct.stdpy import glob
import __builtin__

def loadToonHead(toontype,color1,color2,color3,numb,anims={}):
    
    _version = '1.8.0'
    if pversion:
        _version=pversion
    
    head = Actor("data/models/toons/heads/{0}/{1}/{1}{2}.bam".format(_version,toontype,numb),anims)
    _color = Vec4(color1,color2,color3,1)
    
    for mesh in head.findAllMatches("**"):
        if not ("eye" in mesh.getName() or "muzzle" in mesh.getName() \
            or "1000" in mesh.getName() or "Actor" in mesh.getName() \
            or "dog" in mesh.getName() or "def_head" in mesh.getName() \
            or "nose" in mesh.getName() or "pupil" in mesh.getName() \
            or ("ears" in mesh.getName() and toontype=="dog")) and mesh.getName():
            
            mesh.setColor(_color,1)
            
    return head

rgb2p = lambda r,g,b: (r/255.,g/255.,b/255.)

class Toon:
    def __init__(self,np=None,toontype="cat",color_head=(.3,.3,.3),color_torso=(.3,.3,.3),
                 color_legs=(.3,.3,.3),body="s",gender="shorts",legsSz="s",headn=0,
                 autoShow=True,clt=(None,None,None),name=""):
        
        if np is None: np = render
        
        self._toon = np.attachNewNode('toon')
        self._toon.hide() # hiding avoids the idle-for-1-second-bug
        
        #if hasattr(__builtin__,"isCompiled"):
         #   glob = __builtin__.glob_copy
        #else:
          #  print 'Not compiled! Using standard glob...'
          #  import glob
          #  __builtin__.glob = glob
        
        _head_anims = {}
        
        for f in glob.glob("data/models/toons/dg{0}/{1}/head_*.bam".format(body,gender)):
            _a = f.split("_")[-1]
            _head_anims[_a.replace('/','\\').split('\\')[-1].split('.',1)[0]]="data/models/toons/dg{0}/{1}/head_{2}".format(body,gender,_a)
        
        _torso_anims = {}
        
        for f in glob.glob("data/models/toons/dg{0}/{1}/torso_*.bam".format(body,gender)):
            _a = f.split("_")[-1]
            _torso_anims[_a.replace('/','\\').split('\\')[-1].split('.',1)[0]]="data/models/toons/dg{0}/{1}/torso_{2}".format(body,gender,_a)
            
        _legs_anims = {}
        
        for f in glob.glob("data/models/toons/legs/legs{0}_*.bam".format(legsSz)):
            _a = f.split("_")[-1]
            _legs_anims[_a.replace('/','\\').split('\\')[-1].split('.',1)[0]]="data/models/toons/legs/legs{0}_{1}".format(legsSz,_a)
        
        self.head = loadToonHead(toontype,*color_head+(headn,_head_anims))

        self.torso = Actor("data/models/toons/dg{0}/{1}/torso_1000.bam".format(body,gender),
                                          _torso_anims)

        self.legs = Actor("data/models/toons/legs/legs{0}_1000.bam".format(legsSz),_legs_anims)
          
        self.legs.reparentTo(self._toon)
        #self.legs.loop("walk")
        self.legs.find("**/legs").setColor(*color_legs+(1,))
        self.legs.find("**/feet").setColor(*color_torso+(1,1))
        self.legs.find("**/shoes").remove()
        self.legs.find("**/boots_short").remove()
        self.legs.find("**/boots_long").remove()
        self.legs.setSz(self._toon,legsSz)
                
        self.torso.reparentTo(self.legs.exposeJoint(None,"modelRoot","joint_hips"))
        #self.torso.loop("walk")
        #self.torso.find("**/torso-top").setTexture(loader.loadTexture("data/torso_AA_texture_1.jpg"),1)
        #self.torso.find("**/torso-bot").setTexture(loader.loadTexture("data/torso_AB_texture_1.jpg"),1)
        self.torso.find("**/neck").setColor(*color_torso+(1,1))
        self.torso.find("**/arms").setColor(*color_torso+(1,1))
        #self.torso.find("**/sleeves").setColor(*color_torso+(1,1))
        self.torso.find("**/hands").setColor(1,1,1,1,1)
        
        self.torso.setSz(self._toon,1)
          
        self.head.reparentTo(self.torso.exposeJoint(None,"modelRoot","def_head"))
        self.head.setSz(self._toon,1)
        
        if autoShow: self._toon.show()
        
        #store stuff
        self.data = {
                    'toontype':toontype,
                    'color1':color_head,
                    'color2':color_torso,
                    'color3':color_legs,
                    'body':body,
                    'gender':gender,
                    'legs':legsSz,
                    'head':headn,
                    'clt':clt,
                    'name':name
                    }
        
        if any(clt):
            self.reTexture(*clt)
            
        self.hz = sum(map(lambda x: max(x[-1],-x[-1]),self._toon.getTightBounds()))
            
        self.tag = OnscreenText(scale=.75, text=unicode(self.data["name"].decode('latin-1')),bg=(.9,.9,.9,.3),fg=(0,0,1,1),wordwrap=8,decal=True)

        self.tag.setTextureOff()
        
        self.tag.setDepthTest(True)
        self.tag.setDepthWrite(True)
    
        self.tag.reparentTo(self._toon)
        self.tag.setZ(self.hz+1)
        
    def anim(self, *anims, **kw):
        #self.head.loop(anim, **kw) #head disappears when it is called
        parts = [self.legs,self.torso]        
        for i,part in enumerate(parts): part.loop(anims[min(i,len(anims)-1)], **kw)
        
    def setX(self, *args,**kw): self._toon.setX(*args,**kw)
    def setY(self, *args,**kw): self._toon.setY(*args,**kw)
    def setZ(self, *args,**kw): self._toon.setZ(*args,**kw)
    def setPos(self, *args,**kw): self._toon.setPos(*args,**kw)
    def setH(self, *args,**kw): self._toon.setH(*args,**kw)
    def setP(self, *args,**kw): self._toon.setP(*args,**kw)
    def setR(self, *args,**kw): self._toon.setR(*args,**kw)
    def setHpr(self, *args,**kw): self._toon.setHpr(*args,**kw)
    def setSx(self, *args,**kw): self._toon.setSx(*args,**kw)
    def setSy(self, *args,**kw): self._toon.setSy(*args,**kw)
    def setSz(self, *args,**kw): self._toon.setSz(*args,**kw)
    def setScale(self, *args,**kw): self._toon.setScale(*args,**kw)
    
    def reColor(self,color_head,color_torso,color_legs):
        self.legs.find("**/legs").setColor(*color_legs+(1,))
        self.legs.find("**/feet").setColor(*color_legs+(1,1))
                
        self.torso.find("**/neck").setColor(*color_torso+(1,1))
        self.torso.find("**/arms").setColor(*color_torso+(1,1))
        #self.torso.find("**/sleeves").setColor(*color_torso+(1,1))
        
        _color = Vec4(*color_head+(1,))
    
        for mesh in self.head.findAllMatches("**"):
            if not ("eye" in mesh.getName() or "muzzle" in mesh.getName() or "1000" in mesh.getName() or "Actor" in mesh.getName() \
            or "dog" in mesh.getName() or "def_head" in mesh.getName() \
            or "nose" in mesh.getName() \
            or ("ears" in mesh.getName() and self.data['toontype']=="dog")):
                mesh.setColor(_color,1)
                
        self.data['color1']=color_head
        self.data['color2']=color_torso
        self.data['color3']=color_legs
                
    def reTexture(self, top, bot, sleeves = None):
        self.torso.find("**/torso-top").setTexture(loader.loadTexture("data/models/toons/clothes/top{0}.jpg".format(top)),1)
        self.torso.find("**/torso-bot").setTexture(loader.loadTexture("data/models/toons/clothes/bot{0}.jpg".format(bot)),1)
        
        self.torso.find("**/sleeves").setTexture(L10N.getSleeveTexture()[1],1)
        
        self.data['clt'] = (top, bot, sleeves)

class EToon:
    def __init__(self,np=None,toontype="cat",color_head=(.3,.3,.3),color_torso=(.3,.3,.3),
                 color_legs=(.3,.3,.3),body="s",gender="shorts",legsSz=.5,headn=0,
                 autoShow=True,clt=(None,None,None),name="",extraDnaStuff = {}):
        
        if np is None: np = render
        
        self._toon = np.attachNewNode('toon')
        self._toon.hide() # hiding avoids the idle-for-1-second-bug
        
        #if hasattr(__builtin__,"isCompiled"):
         #   glob = __builtin__.glob_copy
        #else:
         #   print 'Not compiled! Using standard glob...'
          #  import glob
           # __builtin__.glob = glob
        
        #print 'EToon.Glob:',glob,glob.glob,glob.glob("data/models/toons/dg{0}/{1}/legs_*.bam".format(body,gender))
        
        _head_anims = {}
        
        for f in glob.glob("data/models/toons/dg{0}/{1}/head_*.bam".format(body,gender)):
            _a = f.split("_")[-1]
            _head_anims[_a.replace('/','\\').split('\\')[-1].split('.',1)[0]]="data/models/toons/dg{0}/{1}/head_{2}".format(body,gender,_a)
        
        _torso_anims = {}
        
        for f in glob.glob("data/models/toons/dg{0}/{1}/torso_*.bam".format(body,gender)):
            _a = f.split("torso_")[-1]
            _torso_anims[_a.replace('/','\\').split('\\')[-1].split('.',1)[0]]="data/models/toons/dg{0}/{1}/torso_{2}".format(body,gender,_a)
            
        _legs_anims = {}
        
        for f in glob.glob("data/models/toons/legs/legs_*.bam"):
            _a = f.split("legs_")[-1]
            #print _a
            _legs_anims[_a.replace('/','\\').split('\\')[-1].split('.',1)[0]]="data/models/toons/legs/legs_"+_a       
        
        self.head = loadToonHead(toontype,*color_head+(headn,_head_anims))
        self.torso = loader.loadModel("data/models/toons/dg{0}/{1}/torso_1000.bam".format(body,gender))
        
        self.torso.find("**/neck").setColor(*color_torso+(1,1))
        self.torso.find("**/arms").setColor(*color_torso+(1,1))
        #self.torso.find("**/sleeves").setColor(*color_torso+(1,1))
        self.torso.find("**/hands").setColor(1,1,1,1,1)
        
        self.legs = loader.loadModel("data/models/toons/legs/legs_1000.bam")
        
        self.legs.find("**/legs").setColor(*color_legs+(1,))
        self.legs.find("**/feet").setColor(*color_torso+(1,1))
        self.legs.find("**/shoes").remove()
        self.legs.find("**/boots_short").remove()
        self.legs.find("**/boots_long").remove()
        self.legs.setSz(legsSz)
          
        self._m = Actor({'head':self.head, 'torso':self.torso,'legs':self.legs},{'torso':_torso_anims, 'legs':_legs_anims})
        self._m.reparentTo(self._toon)
        
        self._m.attach("head","torso","def_head")
        self._m.attach("torso","legs","joint_hips")
        
        if autoShow: self._toon.show()
        
        #store stuff
        self.data = {
                    'toontype':toontype,
                    'color1':color_head,
                    'color2':color_torso,
                    'color3':color_legs,
                    'body':body,
                    'gender':gender,
                    'legs':legsSz,
                    'head':headn,
                    'clt':clt,
                    'name':name
                    }
        
        self.data.update(extraDnaStuff)
        
        if any(clt):
            #print 'Setting texture...'
            self.reTexture(*clt)
            
        self.hz = sum(map(lambda x: max(x[-1],-x[-1]),self._toon.getTightBounds()))
        
        self._toon.setScale(.65)
        
        self.tag = OnscreenText(scale=.75,font=BTFont,text=unicode(self.data["name"].decode('latin-1')),bg=(.9,.9,.9,.3),fg=(0,0,1,1),wordwrap=8,decal=True)

        self.tag.setTextureOff()
        self.tag.setBillboardAxis()
        
        self.tag.setDepthTest(True)
        self.tag.setDepthWrite(True)
    
        self.tag.reparentTo(self._m)
        self.tag.setZ(self.hz+1)
        
    def anim(self, anim, playRate=1.0):
        ActorInterval(self._m, anim, playRate=playRate).loop()
        
    def pose(self, anim, frame):
        ActorInterval(self._m, anim, startFrame=frame, endFrame=frame+1).loop()
        
    def setX(self, *args,**kw): self._toon.setX(*args,**kw)
    def setY(self, *args,**kw): self._toon.setY(*args,**kw)
    def setZ(self, *args,**kw): self._toon.setZ(*args,**kw)
    def setPos(self, *args,**kw): self._toon.setPos(*args,**kw)
    def setH(self, *args,**kw): self._toon.setH(*args,**kw)
    def setP(self, *args,**kw): self._toon.setP(*args,**kw)
    def setR(self, *args,**kw): self._toon.setR(*args,**kw)
    def setHpr(self, *args,**kw): self._toon.setHpr(*args,**kw)
    def setSx(self, *args,**kw): self._toon.setSx(*args,**kw)
    def setSy(self, *args,**kw): self._toon.setSy(*args,**kw)
    def setSz(self, *args,**kw): self._toon.setSz(*args,**kw)
    def setScale(self, *args,**kw): self._toon.setScale(*args,**kw)
    
    def reColor(self,color_head,color_torso,color_legs):
        self.legs.find("**/legs").setColor(*color_legs+(1,))
        self.legs.find("**/feet").setColor(*color_legs+(1,1))
                
        self.torso.find("**/neck").setColor(*color_torso+(1,1))
        self.torso.find("**/arms").setColor(*color_torso+(1,1))
        #self.torso.find("**/sleeves").setColor(*color_torso+(1,1))
        
        _color = Vec4(*color_head+(1,))
    
        for mesh in self.head.findAllMatches("**"):
            if not ("eye" in mesh.getName() or "muzzle" in mesh.getName() or "1000" in mesh.getName() or "Actor" in mesh.getName() \
            or "dog" in mesh.getName() or "def_head" in mesh.getName() \
            or "nose" in mesh.getName() \
            or ("ears" in mesh.getName() and self.data['toontype']=="dog")):
                mesh.setColor(_color,1)
                
        self.data['color1']=color_head
        self.data['color2']=color_torso
        self.data['color3']=color_legs
                
    def reTexture(self, top, bot, sleeves = None):
        self._m.find("**/torso-top").setTexture(loader.loadTexture("data/models/toons/clothes/top{0}.jpg".format(top)),1)
        self._m.find("**/torso-bot").setTexture(loader.loadTexture("data/models/toons/clothes/bot{0}.jpg".format(bot)),1)
        
        if sleeves:
            print 'SLEEVES SET',sleeves,'!!'
            self._m.find("**/sleeves").setTexture(loader.loadTexture("data/models/toons/sleeves/{0}.png".format(sleeves)),1)
        else:
            sleeves,_tex = L10N.getSleeveTexture()
            self._m.find("**/sleeves").setTexture(_tex,1)
        
        self.data['clt'] = (top, bot, sleeves)

    def makeDna(self): return make_buffer(self.data)