from panda3d.core import *
from direct.gui.DirectGui import *

from tth.avatar.toon import rgb2p
from tth.book import Book
from chat import makeSCMenu,ClassicChatBox
from direct.interval.IntervalGlobal import *
#makeSCMenu = lambda *a:0

def getGuiItem(name):
    gui_items = {m.getName():m for m in loader.loadModel('phase_3/models/gui/book_gui.bam').findAllMatches('**') if m.getName()}
    if name == 'ALL':
        return gui_items.keys()
    return gui_items[filter(lambda x: name in x,gui_items.keys())[0]]

def getNameGuiItem(name):
    gui_items = {m.getName().split('_')[-1]:m for m in loader.loadModel('phase_3/models/gui/tt_m_gui_mat_nameShop.bam').findAllMatches('**') if m.getName()}
    if name == 'ALL':
        return gui_items.keys()
    return gui_items[filter(lambda x: name in x,gui_items.keys())[0]]

class LaffOMeter:
    def __init__(self,frame,default=None,_spc=None,_color=None):
        self.maxhp = int(gamebase.toonAvatarStream.read('hp',15))
        self.hp = int(gamebase.toonAvatarStream.read('curhp',15))

        if default is not None: self.hp,self.maxhp = default

        if not _color:
            _color = gamebase.toonAvatarStream.read('color1',"(0,0,0)")
        _map = lambda *a,**k: tuple(map(*a,**k))
        self.color = _map(lambda x:float(x.strip('()')),_color.split(','))

        self._meter = frame.attachNewNode('meter')
        self._meter.setPos(.155,0,.15)#-1.18,0,-.85) #left, ?, top
        self._meter.setScale(0.080)

        self.reparentTo = self._meter.wrtReparentTo
        self.removeNode = self._meter.removeNode
        self.getParent = self._meter.getParent

        self._teeth = self._meter.attachNewNode('teeth')

        if not _spc: _spc = int(gamebase.toonAvatarStream.read('spc',"0"))
        self.spc = ["cat","pig","dog","horse","bear","mouse","duck","bunny","monkey"][_spc]

        self.head = self.getItem('heads/{0}head'.format(self.spc))
        self.head.reparentTo(self._meter)
        self.head.setColorScale(self.color+(1,))

        self.eyes = self.getItem('eyes')
        self.eyes.reparentTo(self._meter)

        self.totalHpText = OnscreenText(text=str(self.maxhp),parent=self.eyes,pos=(.43,0),scale=.4,mayChange=1)
        self.hpText = OnscreenText(text=str(self.hp),parent=self.eyes,pos=(-.43,0),scale=.4,mayChange=1)
        self.totalHpText.setFont(loader.loadFont('phase_3/models/fonts/ImpressBT.ttf'))
        self.hpText.setFont(loader.loadFont('phase_3/models/fonts/ImpressBT.ttf'))
        self.drawTeeth()

    def hideEyes(self):
        self.eyes.hide()

    def showEyes(self):
        self.eyes.show()

    def update(self,default = None):
        self.maxhp = int(gamebase.toonAvatarStream.read('hp',15))
        self.hp = int(gamebase.toonAvatarStream.read('curhp',15))

        if default is not None: self.hp,self.maxhp = default

        self.totalHpText.setText(str(self.maxhp))
        self.hpText.setText(str(self.hp))

        self.drawTeeth()

    def cleanTeeth(self):
        self._teeth.removeNode()
        self._teeth = self._meter.attachNewNode('teeth')

    def getItem(self,item):
        return loader.loadModel('phase_3/models/gui/laff_o_meter.bam').find("**/"+item)

    def die(self):
        self.cleanTeeth()
        self.hideEyes()

        self.getItem('frown').reparentTo(self._teeth)
        self.head.setColorScale(.3,.6,.4,1)

    def respawn(self):
        self.showEyes()
        self.drawTeeth()

        self.head.setColorScale(self.color+(1,))

    def drawTeeth(self):
        self.hpText.setText(str(self.hp))

        _ratio = float(self.hp)/self.maxhp
        smiley = 6-int(_ratio*6)

        if _ratio == 0.0: return self.die()
        else: smiley = 'tooth_'+str(smiley)

        if int(_ratio) == 1: smiley = 'smile'

        self.cleanTeeth()
        if smiley.startswith('tooth_'):
            for i in reversed(range(int(smiley[-1]),7)):
                tooth = self.getItem('*_'+str(i))
                tooth.reparentTo(self._teeth)

        else:
            teeth = self.getItem(smiley)
            teeth.reparentTo(self._teeth)

def _openBook(frame):
    Sequence(
             Func(gamebase.toonAvatar[0].b_setState,"Book"),
             Wait(0.9), #2.5 is too much!
             Func(__open,frame)
            ).start()

def __open(frame):
    gamebase.curArea.book = Book(frame)

def setupHud(frame):
    bookM = loader.loadModel('phase_3.5/models/gui/sticker_open_close_gui.bam')
    bookGeom = map(lambda x: bookM.find('**/'+x),("BookIcon_CLSD","BookIcon_OPEN","BookIcon_RLVR","BookIcon_CLSD"))

    book = DirectButton(text="",parent=base.a2dBottomRight,pos=Vec3(-.20,0,1-.82),scale=0.80,geom=bookGeom,relief=None,command = lambda: _openBook(frame),
                        clickSound=gamebase.sounds['GUI_stickerbook_open'],rolloverSound=gamebase.sounds['GUI_rollover'])

    laffmeter = LaffOMeter(base.a2dBottomLeft)

    #scM = loader.loadModel("data/models/gui/speedChatGui.bam")
    base.distMgr.menuGui = None
    speedchatButt = DirectButton(text="",parent=base.a2dTopLeft,pos=Vec3(.25,0,0.918-1),scale=1.2,color=(0,1,0,1),geom=loader.loadModel("phase_3.5/models/gui/chat_input_gui.bam").find("**/ChtBx_ChtBtn_UP"),
                                 relief=None,clickSound=gamebase.sounds['GUI_click'],rolloverSound=gamebase.sounds['GUI_rollover'])

    SCBO = frame.attachNewNode("SpeedChatOriginButton")
    SCBO.setPos(speedchatButt.getPos(frame))
    SCBO.setPos(SCBO,(-.485,0,0))
    speedchatButt["command"] = makeSCMenu
    speedchatButt["extraArgs"] = (SCBO,)

    chatbox = ClassicChatBox(base.a2dTopLeft)
    if base.isCompiled: chatbox.OldChatBoxOpen.hide() #can bypass blacklist!! not ready to go to public

    from tth.friends.FriendsPanel import FriendsListPanel as FLP

    flp = FLP(None)
    flp.hide()

    def _flObscurer(butt,goodGeom):
        def wrap(state):
            butt["geom"] = (goodGeom,(None,None,None,None))[state]
            butt["state"] = (DGG.NORMAL,DGG.DISABLED)[state]
        return wrap

    flModels = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
    flgeom = map(lambda x: flModels.find("**/FriendsBox_"+x),("Closed","Rollover"))
    flButt = DirectButton(relief=None,geom=flgeom,parent=base.a2dTopRight,pos=(-.2,0,-.2), command = flp.enter)

    flp.wrtReparentTo(flButt)
    flButt.obscure = _flObscurer(flButt,flgeom)
    return [book,laffmeter,speedchatButt,chatbox,flButt]
