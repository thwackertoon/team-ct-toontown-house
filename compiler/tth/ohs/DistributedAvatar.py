#from direct.distributed.DistributedNode import DistributedNode
from direct.distributed.DistributedSmoothNode import DistributedSmoothNode #as DistributedNode
from direct.controls.GravityWalker import GravityWalker
from direct.actor.Actor import Actor
from pandac.PandaModules import *
from tth.avatar.toon import *
from tth.avatar.ToonAvatarPanel import ToonAvatarPanel as TAP

from AvatarFSM import AvatarFSM

class DistributedAvatar(DistributedSmoothNode):
    def __init__(self, cr):
        DistributedSmoothNode.__init__(self, cr)
        NodePath.__init__(self, 'avatar')
        
        self.sb = None

        self.toon = EToon(self,autoShow=False)
        self._toon = self.toon._toon
        self.avatar = self.toon._m
        self._m = self.avatar
        self.model = self.avatar
        self._toon.hide()
        self.dna = self.toon.makeDna()
        self._state = ("Neutral","None")
            
        self.isLocalToon = False
        
    def setState(self,state,arg):
        self._state = (state,arg)
        self.fsm.request(state,arg)
        
    def d_setState(self,state,arg="None"): self.sendUpdate("setState",[state,arg])
    def b_setState(self,state,arg="None"):
        self.setState(state,arg)
        self.d_setState(state,arg)
        
    def getState(self):
        return self._state
        
    def loadByDNA(self):
        data = load_buffer(self.dna)

        try:
            self.toon._m.physControls.deleteCollisions()
            self.toon._m.physControls.disableAvatarControls()
        except: pass
        self.toon._toon.removeNode()
        self.toon = EToon(self,data['toontype'],data['color1'],data['color2'],data['color3'],data['body'],
                          data['gender'],data['legs'],data['head'],True,data['clt'],data['name'])
        self._toon = self.toon._toon
        self.avatar = self.toon._m
        self._m = self.avatar
        
        self.model = self.avatar
        
        data.update(self.toon.data)
        self.dna = make_buffer(data)
        
        if self.isLocalToon:
            wc = GravityWalker(legacyLifter=True)
            wc.setWallBitMask(BitMask32(1))
            wc.setFloorBitMask(BitMask32(2))
            wc.setWalkSpeed(20,10,20,60)
            wc.initializeCollisions(base.cTrav, self, floorOffset=0.025, reach=4.0) #.toon._toon
            wc.enableAvatarControls()
            self.toon._m.physControls = wc
            self.toon._m.physControls.placeOnFloor()
              
        else:
            cn = CollisionNode(self.getName()+'-cnode')
            cs = CollisionSphere(0,0,0,1)
            cn.addSolid(cs)
            cn.setCollideMask(BitMask32(16)|BitMask32(1))
            
            self.cnp = self.toon._toon.attachNewNode(cn)
            self.cnp.setZ(3)
            self.cnp.setSz(3)
                
            gamebase.clickDict[self.cnp] = self.__click
            #self.cnp.show()
                
    def __click(self,e):
        id = load_buffer(self.dna).get('toonId',None)
        if id:
            self.tap = TAP(int(id),self.doId,load_buffer(self.dna))
          
    def setToonDna(self,data):
        self.dna = data
        self.loadByDNA()
        
        self.toon._toon.show()
        
    def d_setToonDna(self,data):
        self.sendUpdate('setToonDna',[data])
        
    def b_setToonDna(self,data):
        self.setToonDna(data)
        self.d_setToonDna(data)
        
    def getToonDna(self):
        return self.dna
        
    def anim(self,*a,**kw): print "Warning: using deprecated anim function!"
        
    def getAnim(self): return ("neutral",1.0)
        
    def speak(self,speech):
        if self.sb and self.sb.exists: self.sb.destroy()
        self.sb = SpeechBubble(self.toon, base.chatMgr.parse(speech))
    
    def d_speak(self,speech): self.sendUpdate("speak",[speech])
    
    def b_speak(self,speech):
        self.speak(speech)
        self.d_speak(speech)

    def setToonDna(self,data):
        self.dna = data
        self.loadByDNA()
   
    def generate(self):
        DistributedSmoothNode.generate(self)
        self.activateSmoothing(True, False)
        self.startSmooth()
        
        self.fsm = AvatarFSM()
        self.fsm.setToon(self)
        
        self.setName("toon_"+str(self.doId))
        self.reparentTo(render)  

    def disable(self):
        self.stopSmooth()
        self.stopPosHprBroadcast()
        self.detachNode()
        DistributedSmoothNode.disable(self)

    def delete(self):
        try:
            self.cnp.removeNode()
            del gamebase.clickDict[self.cnp]
            self.tap.removeNode()
            self.toon._m.physControls.disableAvatarControls()
        except: pass
        self.toon._toon.removeNode()
        DistributedSmoothNode.delete(self)