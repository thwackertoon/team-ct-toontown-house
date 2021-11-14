import direct.directbase.DirectStart
from direct.actor.Actor import *
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.DirectObject import DirectObject

from direct.controls.GravityWalker import GravityWalker

import random, sys, os, glob
from math import *

import __builtin__, math
__builtin__.glob = glob
__builtin__.pversion = None
sys.path.append('../..')

getModelPath().appendDirectory('../..')


##################################################
#implemetation of Cogtown Injector for easy debugging!
def runInjectorCode():
        global text
        exec (text.get(1.0, "end"),globals())
    
def openInjector():
    import Tkinter as tk
    from direct.stdpy import thread
    root = tk.Tk()
    root.geometry('600x400')
    root.title('Cogtown (TTH version) Injector')
    root.resizable(False,False)
    global text
    frame = tk.Frame(root)
    text = tk.Text(frame,width=70,height=20)
    
    text.pack(side="left")
    tk.Button(root,text="Inject!",command=runInjectorCode).pack()
    scroll = tk.Scrollbar(frame)
    scroll.pack(fill="y",side="right")
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    frame.pack(fill="y")
    
    thread.start_new_thread(root.mainloop,())
    
openInjector()
##################################################
base.isInjectorOpen=1
base.cTrav = CollisionTraverser()

def parentLoop(np,last,_name='render'):
            last = np
            np = np.getParent()
            if np.isEmpty(): return last.getName()
            if np.getName() == _name:
                return last.getName()
            return parentLoop(np,last)
        
def findNodeAt(np,needle,exact=False,_name='render'):
            if np.isEmpty(): return False
            if exact:
                if np.getName() == needle: return True
            else:
                if needle in np.getName(): return True 
            if np.getName() == _name: return False
            return findNodeAt(np.getParent(),needle,exact)

class VirtualArea(DirectObject):
    def __init__(self,toon,environ=None):
        
        self.toon,self.avatar = toon
        
        self.avatar.setPos(0,0,0)
        self.avatar.setHpr(0,0,0)
        
        self.avatar.show()
        
        print 'Setting up',self.name
        
        self.np = NodePath(self.name)
        self.np.reparentTo(render)
        self.avatar.reparentTo(self.np)
        
        if environ: self.environ = loader.loadModel(environ)
        
        self.keyMap = {"left":0, "right":0, "forward":0, "cam-left":0, "cam-right":0, "backward":0,"control":0,"coll":0}
        self.allKeys = {}
        base.win.setClearColor(Vec4(0,0,0,1))
        
        if self.music:
            self.theme = loader.loadMusic(self.music)
            self.theme.setLoop(1)
            self.theme.play()
        
        self.frame = DirectFrame(frameColor=(0,0,0,0),parent=base.a2dBackground)
        
        self.floater = NodePath(PandaNode("floater"))
        
        self.enableControls()
        
        self.accept("q", self.keyMap.__setitem__, ["coll",1])
        self.accept("q-up", self.keyMap.__setitem__, ["coll",0])

        self.task = taskMgr.add(self.area_task,self.name)

        #self.movingJumping,self.movingForward,self.movingNeutral,self.movingRotation,self.movingBackward = [False for i in xrange(5)]
        self.movingWalk,self.movingJumping = False,False
        self.canMove = True
        
        base.disableMouse()

        Z1,Z2 = map(lambda a:a[-1],self.avatar.getTightBounds())
        
        self.collHand = CollisionHandlerQueue()
        self.pusher = CollisionHandlerPusher()
        
        self.cNode = CollisionNode('avatarCNode')
        self.cNode.setIntoCollideMask(BitMask32(8))
        self.cNode.setFromCollideMask(BitMask32(8))
        
        self.ray = CollisionRay(0,0,-1,0,0,-1)
        self.cNode.addSolid(self.ray)
        
        self.cNodepath = self.avatar.attachNewNode(self.cNode)
        if base.isInjectorOpen:
            self.cNodepath.show()
            base.cTrav.showCollisions(render)
            
        self.camCNode = CollisionNode('camCNode')
        self.camCNode.addSolid(CollisionRay(0,0,-1,0,0,-1))
        self.camCNode.setFromCollideMask(BitMask32(1))
        self.camCNode.setIntoCollideMask(BitMask32.allOff())
        self.camNp = base.cam.attachNewNode(self.camCNode)
        
        base.cTrav.addCollider(self.cNodepath, self.collHand)
        base.cTrav.addCollider(self.camNp, self.pusher)
        
        #self.pusher.addCollider(self.camNp, base.cam)
        
        base.cTrav.setRespectPrevTransform(True)
        
        if not hasattr(self,"avatarPN"): self.avatarPN = []
        
        if hasattr(self,"light") and self.light:

            ambientLight = AmbientLight("ambientLight")
            ambientLight.setColor(Vec4(1,1,1,1))
            directionalLight = DirectionalLight("directionalLight")
            directionalLight.setDirection(Vec3(0, 0, -1))
            directionalLight.setColor(Vec4(1, 1, 1, 1))
            directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
            self.np.setLight(self.np.attachNewNode(ambientLight))
            self.np.setLight(self.np.attachNewNode(directionalLight))
        
        self.camTarget = self.avatar
        self.last = 0
        self.handleAnim = True
        
        base.camera.reparentTo(self.avatar)
        _Z = 4.7
        base.camera.setPos(0, -20, _Z) 

        self.lastBroadcastTransform = None
        times_per_second = 8
        #taskMgr.doMethodLater(1./times_per_second, self.updateAvatar, 'updateAvatar')
        #self.toon.startPosHprBroadcast()

            
    def disableControls(self):
        self.handleAnim = False
        for input,(key,keyMapName) in self.allKeys.items():
            inputState.set(input, False)
            self.keyMap[keyMapName] = 0
        self.ignoreAll()
            
    def enableControls(self):
        self.setWatchKey('arrow_up', 'forward', 'forward')
        self.setWatchKey('control-arrow_up', 'forward', 'forward')
        self.setWatchKey('alt-arrow_up', 'forward', 'forward')
        self.setWatchKey('shift-arrow_up', 'forward', 'forward')
        self.setWatchKey('arrow_down', 'reverse', 'backward')
        self.setWatchKey('control-arrow_down', 'reverse', 'backward')
        self.setWatchKey('alt-arrow_down', 'reverse', 'backward')
        self.setWatchKey('shift-arrow_down', 'reverse', 'backward')
        self.setWatchKey('arrow_left', 'turnLeft', 'left')
        self.setWatchKey('control-arrow_left', 'turnLeft', 'left')
        self.setWatchKey('alt-arrow_left', 'turnLeft', 'left')
        self.setWatchKey('shift-arrow_left', 'turnLeft', 'left')
        self.setWatchKey('arrow_right', 'turnRight', 'right')
        self.setWatchKey('control-arrow_right', 'turnRight', 'right')
        self.setWatchKey('alt-arrow_right', 'turnRight', 'right')
        self.setWatchKey('shift-arrow_right', 'turnRight', 'right')
        self.setWatchKey('control', 'jump', 'control')
        self.handleAnim = True
            
    def setWatchKey(self, key, input, keyMapName):
        def watchKey(active=True):
            if active:
                inputState.set(input, True)
                self.keyMap[keyMapName] = 1
            else:
                inputState.set(input, False)
                self.keyMap[keyMapName] = 0
                
        self.accept(key, watchKey, [True])
        self.accept(key+'-up', watchKey, [False])
        self.allKeys[input] = (key,keyMapName)
    
    def area_task(self, task):
        #base.camera.lookAt(self.avatar)

        startpos = self.avatar.getPos()

        #anim
        
        if self.handleAnim:
            ij,iw = self.keyMap['control'],(self.keyMap['forward'] or self.keyMap['backward'] or self.keyMap['left'] or self.keyMap['right'])
            it = self.keyMap['left'] or self.keyMap['right']
            
            jp = '-zhang'
            
            if iw:
                if not self.movingWalk:
                    self.movingWalk = True
                    
                    if ij: self.toon.anim('jump-zhang')
                    else: self.toon.anim(('run','walk')[it])
                    
            else:
                if self.movingWalk:
                    self.movingWalk = False
                    
                    if ij: self.toon.anim('jump'+jp,1.2)
                    else: self.toon.anim('neutral')
                    
            if ij:
                if not self.movingJumping:
                    self.movingJumping = True
                    
                    if iw: self.toon.anim('jump-zhang')
                    else: self.toon.anim('jump'+jp,1.2)
                    
            else:
                if self.movingJumping:
                    self.movingJumping = False
                    
                    if iw: self.toon.anim(('run','walk')[it])
                    else: self.toon.anim('neutral')
        
        base.cTrav.traverse(self.np)

        n = self.collHand.getNumEntries()
        for i in xrange(n):
            entry = self.collHand.getEntry(i)
                
            if hasattr(self,"collDict"):
                for obj in self.collDict:
                    if self.keyMap["coll"]:print 'COLLDICT!',obj,entry.getIntoNode()==obj
                    if entry.getIntoNode() == obj: self.collDict[obj](entry)
                
            if self.keyMap["coll"]:print entry
            
        if hasattr(self,"taskMethod"): self.taskMethod(task)
        
        return task.cont

class VirtualDock(VirtualArea):
    def __init__(self,toon):
        self.music = "data/sounds/DD_nbrhood.mp3"
        self.name = "AREA_DDK"
 
        self.zoneId = 2000
        newModel = loader.loadModel
        
        self.av_startpos = (
                            ((-116.69, -34.2716, -0.245013),(-179.758, 0, 0)),
                            ((-92.9745, -38.4801, -0.00904583),(-72.1942, 0, 0)),
                            ((-59.2309, -43.7733, -0.00904993),(-117.784, 0, 0)),
                            ((18.9871, -15.2758, -0.00811336),(-211.235, 0, 0)),
                            ((-22.0924, -103.422, -0.00839086),(-242.26, 0, 0)),
                            ((-59.7771, -190.784, 2.40302),(-331.3, 0, 0)),
                            ((-167.607, -191.644, 2.37616),(-388.684, 0, 0)),
                            ((-200.292, -119.822, 2.4041),(-427.432, 0, 0)),
                            ((-165.27, -53.3781, 2.40303),(-487.091, 0, 0)),
                            ((-109.571, -118.602, 2.47348),(-480.476, 0, 0)),
                            )
        VirtualArea.__init__(self,toon,"data/models/DDK/dd.bam")
 
        self.sky1 = loader.loadModel("data/models/TTC/TT_sky.bam")
        self.sky1.reparentTo(self.np)
        self.sky2 = loader.loadModel("data/models/DDK/sky.bam")
        self.sky2.reparentTo(self.np)
        self.sky2.hide()

        self.environ.setPos(-25,10,0)
        self.environ.setHpr(180,0,0)
        self.environ.reparentTo(self.np)
        self.boat = self.environ.find("**/donalds_boat")
        self.boat.setPos(50.1,25,-4)
        self.boat.setHpr(180,0,0)
        self.EPier = self.environ.find("**/east_pier")
        self.WPier = self.environ.find("**/west_pier")

        self.pier1 = newModel("data/models/DDK/pier.bam")
        self.pier1.reparentTo(self.np)
        self.pier1.setPos(-1.79822,139.984,3.59855)
        self.pier1.setHpr(135,0,0)
        self.pier2 = newModel("data/models/DDK/pier.bam")
        self.pier2.reparentTo(self.np)
        self.pier2.setPos(-11.6229,148.498,3.64751)
        self.pier2.setHpr(165,0,0)
        self.pier3 = newModel("data/models/DDK/pier.bam")
        self.pier3.reparentTo(self.np)
        self.pier3.setPos(-23.6427,149.15,3.59725)
        self.pier3.setHpr(-165,0,0)
        self.pier3 = newModel("data/models/DDK/pier.bam")
        self.pier3.reparentTo(self.np)
        self.pier3.setPos(-31.3754,141.368,3.56653)
        self.pier3.setHpr(-135,0,0)
        
from tth.avatar.toon import EToon
myToon = EToon(render)

wc = GravityWalker(legacyLifter=True)
wc.setWallBitMask(BitMask32(1))
wc.setFloorBitMask(BitMask32(2))
wc.setWalkSpeed(20,10,20,60)
wc.initializeCollisions(base.cTrav, myToon._toon, floorOffset=0.025, reach=4.0)
wc.enableAvatarControls()
myToon._m.physControls = wc
myToon._m.physControls.placeOnFloor()

dock = VirtualDock((myToon,myToon._m))

run()