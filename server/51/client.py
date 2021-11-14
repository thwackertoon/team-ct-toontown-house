import direct.directbase.DirectStart
from direct.showbase.ShowBaseGlobal import *
from direct.actor.Actor import *
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.DirectObject import DirectObject
from direct.distributed.DistributedObject import *
from direct.distributed.DistributedSmoothNode import DistributedSmoothNode
from direct.distributed.ClientRepository import *
from direct.distributed.ServerRepository import *
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
import sys, glob, __builtin__, random

getModelPath().appendDirectory('../..')

base.isInjectorOpen = 0
base.cTrav = CollisionTraverser('baseTraveser')

__builtin__.glob = glob
__builtin__.pversion = '1.8.0'
#from base import *

sys.path.append('../..')
from tth.avatar.toon import EToon

class Client(ClientRepository):
    def __init__(self):
        dcFileNames = ['direct.dc', 'tth.dc']
        
        ClientRepository.__init__(self, dcFileNames = dcFileNames)
            
class EToon2:
    def __init__(self,*ignore):
        self.name = "no name".title()
        self.head = loader.loadModel("data/models/cogs/headsA.bam").find("**/yesman")
        self._toon = Actor("data/models/cogs/suitC.bam",
                                                        {
                                                        "neutral":"data/models/cogs/suitC-neutral.bam",
                                                        "run":"data/models/cogs/suitC-walk.bam",
                                                        "jump":"data/models/cogs/suitC-neutral.bam",
                                                        }
                                                        )
                                                        
        self.head.reparentTo(self._toon.exposeJoint(None,"modelRoot","joint_head"))
        
        self.tag = OnscreenText(scale=.75, text=self.name,bg=(.9,.9,.9,.3),fg=(0,0,1,1),wordwrap=8,decal=True)

        self.tag.setTextureOff()
        
        self.tag.setDepthTest(True)
        self.tag.setDepthWrite(True)
    
        self.tag.reparentTo(self._toon)
        self.tag.setZ(6)
                                                        
    def anim(self,*a,**k):
        self._toon.loop(*a,**k)
             
toonAvatar = EToon(render)

import string
toonName = "Test "+random.choice([string.ascii_lowercase])

toonAvatar.tag = OnscreenText(scale=.75, text=toonName,bg=(.9,.9,.9,.3),fg=(0,0,1,1),wordwrap=8,decal=True)

toonAvatar.tag.setTextureOff()

toonAvatar.tag.setDepthTest(True)
toonAvatar.tag.setDepthWrite(True)
    
toonAvatar.tag.reparentTo(toonAvatar._toon)
toonAvatar.tag.setZ(6)

class Area(DirectObject):
    def __init__(self,environ=None):
        
        self.client = Client()
        if not self.client.connect():
            raise Exception("failed to connect!")
        
        
        base.camera.setPos(0,0,0)
        base.camera.setHpr(0,0,0)
        self.avatar = toonAvatar._m#toon
        self.toon = toonAvatar
        self.toon.anim('neutral')
        
        print self.client.sendCommand("2013",["me","\0"])
                
        self.name="blah"
        
        self.avatar.show()
        
        print 'Setting up',self.name
        
        #gamebase.toonAvatarStream.write("lastArea",str(self.__class__).rsplit('.',1)[-1])
        #gamebase.toonAvatarStream.write("lastAreaName",self.name)
        self.music = "data/sounds/ttc/ttc.ogg"
        
        self.np = NodePath(self.name)
        self.np.reparentTo(render)
        self.avatar.reparentTo(self.np)
        
        self.environ = loader.loadModel("data/models/DDK/donalds_dock.bam")
        self.environ.reparentTo(self.np)
        
        self.keyMap = {"left":0, "right":0, "forward":0, "cam-left":0, "cam-right":0, "backward":0,"control":0,"coll":0}
        base.win.setClearColor(Vec4(0,0,0,1))
        
        if self.music:
            self.theme = loader.loadMusic(self.music)
            self.theme.setLoop(1)
            self.theme.play()
        
        self.frame = DirectFrame(frameColor=(0,0,0,0),parent=base.a2dBackground)
        
        self.floater = NodePath(PandaNode("floater"))
        
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
        
        self.accept("q", self.keyMap.__setitem__, ["coll",1])
        self.accept("q-up", self.keyMap.__setitem__, ["coll",0])

        self.task = taskMgr.add(self.area_task,self.name)

        #self.movingJumping,self.movingForward,self.movingNeutral,self.movingRotation,self.movingBackward = [False for i in xrange(5)]
        self.movingWalk,self.movingJumping = False,False
        self.canMove = True
        
        base.disableMouse()

        Z1,Z2 = map(lambda a:a[-1],self.avatar.getTightBounds())
        
        self.collHand = CollisionHandlerQueue()
        
        self.cNode = CollisionNode('avatarCNode')
        self.cNode.setIntoCollideMask(BitMask32(8))
        self.cNode.setFromCollideMask(BitMask32(8))
        
        self.ray = CollisionRay(0,0,-1,0,0,-1)
        self.cNode.addSolid(self.ray)
        
        self.cNodepath = self.avatar.attachNewNode(self.cNode)
        if base.isInjectorOpen:
            self.cNodepath.show()
            base.cTrav.showCollisions(render)
        
        from direct.controls.GravityWalker import GravityWalker
        wc = GravityWalker(legacyLifter=True)
        wc.setWallBitMask(BitMask32(1))
        wc.setFloorBitMask(BitMask32(2))
        wc.setWalkSpeed(16.0, 24.0, 8.0, 80.0)
        wc.initializeCollisions(base.cTrav, self.avatar, floorOffset=0.025, reach=4.0)

        wc.enableAvatarControls()
        self.avatar.physControls = wc
        self.avatar.physControls.placeOnFloor()
        
        base.cTrav.addCollider(self.cNodepath, self.collHand)
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
        
        base.camera.reparentTo(self.avatar)
        _Z = 4.7
        base.camera.setPos(0, -20, _Z)  

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
    
    def area_task(self, task):
        #base.camera.lookAt(self.avatar)

        startpos = self.avatar.getPos()

        #anim
        
        ij,iw = self.keyMap['control'],(self.keyMap['forward'] or self.keyMap['backward'] or self.keyMap['left'] or self.keyMap['right'])
        it = self.keyMap['left'] or self.keyMap['right']
        
        jp = ''
        
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
            
        entries = []

        n = self.collHand.getNumEntries()
        for i in xrange(n):
            entry = self.collHand.getEntry(i)
                
            for obj in self.avatarPN:
                if findNodeAt(entry.getIntoNodePath(),obj,_name=self.name): entries.append(entry)
                
            if hasattr(self,"collDict"):
                for obj in self.collDict:
                    if self.keyMap["coll"]:print 'COLLDICT!',obj,entry.getIntoNode()==obj
                    if entry.getIntoNode() == obj: self.collDict[obj](entry)
                
            if self.keyMap["coll"]:print entry
            
        if (len(entries)>0):
            self.avatar.setPos(startpos)
            
        if hasattr(self,"taskMethod"): self.taskMethod(task)
        
        return task.cont
        
    def __tth_area__DUMMY(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
                
    def destroy(self):
        self.cNodepath.removeNode()
        
Area()
run()