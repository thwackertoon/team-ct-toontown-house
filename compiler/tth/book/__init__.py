from panda3d.core import *
from direct.gui.DirectGui import *

from tth.avatar.toon import rgb2p

def getGuiItem(name):
    gui_items = {m.getName():m for m in loader.loadModel('phase_3.5/models/gui/stickerbook_gui.bam').findAllMatches('**') if m.getName()}
    if name == 'ALL': return gui_items.keys()
    return gui_items[filter(lambda x: name in x,gui_items.keys())[0]]
    
def getNameGuiItem(name):
    gui_items = {m.getName().split('_')[-1]:m for m in loader.loadModel('phase_3/models/gui/tt_m_gui_mat_nameShop.bam').findAllMatches('**') if m.getName()}
    if name == 'ALL': return gui_items.keys()
    return gui_items[filter(lambda x: name in x,gui_items.keys())[0]]
    
def getFriendGuiItem(name):
    gui_items = {m.getName():m for m in loader.loadModel('phase_3.5/models/gui/friendslist_gui.bam').findAllMatches('**') if m.getName()}
    if name == 'ALL': return gui_items.keys()
    return gui_items[filter(lambda x: name in x,gui_items.keys())[0]]
    
def getFrameItems(x): return len(x.findAllMatches("**"))-1
BUTT_SCALE = .08

class Book:
    def __init__(self,frame,page=0):
        self.cArea = gamebase.curArea
        self.cArea.disableControls()
        
        self.__bg = DirectFrame(parent=render2d,frameColor=rgb2p(13,38,102)+(1,),frameSize=(-1,1,-1,1))
        self.bg = frame.attachNewNode('bookBg')
        
        for o in self.cArea.hud: o.reparentTo(o.getParent())
        
        bookM = loader.loadModel('phase_3.5/models/gui/sticker_open_close_gui.bam')
        bookGeom = map(lambda x: bookM.find('**/'+x),("BookIcon_OPEN","BookIcon_CLSD","BookIcon_RLVR2","BookIcon_CLSD"))
        
        self.oldCmd = self.cArea.hud[0]['command']
        self.oldGeom = self.cArea.hud[0]['geom']
        self.cArea.hud[0]['command'] = self.close
        self.cArea.hud[0]['geom'] = bookGeom
        
        self.bigbook = getGuiItem('big')
        self.bigbook.reparentTo(self.bg)
        self.bigbook.setSz(1.5)
        self.bigbook.setSx(2.2)
        
        from OptionsPage import OptionsPage
        from DistrictPage import DistrictPage
        from MapPage import MapPage
        from SuitPage import SuitPage
        from DisguisePage import DisguisePage
        
        self.pages = [
                      OptionsPage,
                      DistrictPage,
                      MapPage,
                      SuitPage,
                      DisguisePage,
                      ]
                      
        self.buttons = self.bg.attachNewNode("buttons")
        self.buttons.setPos(1.025,0,.6)
        self.buttonM = loader.loadModel("phase_3.5/models/gui/sos_textures.bam")
        
        icons = map(lambda x:(x[1],self.buttonM.find("**/"+x[0])),(
                                                         ("switch",0),
                                                         ("district",1),
                                                         ("teleportIcon",2),
                                                         ("gui_gear",3),
                                                #         ("fish",4),
                                                 #        ("kartIcon",5),
                                                         ("disguiseIcon",4   +6*0),
                                                  #       ("gardenIcon",7),
                                                         )
                    )

        for i,x in icons:
            z = -getFrameItems(self.buttons)*(BUTT_SCALE+.01)
            DirectButton(
                         geom=x,scale=BUTT_SCALE,
                         parent=self.buttons,pos=(0,0,z),
                         command = self.loadPage, extraArgs = [i],
                         )
        
        self.cPage = None
        self.loadPage(page)

        #base.accept("arrow_right",self.addPageNumber)
        #base.accept("arrow_left",self.removePageNumber)
            
    def loadPage(self,index):
        if self.cPage is not None:
            self.cPage.destroy()
            
        self.cPage = self.pages[index](self)
        self.cPage.setup()
        
    def close(self):
        self.__bg.removeNode()
        self.bg.removeNode()
        
        if self.cPage: self.cPage.destroy()
        
        self.cArea.toon.b_setState("neutral")
        
        self.cArea.hud[0]['command'] = self.oldCmd
        self.cArea.hud[0]['geom'] = self.oldGeom
        
        self.cArea.enableControls()
