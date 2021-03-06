""" Demonstrates the DC system from the client side, using a
DistributedNode-based avatar. """

from direct.directbase.DirectStart import *
from direct.distributed.ClientRepository import ClientRepository
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.showbase.InputStateGlobal import inputState
#from DistributedPellet import DistributedPellet
import sys
import random, glob
import sys, glob, __builtin__, random
base.isInjectorOpen = 0
base.cTrav = CollisionTraverser('baseTraveser')

__builtin__.glob = glob
__builtin__.pversion = '1.8.0'
#from base import *

sys.path.append('../..')
getModelPath().appendDirectory('../..')

helpText = """[Left Arrow]: Rotate Left
[Right Arrow]: Rotate Right
[Up Arrow]: Move Forward
[Down Arrow]: Move Backwards
[Tab]: Change color
[Space]: Drop pellet
[c]: Clear pellets
[1 - 9]: Set zone
[Escape]: exit"""

class MyClientRepository(ClientRepository):
    def __init__(self):
        dcFileNames = ['direct.dc', 'tth.dc']
        
        ClientRepository.__init__(self, dcFileNames = dcFileNames)

class World(DirectObject):

    # Degrees per second of rotation
    rotateSpeed = 90

    # Units per second of motion
    moveSpeed = 8
    
    def __init__(self):
        DirectObject.__init__(self)

        # No avatar yet.
        self.av = None

        # No pellets either.
        self.pellets = []
        
        self.env = loader.loadModel("data/models/GRD/daisys_garden.bam")
        self.env.reparentTo(render)

        # The list of keys that we will be monitoring.
        self.moveKeyList = [
            'arrow_left', 'arrow_right', 'arrow_up', 'arrow_down'
            ]

        # Initially, all keys are up.  Construct a dictionary that
        # maps each of the above keys to False, and hang the event to
        # manage that state.
        self.moveKeys = {}
        for key in self.moveKeyList:
            self.moveKeys[key] = False
            self.accept(key, self.moveKeyStateChanged, extraArgs = [key, True])
            self.accept(key + '-up', self.moveKeyStateChanged, extraArgs = [key, False])


        tcpPort = base.config.GetInt('server-port', 4000)
        hostname = base.config.GetString('server-host', '127.0.0.1')
        self.url = URLSpec('http://%s:%s' % (hostname, 4000))

        self.cr = MyClientRepository()
        self.cr.connect([self.url],
                        successCallback = self.connectSuccess,
                        failureCallback = self.connectFailure)
        
        self.waitingText = OnscreenText(
            'Connecting to %s.\nPress ESC to cancel.' % (self.url),
            scale = 0.1, fg = (1, 1, 1, 1), shadow = (0, 0, 0, 1))

        self.accept('escape', self.escape)

        # Oobe mode is handy to have on all the time.  Why not?
        base.oobe()

    def moveKeyStateChanged(self, key, newState):
        """ A key event has been received.  Change the key state in
        the dictionary. """
        self.moveKeys[key] = newState

    def escape(self):
        """ The user pressed escape.  Exit the client. """
        sys.exit()
        
    def connectFailure(self, statusCode, statusString):
        self.waitingText.destroy()
        self.failureText = OnscreenText(
            'Failed to connect to %s: %s.\nPress ESC to quit.' % (self.url, statusString),
            scale = 0.15, fg = (1, 0, 0, 1), shadow = (0, 0, 0, 1))

    def connectSuccess(self):
        """ Successfully connected.  But we still can't really do
        anything until we've got the doID range. """
        self.waitingText.destroy()
        self.waitingText = OnscreenText(
            'Waiting for server.',
            scale = 0.1, fg = (1, 1, 1, 1), shadow = (0, 0, 0, 1))
        self.acceptOnce('createReady', self.createReady)

    def createReady(self):
        """ Now we're ready to go! """
        self.waitingText.destroy()
        
        # Manifest an avatar for ourselves.
        self.av = self.cr.createDistributedObject(
            className = 'DistributedAvatar', zoneId = 1)

        # The tab key changes your color.
        self.accept('tab', self.changeAvColor)

        # The space bar drops a new pellet.
        self.accept('space', self.dropPellet)

        # The 'c' key clears the pellets you've dropped.
        self.accept('c', self.clearPellets)

        # A number key (other than zero) changes your zone.
        for zoneId in range(1, 10):
            self.accept(str(zoneId), self.changeAvZone, extraArgs = [zoneId])

        # Pop up some help text.
        self.title = OnscreenText(
            parent = base.a2dBottomRight,
            text = 'DistributedNode client demo',
            fg = (1, 1, 1, 1),
            pos = (-0.03, 0.03), align = TextNode.ARight, scale = 0.1)

        self.help = OnscreenText(
            parent = base.a2dTopLeft,
            text = helpText,
            fg = (1, 1, 1, 1),
            pos=(0.03, -0.1), align = TextNode.ALeft, scale = 0.07)

        # Update the local avatar's position every frame.
        self.moveTask = taskMgr.add(self.moveAvatar, 'moveAvatar')

        # Send position updates only several times a second, instead
        # of every frame, or we will flood the network.
        self.lastBroadcastTransform = self.av.getTransform()
        self.updateTask = taskMgr.doMethodLater(0.2, self.updateAvatar, 'updateAvatar')

    def dropPellet(self):
        # Create a new DistributedPellet, and put it right where the
        # avatar is.
        pellet = DistributedPellet(self.cr)
        x, y, z = self.av.getPos()
        pellet.setInitialPos(x, y, z)
        self.cr.createDistributedObject(
            distObj = pellet, zoneId = self.av.zoneId)
        self.pellets.append(pellet)

    def clearPellets(self):
        # Remove all of the DistributedPellets we've created.
        for p in self.pellets:
            self.cr.sendDeleteMsg(p.doId)

    def changeAvColor(self):
        """ The user pressed the tab key.  Change the color of the
        local avatar to a new random color. """
        r = random.uniform(0, 1)
        g = random.uniform(0, 1)
        b = random.uniform(0, 1)
        self.av.b_setAvColor(r, g, b)

    def changeAvZone(self, zoneId):
        """ The user pressed one of the number keys to change zones.
        Move the avatar into the indicated zone. """

        # Move our avatar into the indicated zone
        self.cr.setObjectZone(self.av, zoneId)

    def moveAvatar(self, task):
        """ This task runs each frame to move the avatar according to
        the set of arrow keys that are being held. """

        dt = globalClock.getDt()
        
        if self.moveKeys['arrow_left']:
            self.av.setH(self.av, dt * self.rotateSpeed)
        elif self.moveKeys['arrow_right']:
            self.av.setH(self.av, -dt * self.rotateSpeed)

        if self.moveKeys['arrow_up']:
            self.av.setY(self.av, dt * self.moveSpeed)
        elif self.moveKeys['arrow_down']:
            self.av.setY(self.av, -dt * self.moveSpeed)

        return task.cont

    def updateAvatar(self, task):
        """ This task runs five times a second to broadcast the
        avatar's position to all of the other clients. """

        currentTransform = self.av.getTransform()
        if self.lastBroadcastTransform == currentTransform:
            # No change since last broadcast.
            return task.again

        self.lastBroadcastTransform = currentTransform
        x, y, z = self.av.getPos()
        h, p, r = self.av.getHpr()
        self.av.d_setPosHpr(x, y, z, h, p, r)

        return task.again

w = World()
run()

