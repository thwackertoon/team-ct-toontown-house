from panda3d.core import *
import direct.directbase.DirectStart
loadPrcFileData('','default-model-extension .bam')
import os, __builtin__

mfRoot = "data/"
mfs = [mfRoot+x for x in os.listdir(mfRoot) if x.endswith(".mf")]
vfs = VirtualFileSystem.getGlobalPtr()
for mf in mfs: print "mounting",mf,vfs.mount(mf,".",VirtualFileSystem.MFReadOnly,(lambda x,y:x.decode(y))("ggu0hf3","rot13"))
getModelPath().appendDirectory("./data")

__builtin__.BTFont =loader.loadFont('phase_3/models/fonts/ImpressBT.ttf')

from direct.actor.Actor import Actor
from tth.avatar import Toon, ToonDNA

dna = ToonDNA.ToonDNA()
dna.newToonRandom()
#dna.updateToonProperties(head='dll')
#print dna

toon = Toon.Toon()
toon.setDNA(dna)
toon.reparentTo(base.cam)
toon.setPos(0,30,-2)
toon.setH(180)
toon.loop('neutral')
toon.setName('Test Name',1,1)

maxColor = len(ToonDNA.allColorsList)

global cColor
cColor = dna.armColor
def nextColor():
    global cColor
    cColor = (cColor+1)%maxColor

    dna.updateToonProperties(armColor = cColor)
    toon.setDNA(dna)

base.accept('space',nextColor)

from direct.gui.DirectGui import *
from panda3d.core import *

from tth.managers import MGR_SFX_speech as MSs

class SpeechBubbleBase(NodePath):
    def __init__(self, speech, font = None):
        self.speech = speech

        NodePath.__init__(self,'SBBase')

        box = loader.loadModel("phase_3/models/props/chatbox.bam")
        box.setBillboardAxis()
        box.setBillboardPointWorld()
        box.reparentTo(self)
        self.box = box

        if not speech:
            self.text = TextNode('dummy')
            self.textNp = NodePath('dummy')
            return

        text = TextNode('chatbox_text')
        if not isinstance(speech,unicode): speech = unicode(speech,'latin-1')

        text.setWtext(speech)

        if not font: font = BTFont
        text.setFont(font)

        bw = map(Vec3.getX,box.getTightBounds())
        bw = abs(bw[0]-bw[1])

        bh = map(Vec3.getZ,box.getTightBounds())
        bh = abs(bh[0]-bh[1])

        ww = (bw-5)/.525
        text.setWordwrap(ww)

        textNp = box.find('**/top').attachNewNode(text)
        textNp.setColor(Vec4(0,0,0,1),1)
        textNp.setScale(.3) #.5 --> BIG! (editing fucked it, so restored to .5 -_-) - Thanks, not, fixing it.
        textNp.setDepthOffset(100)
        textNp.setZ(.1)
        textNp.setX(.2)

        w = text.getWidth() / 2.75   #1.75
        h = text.getHeight()
        l = text.getNumRows() -.055 #(none)

        textNp.wrtReparentTo(hidden)
        box.setSx(w/bw)

        textNp.setX(box,1)
        box.setSz((l*1.2)/bh)
        box.setZ((3-l)*1.2)
        textNp.wrtReparentTo(box.find('**/top'))

        self.text = text
        self.textNp = textNp
        self.box = box

class ToonSpeechBubble(SpeechBubbleBase):
    def __init__(self, toon, speech, time = 6):
        self.toon = toon
        self.time = time

        self.tag = toon.tag
        if self.tag: self.tag.hide()

        SpeechBubbleBase.__init__(self,speech)

        if self.textNp.getName() != "dummy":
            self.reparentTo(self.toon)
            self.box.setZ(self,self.tag.getZ(self.toon))

            self.exists = True
            spc = self.toon.style.getAnimal()
            if spc:  MSs(spc,speech).play()

            self.frame = self.box
            taskMgr.doMethodLater(time,self._destroyTask, 'destroyTask')

            print self.box.getZ(render),self.tag.getZ()+.2

    def _destroyTask(self,task):
        self.frame.hide()
        self.frame.removeNode()
        self.exists = False
        if self.tag: self.tag.show()
        return task.done

    def destroy(self):
        self.frame.hide()
        self.tag = None
        self.exists = False

#base.cam.lookAt(ToonSpeechBubble(toon,"Test long long long long").box)

run()