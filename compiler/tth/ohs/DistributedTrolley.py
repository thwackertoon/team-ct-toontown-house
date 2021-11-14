from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State

from direct.task.Task import Task

from panda3d.core import Point3, BitMask32, TextNode

COUNTDOWN_TIME = 10.0
TOON_BOARD_TIME = 1.0
TOON_EXIT_TIME = 1.0

class DistributedTrolley(DistributedObject):
    def __init__(self,cr):
        self.toons = [-1,-1,-1,-1]
        self._waitingId = -1
        self.geomInited = False
        self.seq = None
        self.letGoIn = True
        
        self.fsm = ClassicFSM('Trolley',[
                                      State('Wait', self.enterWait, self.exitWait, ['Countdown']),
                                      State('Countdown', self.enterCountdown, self.exitCountdown, ['Wait', 'Go']),
                                      State('Go', self.enterGo, self.exitGo, ['Wait'])
                                      ],'Wait','Wait')
                                      
        self.fsm.enterInitialState([0])
        
        DistributedObject.__init__(self,cr)
        
    def generate(self):
        DistributedObject.generate(self)
        taskMgr.doMethodLater(.5,self.__initGoem,'blah')
        
    def setToons(self,t0,t1,t2,t3):
        self.toons = [t0,t1,t2,t3]
        #print 'TOONS SET!',self.toons
        
    def d_requestBoard(self,_id):
        if self._waitingId == -1 and _id not in self.toons and self.letGoIn:
            self.sendUpdate("requestBoard",[_id])
            self._waitingId = _id
        
    def accept(self,_id,index):
        if _id != self._waitingId:
            return
            
        print 'accepted to trolley @ pos',index
        self._waitingId = -1

        gamebase.curArea.disableControls()
        gamebase.curArea.toon._m.physControls.setCollisionsActive(False)
        gamebase.curArea.toon._m.physControls.isAirbone = True
        
        toon,avatar = gamebase.curArea.toon,gamebase.curArea.avatar
        avatar.setPos(0,0,0)
        avatar.setHpr(0,0,0)
        avatar.reparentTo(self.points[index])
        toon.b_setState('Sit')
        
        base.cam.setPos(0,0,0)
        base.cam.setHpr(0,0,0)
        base.cam.reparentTo(self.trolleyCar)
        base.cam.setPos((-50,0,6))
        base.cam.setH(-90)
        
        self.exitButton = DirectButton(relief=None, text=L10N('ELEVATOR_HOPOFF'),
         text_fg=(0.9, 0.9, 0.9, 1), text_pos=(0, -0.23), text_scale=.8,
         image=(self.upButton, self.downButton, self.rolloverButton), image_color=(1, 0, 0, 1),
         image_scale=(20, 1, 11), pos=(0, 0, 0.8), scale=0.15, command=self.__hopOff)
            
    def reject(self,_id):
        if _id == self._waitingId:
            print 'rejected to trolley!'
            
        self._waitingId = -1
    
    def __hopOff(self):
        print 'hopping off trolley'
        self.letGoIn = False
        self.sendUpdate("requestExit",[gamebase.curArea.toon.doId])
        gamebase.curArea.toon._m.physControls.setCollisionsActive(True)
        gamebase.curArea.toon._m.physControls.isAirborne = True
        gamebase.curArea.toon._m.physControls.placeOnFloor()
        gamebase.curArea.avatar.wrtReparentTo(gamebase.curArea.np)
        
        WalkAway = Sequence()
        WalkAway.append(Func(gamebase.curArea.avatar.setH,self.trolleyStation.getH(render)))
        WalkAway.append(Func(gamebase.curArea.avatar.setY,gamebase.curArea.avatar,-25))
        
        Sequence(
                 Func(self.exitButton.removeNode),
                 Wait(.2),
                 Func(gamebase.curArea.toon.anim,'jump'),
                 WalkAway,
                 #Func(gamebase.curArea.toon.b_anim,'neutral'),
				 #there isnt no god damn b.anim in the toon files. WHA ARE YOU EVEN THINKING?!
				 Func(gamebase.curArea.toon.anim,'neutral'),
                 Func(self.__hopOff_cam),
                 Func(gamebase.curArea.enableControls),
                 Func(self.__dict__.__setitem__,"letGoIn",True)
                ).start()
                
    def enterWait(self, ts): pass 
    def exitWait(self): pass 
               
    def enterCountdown(self, ts):
        if not self.geomInited: 
            taskMgr.doMethodLater(.5,lambda t:self.enterCountdown(ts),'recount')
            return Task.done
            
        #print 'ENTER COUNTDOWN'
        self.clockNode = TextNode('trolleyClock')
        self.clockNode.setAlign(TextNode.ACenter)
        self.clockNode.setTextColor(0.9, 0.1, 0.1, 1)
        self.clockNode.setText('10')
        self.clock = self.trolleyStation.attachNewNode(self.clockNode)
        self.clock.setBillboardAxis()
        self.clock.setPosHprScale(15.86, 13.82, 11.68, -0.0, 0.0, 0.0, 3.02, 3.02, 3.02)
        if ts < COUNTDOWN_TIME:
            self.countdown(COUNTDOWN_TIME - ts)

    def timerTask(self, task):
        countdownTime = int(task.duration - task.time)
        timeStr = str(countdownTime)
        if self.clockNode.getText() != timeStr:
            self.clockNode.setText(timeStr)
        if task.time >= task.duration:
            return Task.done
        else:
            return Task.cont

    def countdown(self, duration):
        countdownTask = Task(self.timerTask)
        countdownTask.duration = duration
        taskMgr.remove('trolleyTimerTask')
        return taskMgr.add(countdownTask, 'trolleyTimerTask')
        
    def exitCountdown(self):
        #print 'EXIT COUNTDOWN'
        taskMgr.remove('trolleyTimerTask')
        try:
            self.clock.removeNode()
            del self.clock
            del self.clockNode
        except: pass
        
    def setState(self, state, timestamp):
        print 'set_state',state, globalClockDelta.localElapsedTime(timestamp)
        self.fsm.request(state, [globalClockDelta.localElapsedTime(timestamp)])
        
    def __hopOff_cam(self):
        base.cam.setPos(0,0,0)
        base.cam.setHpr(0,0,0)
        base.cam.reparentTo(gamebase.curArea.avatar)
        base.cam.setPos(0, -20, 4.7) 
        
    def __initGoem(self,task):
        if not gamebase.curArea: return task.again
        if not gamebase.curArea.np: return task.again
    
        gamebase.curArea.trolleyMgr = self
        np = gamebase.curArea.np
        
        self.trolleyStation = np.find('**/*trolley_station*')
        self.trolleyCar = self.trolleyStation.find('**/trolley_car')
        self.trolleyCar.find('**/*trigg*').node().setCollideMask(BitMask32.allOff())
        
        self.points = []
        for i in xrange(4):
            p = self.trolleyCar.attachNewNode("point"+str(i))
            p.setPos(-6,-3.1+(i*2.3),3.3)
            p.setHpr(90,0,0)
            self.points.append(p)
        
        self.seq = Sequence(
                            self.trolleyCar.posInterval(4,(40, 14.1588, -0.984615)),
                            self.trolleyCar.posInterval(.1,(40, 14.1588, -40)),
                            self.trolleyCar.posInterval(.1,(-30, 14.1588, -40)),
                            self.trolleyCar.posInterval(.1,(-30, 14.1588, -0.984615)),
                            self.trolleyCar.posInterval(4,(15.751, 14.1588, -0.984615)),
                            )
                            
        self.camSeq = Sequence(
                            base.cam.posHprInterval(2.5, Point3(-35, 0, 8), Point3(-90, 0, 0)),
                            )
        
        self.buttonModels = loader.loadModel('phase_3.5/models/gui/inventory_gui.bam')
        self.upButton = self.buttonModels.find('**/InventoryButtonUp')
        self.downButton = self.buttonModels.find('**/InventoryButtonDown')
        self.rolloverButton = self.buttonModels.find('**/InventoryButtonRollover')
        
        self.geomInited = True
        
        return task.done
        
    def enterGo(self,timestamp,task=None):
        try: self.exitButton.removeNode()
        except: pass
        
        if self.seq:
            self.seq.start(timestamp)
            if self.localOnBoard(): self.camSeq.start(timestamp)
            
        else: 
            taskMgr.doMethodLater(.5,lambda t:self.enterGo(ts),'rego')
        return Task.done
        
    def exitGo(self): pass
    
    def setMinigameZone(self,x):
        if self.localOnBoard():
            print 'minigame zone is',x
            messenger.send('playMinigame',[x])
            
    def localOnBoard(self): return gamebase.toonAvatar[0].doId in self.toons