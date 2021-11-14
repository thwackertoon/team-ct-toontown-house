from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import ToonGlobber

from ToonHead import ToonHead
class HookedHead(ToonHead):
    def __init__(self,head,color,gender):
        self.head = head
        
        self.color = color
        self.gender = gender
        
        ToonHead.__init__(self)
        self.setupHead(self,False)
        
    def getGender(self): return self.gender
    def getHeadColor(self): return self.color
    def getAnimal(self):
        return {'d': 'dog','c': 'cat','h': 'horse',
                'm':'mouse','r':'rabbit','f':'duck',
                'p':'monkey','b':'bear','s':'pig'}[self.head[0]]
                
    def setColorFromActor(self,actor,color):
        color = Vec4(color+(1,))
        parts = actor.findAllMatches('**/head*')
        parts.setColor(color)
        animalType = self.getAnimal()
        if animalType == 'cat' or animalType == 'rabbit' or animalType == 'bear' or animalType == 'mouse' or animalType == 'pig':
            parts = actor.findAllMatches('**/ear?-*')
            parts.setColor(color)

def loadToonHead(toontype,color1,color2,color3,numb,gender,animMode = 1):

    _color = Vec4(color1,color2,color3,1)
    
    tt = {'d': 'dog','c': 'cat','h': 'horse','m':'mouse','r':'rabbit','f':'duck','p':'monkey','b':'bear','s':'pig'}
    tt = dict(zip(tt.values(),tt.keys()))[toontype]
    
    if tt[0] == "m": numb %= 2
    tt += (("ss","sl","ls","ll"),("ss","ls"))[tt=="m"][int(numb)]
    
    _gender = gender.lower()
    if len(_gender) != 1: _gender = {"shorts":"m","skirt":"f"}[_gender]
    
    print 'HEAD DNA HOOKER: CONVERTED:',toontype,numb,gender,'->',tt,_gender
    
    head = HookedHead(tt,_color,_gender)
    
    lookAround,blink =  map(lambda x:bool(int(x)),str(bin(animMode))[2:].ljust(2,'0'))
    if lookAround: head.startLookAround()
    if blink: head.startBlink()
            
    return head

rgb2p = lambda r,g,b: (r/255.,g/255.,b/255.)

class EToon:
    ANIMS = ToonGlobber.smartScan()
    
    def __init__(self,np=None,toontype="cat",color_head=(.3,.3,.3),color_torso=(.3,.3,.3),
                 color_legs=(.3,.3,.3),body="s",gender="shorts",legsSz=.5,headn=0,
                 autoShow=True,clt=(None,None,None),name="",extraDnaStuff = {}):
        
        if np is None: np = render
        
        self._toon = np.attachNewNode('toon')
        self._toon.hide() # hiding avoids the idle-for-1-second-bug
                
        _torso_anims = {}

        for f in ToonGlobber.loadTorsoAnims(self.ANIMS,gender,body):
            _a = f.split("torso_")[-1]
            _torso_anims[_a.split('/')[-1].split('.',1)[0]] = f
            
        _legs_anims = {}
        
        __lf = {.5:'s',.75:'m',1:'l'}[legsSz]
        for f in ToonGlobber.loadLegsAnims(self.ANIMS,gender,__lf):
            _a = f.split("legs_")[-1]
            _legs_anims[_a.split('/')[-1].split('.',1)[0]] = f     
        
        self.head = loadToonHead(toontype,*color_head+(headn,gender))
        self.torso = loader.loadModel("phase_3/models/char/tt_a_chr_dg{0}_{1}_torso_1000".format(body,gender))
        
        self.torso.find("**/neck").setColor(*color_torso+(1,1))
        self.torso.find("**/arms").setColor(*color_torso+(1,1))
        self.torso.find("**/hands").setColor(1,1,1,1,1)
        
        self.legs = loader.loadModel("phase_3/models/char/tt_a_chr_dg{0}_shorts_legs_1000".format(__lf))
        
        self.legs.find("**/legs").setColor(*color_legs+(1,))
        self.legs.find("**/feet").setColor(*color_torso+(1,1))
        self.legs.find("**/shoes").remove()
        self.legs.find("**/boots_short").remove()
        self.legs.find("**/boots_long").remove()
          
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
        
        self.tag = OnscreenText(scale=.50,font=loader.loadFont("phase_3/models/fonts/ImpressBT.ttf"),
                                text=unicode(self.data["name"].decode('latin-1')),
                                bg=(.9,.9,.9,.3),fg=(0,0,1,1),wordwrap=8,decal=True)

        self.tag.setTextureOff()
        self.tag.setBillboardAxis()
        self.tag.reparentTo(self._m.find("**/def_head"))
        self.tag.setZ(.2)
        
        self.tag.setDepthTest(True)
        self.tag.setDepthWrite(True)

        self.tag.setZ(1.2)

    def GMIcon(self,icontype,extra,parent): #resistance = fistIcon, getConnected = whistleIcon, whistle = whistleIcon
        self.icon = loader.loadModel("data/models/toons/icons/{0}.bam".format(icontype)).find("**/"+extra)
        self.icon.reparentTo(gamebase.toonAvatar[0]._m.find("**/def_head"))
        #self.icon.setZ(1) #Ever up from tag
        self.icon.setScale(2)
        self.intrval = self.icon.hprInterval(600, (100,0,0),other=self.icon)
        self.intrval.start()
        self.intrval.loop()
        
    def anim(self, anim, playRate=1.0, loop = True):
        #print 'ANIM!',anim,loop
        i = ActorInterval(self._m, anim, playRate=playRate, loop=loop)
        if loop: i.loop()
        else: i.start()
        
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
        self._m.find("**/legs").setColor(*color_legs+(1,))
        self._m.find("**/feet").setColor(*color_legs+(1,1))
                
        self._m.find("**/neck").setColor(*color_torso+(1,1))
        self._m.find("**/arms").setColor(*color_torso+(1,1))
        #self.torso.find("**/sleeves").setColor(*color_torso+(1,1))

        #reload head
        self.head.setColorFromActor(self._m,color_head)
                
        self.data['color1']=color_head
        self.data['color2']=color_torso
        self.data['color3']=color_legs
                
    def reTexture(self, top, bot, sleeves = None):
        self._m.find("**/torso-top").setTexture(loader.loadTexture("data/models/toons/clothes/top{0}.jpg".format(top)),1)
        self._m.find("**/torso-bot").setTexture(loader.loadTexture("data/models/toons/clothes/bot{0}.jpg".format(bot)),1)
        
        if sleeves:
            self._m.find("**/sleeves").setTexture(loader.loadTexture("data/models/toons/sleeves/{0}.png".format(sleeves)),1)
        else:
            sleeves,_tex = L10N.getSleeveTexture()
            self._m.find("**/sleeves").setTexture(_tex,1)
        
        self.data['clt'] = (top, bot, sleeves)

    def makeDna(self): return make_buffer(self.data)
