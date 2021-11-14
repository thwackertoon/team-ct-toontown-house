from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta

import Cog, CogDNA, CogStates

class DistributedCog(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.cog = Cog.Cog() #empty cog
        
    def setState(self,state,arg,ts):
        ts = globalClock.getFrameTime() - globalClockDelta.networkToLocalTime(ts,bits=32)
        self.fsm.request(state,arg,max(ts,-ts))
        
    def setDNA(self,dnaString):
        dna = CogDNA.CogDNA()
        dna.makeFrom(dnaString)
        
        self.fsm = CogStates.getFSM(dna.dept,dna.leader)(self,self.cog)
        
        self.cog.reload(dna.make())
        self.cog.reparentTo(render)

    def delete(self):      
        del self.fsm
        
        self.cog.cleanup()
        self.cog.removeNode()
        
        DistributedObject.delete(self)
        
    #trap door: if a client creates a cog (hacker), gets banned xD (actually just kicked atm)
    def getState(self): return ("Off","",0)
    def getDNA(self): return self.cog.dna.make()