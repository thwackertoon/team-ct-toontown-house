from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import *

from direct.actor.Actor import Actor

class AvatarFSM(FSM):
    def __init__(self):
        FSM.__init__(self,'AvatarFSM')
        self.toon = None
        self.walkingFootStep = loader.loadSfx('phase_3.5/audio/sfx/AV_footstep_runloop.wav')
        self.walkingFootStep.setLoop(1)
        
    def setToon(self,toon): self.toon = toon
        
    def enterSit(self,arg): self.__anim('sit')
    def exitSit(self): pass
    
    def enterWalk(self,arg):
        self.__anim(arg)
        if self.toon.isLocalToon:
            self.walkingFootStep.play()
            
    def exitWalk(self):
        if self.toon.isLocalToon:
            self.walkingFootStep.play()
    
    def enterNone(self,arg): pass
    def exitNone(self): pass
    
    def enterBook(self,arg): 
        self.book = Actor("phase_3.5/models/props/book-mod.bam",{'x':"phase_3.5/models/props/book-chan.bam"})
        self.book.pose('x',70)
        self.book.reparentTo(self.toon.model.find('**/def_*left*'))
        self.book.setPos(self.book,(0,0.5,0))
        self.book.setHpr(self.book,(89.3812, -20.4861, -19.5007))
        self.book.hide()
        
        Sequence(
                 Func(self.__anim,'book',2,False),
                 Wait(.5),
                 Func(self.book.show),
                 Wait(1.5),
                 Func(self.toon.toon.pose,'book',50)
                 ).start()
            
    def exitBook(self):
        self.book.cleanup()
        self.book.removeNode()
        
    def enterNeutral(self,arg): self.__anim('neutral')
    def exitNeutral(self): pass
    
    def enterJump(self,arg): self.__anim('jump-zhang')
    def exitJump(self): pass
    
    def enterTeleport(self,target=None):
        if self.toon.isLocalToon:
            gamebase.curArea.disableControls()
            
        s = Sequence(
            Func(self.__anim,'teleport'),
            Wait(3.3),
            )
        
        if target and self.toon.isLocalToon:
            s.append(Func(base.hoodMgr.bookTp,int(target)))
        
        s.start()
    
	#pass 
    def exitTeleport(self): pass
 
    def __anim(self,*args):
        self.toon.toon.anim(*args)
        
