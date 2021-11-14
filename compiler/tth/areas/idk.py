from __init__ import Area

from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay, TextureStage
from tth.avatar.toon import EToon

class ASTREET(Area):
    def __init__(self,tp=None):
        self.name = "A Street"
        self.music = "data/sounds/ttc/street.ogg"
        self.zoneId = 101
        
        self.avatarPN = ['wall','props']
        Area.__init__(self)

        self.avatar.setPos(-560, -30, 0)
        #self.sky = loader.loadModel("data/models/TTC/TT_sky.bam")
        #self.sky.reparentTo(self.np)
        # self.environ.reparentTo(self.sky)
        # for i in self.environ.findAllMatches('**/mickey'):
            # i.removeNode()
            # print("A mickey was removed !")
            
        self.placestreetm("street_40x40", (-560, -30, 0), (90, 0, -0))
        self.placebldg("data/models/streets/bldg/TT_A3.bam", (-600, -20, 0), 90)
        self.placetun((-580, -30, 0), 180, True)
        self.placestreetm("interior_corner_slope", (-610, 90, 0), (-180, 0, -0), True)
        self.placestreetm("street_slope_transitionL", (-580, 110, 0), (90, 0, -0), True)
        self.placestreetm("street_slope_transition_R", (-610, 80, 0), (180, 0, -0), True)
        self.placestreetm("street_outer_corner", (-580, 60, 0), (-0, 0, -0))

        
        if tp: tp.done()
        
    def placebldg(self, path, pos, h):
        self.nmodel = loader.loadModel(path)
        self.nmodel.reparentTo(self.np)
        self.nmodel.setPos(pos)
        self.nmodel.setH(h)
        
    def placestreetm(self, type, pos, hpr, ise=False):
        if ise == True:
            self.stm = loader.loadModel("data/models/streets/street_modules_enhanced.bam").find("**/"+type)
        else:
            self.stm = loader.loadModel("data/models/streets/street_modules.bam").find("**/"+type)
        self.stm.reparentTo(self.np)
        self.stm.setPos(pos)
        self.stm.setHpr(hpr)
        
    def placetun(self, pos, h, sign = False):
        tunnel = loader.loadModel("data/models/TTC/tunnel_TT.bam")
        tunnel.reparentTo(self.np)
        tunnel.setPos(pos)
        tunnel.setH(h)
        if sign:
            sign = loader.loadModel("data/models/TTC/construction_sign.bam")
            sign.reparentTo(tunnel.find("**/sign_origin"))
            sign.setPos(0,0,-17)
            sign.find("**/sign_board").setPos(0,0,-0.25)
            sign.find("**/p7_3").setPos(0,0,-0.25)
            sign.find("**/stand").setPos(0,0,-0.15)
        
    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'speeches':[],
                'gui':self.frame
                }