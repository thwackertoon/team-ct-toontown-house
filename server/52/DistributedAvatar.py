from direct.distributed.DistributedNode import DistributedNode
from pandac.PandaModules import *

from direct.showbase.InputStateGlobal import inputState

import sys, glob, __builtin__, random

getModelPath().appendDirectory('../..')

base.isInjectorOpen = 0
base.cTrav = CollisionTraverser('baseTraveser')

__builtin__.glob = glob
__builtin__.pversion = '1.8.0'
#from base import *

sys.path.append('../..')
from tth.avatar.toon import EToon

class DistributedAvatar(DistributedNode):
    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        NodePath.__init__(self, 'avatar')

        self.avColor = (1, 1, 1)
        
        # Load up the visible representation of this avatar.
        self.toon = EToon(render)
        self.model = self.toon._toon
        self.avatar = self.toon._m
        
        from direct.controls.GravityWalker import GravityWalker
        
        wc = GravityWalker(legacyLifter=True)
        wc.setWallBitMask(BitMask32(1))
        wc.setFloorBitMask(BitMask32(2))
        wc.setWalkSpeed(16.0, 24.0, 8.0, 80.0)
        wc.initializeCollisions(base.cTrav, self.toon._toon, floorOffset=0.025, reach=4.0)

        wc.enableAvatarControls()
        self.toon._m.physControls = wc
        self.toon._m.physControls.placeOnFloor()
        
        self.keyMap = {"left":0, "right":0, "forward":0, "cam-left":0, "cam-right":0, "backward":0,"control":0,"coll":0}
        
        self.movingWalk,self.movingJumping = False,False
        self.canMove = True
        
        base.camera.reparentTo(self.avatar)
        _Z = 4.7
        base.camera.setPos(0, -20, _Z) 
        
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
        
        self.np = render
        
        taskMgr.add(self.area_task,"34y7gfd5")
        
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

    def setAvColor(self, r, g, b):
        """ The local flavor of setAvColor.  This method applies the
        change locally, but does not send an update on the wire.  This
        method is called automatically when an update comes in on the
        wire for a remote object. """
        
        self.avColor = (r, g, b)
        self.setColor(r, g, b, 1)

    def d_setAvColor(self, r, g, b):
        """ The distributed flavor of setAvColor.  By convention, the
        prefix "d_" is applied for distributed methods.  This method
        sends the update on the wire, but does not apply it
        locally. """
        
        self.sendUpdate('setAvColor', [r, g, b])

    def b_setAvColor(self, r, g, b):
        """ The "both" flavor of setAvColor.  By convention, the
        prefix "b_" is used for methods that both apply the change
        locally and also send the update on the wire. """
        self.setAvColor(r, g, b)
        self.d_setAvColor(r, g, b)

    def getAvColor(self):
        """ Returns the current value of avColor.  This method is
        called automatically when a remote object needs to query the
        current value. """
        
        return self.avColor

    def generate(self):
        """ This method is called when the object is generated: when it
        manifests for the first time on a particular client, or when it
        is pulled out of the cache after a previous manifestation.  At
        the time of this call, the object has been created, but its
        required fields have not yet been filled in. """

        # Always call up to parent class
        DistributedNode.generate(self)
        
    def announceGenerate(self):
        """ This method is called after generate(), after all of the
        required fields have been filled in.  At the time of this call,
        the distributed object is ready for use. """

        DistributedNode.announceGenerate(self)

        # Now that the object has been fully manifested, we can parent
        # it into the scene.
        self.reparentTo(render)

    def disable(self):
        """ This method is called when the object is removed from the
        scene, for instance because it left the zone.  It is balanced
        against generate(): for each generate(), there will be a
        corresponding disable().  Everything that was done in
        generate() or announceGenerate() should be undone in disable().

        After a disable(), the object might be cached in memory in case
        it will eventually reappear.  The DistributedObject should be
        prepared to receive another generate() for an object that has
        already received disable().

        Note that the above is only strictly true for *cacheable*
        objects.  Most objects are, by default, non-cacheable; you
        have to call obj.setCacheable(True) (usually in the
        constructor) to make it cacheable.  Until you do this, your
        non-cacheable object will always receive a delete() whenever
        it receives a disable(), and it will never be stored in a
        cache.
        """

        # Take it out of the scene graph.
        self.detachNode()

        DistributedNode.disable(self)

    def delete(self):
        """ This method is called after disable() when the object is to
        be completely removed, for instance because the other user
        logged off.  We will not expect to see this object again; it
        will not be cached.  This is stronger than disable(), and the
        object may remove any structures it needs to in order to allow
        it to be completely deleted from memory.  This balances against
        __init__(): every DistributedObject that is created will
        eventually get delete() called for it exactly once. """

        # Clean out self.model, so we don't have a circular reference.
        self.model = None

        DistributedNode.delete(self)

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
            
        if (len(entries)>0):
            self.avatar.setPos(startpos)
            
        if hasattr(self,"taskMethod"): self.taskMethod(task)
        
        return task.cont