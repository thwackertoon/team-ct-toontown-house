# Rua do Toontorial
# Criado por: Junior, Nacib and Hugo # :D
# 15/10/2013
########################
#Why is that thing needed? ~s0r00t

from __init__ import Area
from hoods import TTCentral
from etc import *

from direct.interval.IntervalGlobal import *
from panda3d.core import Vec4, TextureStage, Texture, CollisionSphere, CollisionNode, BitMask32
from tth.avatar.toon import EToon, rgb2p
       
class Tutorial(Area):
    def __init__(self,tp=None):
        self.name = 'AREA_Toontorial'
        self.zoneId = 1
        self.music = "phase_3.5/audio/bgm/TC_SZ_activity.mid"
        
        self.avatarPN = ['wall','props']
        Area.__init__(self,"phase_3.5/models/modules/toon_interior_tutorial.bam")
        self.sky = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.sky.reparentTo(self.np)
        walltex = loader.loadTexture("phase_3.5/maps/stripeB5.jpg")
        tsw = TextureStage('tsw')
        tsw.setMode(TextureStage.MBlend)
        tsw.setColor(Vec4(rgb2p(175,241,150)+(1,)))
        self.environ.find("**/random_tc1_TI_wallpaper").setTexture(tsw, walltex)
        self.environ.find("**/random_tc1_TI_wallpaper_border").setTexture(tsw, walltex)
        
        floortex = loader.loadTexture("phase_3/maps/floor_create_toon.jpg")        
        tsf = TextureStage('tsf')
        tsf.setMode(TextureStage.MBlend)
        tsf.setColor(Vec4(rgb2p(114,55,19)+(1,)))
        self.environ.find("**/random_tc1_TI_floor").setTexture(tsf, floortex, 1)
        self.environ.reparentTo(self.np)
        self.environ.setScale((1.6,1.6,1))
        #for m in self.environ.findAllMatches('**/*wall*'):m.setColorScale(Vec4(.1,1,.1,1),1)
        #for m in self.environ.findAllMatches('**/random*'):m.setColorScale(Vec4(.1,1,.1,1),1)
        
        self.npctut = EToon(np=self.environ.find('**/npc_o*'),toontype="dog",color_head=(rgb2p(245,168,126)),color_torso=(rgb2p(245,168,126)),
                 color_legs=(rgb2p(245,168,126)),body="m",gender="shorts",legsSz=.5,headn=3,
                 autoShow=True,clt=(None,None,None))
                 
        self.npctut.anim('neutral')
        
        self.tag = OnscreenText(scale=.75, text="Tutorial Tom",bg=(.9,.9,.9,.3),fg=(1,.5,.25,1),wordwrap=8,decal=True)

        self.tag.setTextureOff()
        self.tag.setBillboardAxis()
        
        self.tag.setDepthTest(True)
        self.tag.setDepthWrite(True)
    
        self.tag.reparentTo(self.npctut._m)
        self.tag.setZ(self.npctut.hz+1)
    
        self.furniture("phase_3.5/models/modules/couch_2person.bam", "random_mo1_TI_couch_2person")
        self.furniture("phase_3.5/models/modules/couch_1person.bam", "random_mo2_TI_couch_1person")
        self.furniture("phase_3.5/models/modules/bookcase.bam", "random_mo1_TI_bookcase")
        self.furniture("phase_3.5/models/modules/bookcase_low.bam", "random_mo1_TI_bookcase_low")
        self.furniture("phase_3.5/models/modules/paper_trashcan.bam", "random_mo1_TI_paper_trashcan")
        self.furniture("phase_3.5/models/modules/chair.bam", "random_mo1_TI_chair")
        self.furniture("phase_3.5/models/modules/rug.bam", "random_mo1_TI_rug")
        self.furniture("phase_3.5/models/modules/desk_only_wo_phone.bam", "random_mo1_TI_desk_only_wo_phone")
        #self.furniture("data/models/furniture/big_planter.bam", "random_mo1_TI_big_planter") need to be fixed since before mf files x)
        self.furniture("phase_3.5/models/modules/coatrack.bam", "random_mo1_TI_coatrack")
        self.door = loader.loadModel("phase_3.5/models/modules/doors_practical.bam")
        self.door.find("**/door_skyler_ur_flat").reparentTo(self.environ.find("**/door_origin"))
        
        self.door.setDepthOffset(99999)
        self.door.setDepthTest(True)
        self.door.setDepthWrite(True)
        
        self.door.setSy(10)
        self.avatar.setPos(-5,13.1,0)
        self.avatar.setH(-4.8)
        
        self.speech = SpeechBubble(self.npctut,L10N('SPEECH_TUT_COMEHERE'))
        #self.wc.addInPattern('%in-into')
        
        #base.accept('againcollision_walls', self.onDesk)
        
        self.csDesk = CollisionSphere(0,0,0,self.npctut._m.getBounds().getRadius()*1.3)
        cnode = CollisionNode('desk')
        self.cnodePath = self.npctut._toon.attachNewNode(cnode)
        self.cnodePath.node().addSolid(self.csDesk)
        cnode.setIntoCollideMask(BitMask32(8))
        cnode.setFromCollideMask(BitMask32(8))
        if -1>0 or base.isInjectorOpen: #if is debugging will show. if you remove the "-" will show.
            self.cnodePath.show()
            self.cNodepath.show()
        
        self.collDict = {cnode:self.onDesk}
        
        if base.isInjectorOpen: base.cTrav.showCollisions(render)# crash
        
        if tp: tp.done()
        
    def onDesk(self,entry):
        if not self.canMove: return
        print "!DESK!"
        self.canMove = False
        
        self.cnodePath.removeNode()
        
        if self.speech.exists: self.speech.frame.hide()   
        Sequence(Func(lambda *a,**k:SpeechBubble(self.npctut,L10N('SPEECH_TUT_GOTOTTC'))),
                 Wait(6),Func(self._go_ttc)).start()
        
        #hide toon and place camera
        self.toon._toon.hide()
        base.cam.reparentTo(self.npctut._m)
        
        base.cam.setPos(0,20,5)
        base.cam.setH(180)
        
    def furniture(self, model, node):
        nmodel = loader.loadModel(model)
        nmodel.reparentTo(self.environ.find("**/"+node))
        
    def _go_ttc(self,*a,**k):
        self.canMove = True
        self.toon._toon.show()
        base.cam.setPos(0, -20, 4.7)
        base.cam.setH(0)
        base.cam.reparentTo(self.avatar)
        if not base.isInjectorOpen: Teleporter(TTCentral,'AREA_TTC').go()
        
    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
        