#The name is in fact a troll :P If you says my creator's name 64 times while staring strangely in front of somebody, I will appear (in your dreams, staring strangely at you saying your name 128 times) !
from __init__ import Area

from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay, TextureStage
from tth.avatar.toon import EToon

class AStreet(Area):
    def __init__(self,tp=None):
        self.name = "STest"
        self.music = "data/sounds/ttc/ttc.ogg"
        
        self.avatarPN = ['wall','props']
        Area.__init__(self,"data/models/streets/street_modules.bam")

        # self.m2 = loader.loadModel("data/models/streets/street_modules_enhanced.bam")
        # self.m2.reparentTo(self.np)
        # self.m1 = loader.loadModel("data/models/streets/street_modules.bam")
        # self.m2.reparentTo(self.np)

        
        if tp: tp.done()
        
    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'speeches':[]
                }