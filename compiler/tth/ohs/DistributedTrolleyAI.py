from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import *
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.task.Task import Task
COUNTDOWN_TIME = 10.0

class DistributedTrolleyAI(DistributedObjectAI):
    def __init__(self,cr):
        self.toons = [-1,-1,-1,-1]
        self._time = 0
        taskMgr.add(self.monitorToons,"trolley monitor")
        self.leaving = False
        
        self.fsm = ClassicFSM('TrolleyAI',[
                                      State('Wait', self.enterWait, self.exitWait, ['Countdown']),
                                      State('Countdown', self.enterCountdown, self.exitCountdown, ['Wait', 'Go']),
                                      State('Go', self.enterGo, self.exitGo, ['Wait'])
                                      ],'Wait','Wait')
        
        self.fsm.enterInitialState()
        
        DistributedObjectAI.__init__(self,cr)
        
    def generate(self):
        DistributedObjectAI.generate(self)
        taskMgr.doMethodLater(2,lambda t:self.setState("Wait"),"x")
        
    def setToons(self,t0,t1,t2,t3):
        self.toons = [t0,t1,t2,t3]
        
    def getToons(self):
        return self.toons
        
    def requestBoard(self,doId):
        print 'Trolley: request enter',doId
        if self.__full() or self.leaving:
            self.sendUpdate("reject",[doId])
        else:
            self.addToon(doId)
            self.sendUpdate("accept",[doId,len(filter(lambda x:x!=-1,self.toons))-1])
            self.sendUpdate("setToons",self.toons) #update
            if len(filter(lambda x:x>0,self.toons)) == 1:
                #print 'TIMER SHOULD START NOW!'
                self.setState("Countdown")
                
    def requestExit(self,doId):
        print 'Trolley: request exit',doId
        
        if not doId in self.toons:
            print '!',doId,'not in toons!'
            return
            
        self.toons[self.toons.index(doId)] = -1
        self.sendUpdate("setToons",self.toons) #update
        
        if not self.__any():
            #print 'TIMER STOP!'
            self.setState("Wait")
            
    def addToon(self,doId):
        self.toons[self.toons.index(-1)] = doId
        
    def monitorToons(self,task):
        for toon in self.toons:
            if toon != -1:
                #check if dc
                if not base.air.id2c(toon) in base.cTracker:
                    print 'Trolley monitor: we have a dc:',toon
                    self.requestExit(toon) #remove
                    
        return task.cont      
        
    def setState(self,state):
        self.__state = [state,globalClock.getFrameTime()]
        self.fsm.request(state)
        self.sendUpdate("setState",[state,globalClockDelta.localToNetworkTime(globalClock.getFrameTime())])
        
    def getState(self):
        return self.__state
        
    def timerTask(self, task):
        countdownTime = int(task.duration - task.time)
        if task.time >= task.duration:
            self._time = 0
            #print 'LEAVE!'
            self.setState("Go")
            return Task.done
        else:
            self._time = globalClock.getFrameTime()
            return Task.cont
        
    def enterCountdown(self):
        countdownTask = Task(self.timerTask)
        countdownTask.duration = 10
        taskMgr.remove('trolleyTimerTask')
        
        return taskMgr.add(countdownTask, 'trolleyTimerTask')
        
    def exitCountdown(self):
        taskMgr.remove('trolleyTimerTask')
        self._time = 0
        
    def enterWait(self): pass 
    def exitWait(self): pass 
    def enterGo(self):
        self.leaving = True
        Sequence(Wait(4.5),Func(self.yieldZone)).start()
    
    def exitGo(self): self.leaving = False
    
    def yieldZone(self):
        zone = base.air.getFreeZone()
        print 'YIELD ZONE!',zone
        self.sendUpdate("setMinigameZone",[zone])
        
        self.toons = [-1,-1,-1,-1]
        self.sendUpdate("setToons",self.toons)
        
        Sequence(Wait(4.5),Func(self.setState,"Wait")).start()
        
    def __full(self): return all(x>0 for x in self.toons)
        
    def __any(self): return any(x>0 for x in self.toons)