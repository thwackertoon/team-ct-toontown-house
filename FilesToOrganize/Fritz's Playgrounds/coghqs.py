from hoods import *

from panda3d.core import *
from tth.avatar.toon import EToon, rgb2p
from direct.gui.DirectGui import *

import random

class BossbotHQ(Hood):
    def __init__(self,tp=None):
        self.music = "phase_12/audio/bgm/Bossbot_Entry_v"+str(random.choice(range(1,4)))+".mid"
        self.zoneId = 10000
        self.name = "AREA_HQ_BOSS"
        
        self.av_startpos = (
                            ((0, 0, 0.0158539),(-295.458, 0, 0)),
                            ((-8.45168, 29.2063, 0.0158539),(-368.019, 0, 0)),
                            ((2.20723, 56.7239, 0.0158539),(-392.864, 0, 0)),
                            ((28.9457, 72.9393, 0.0158539),(-460.487, 0, 0)),
                            ((55.0844, 92.6239, 0.0158539),(-390.817, 0, 0)),
                            ((78.1767, 102.347, 0.0158539),(-487.704, 0, 0)),
                            ((118.244, 63.8471, 0.0158539),(-481.462, 0, 0)),
                            ((126.655, 48.093, 0.0158539),(-532.277, 0, 0)),
                            ((121.437, 12.2197, 0.0158539),(-585.351, 0, 0)),
                            ((116.987, -9.96141, 0.0158539),(-516.87, 0, 0)),
                            ((111.204, -45.1401, 0.0158539),(-574.312, 0, 0)),
                            ((69.0051, -60.0332, 0.0158539),(-702.407, 0, 0))
                            )
        Hood.__init__(self,"phase_12/models/bossbotHQ/CogGolfHub.bam")
        
        self.environ.reparentTo(self.np)

        #Front Three

        self.frontThree = self.environ.find("**/Gate_4")
        self.signSF = self.frontThree.find("**/sign_origin")
        self.baseline(self.signSF,'vtRemingtonPortable.ttf',(0,0,0,1),(0.2,-0.25,0),(0.7,1,0.7),'THE FRONT THREE',9)

        self.kartSF = loader.loadModel("phase_12/models/bossbotHQ/Coggolf_cart3.bam")
        self.kartSF.reparentTo(self.np)
        self.kartSF.setPosHprScale(165,42,0,115.46,0,0,1,1,1)

        #Middle Six
        self.middleSix = self.environ.find("**/Gate_3")
        self.signFT = self.middleSix.find("**/sign_origin")
        self.baseline(self.signFT,'vtRemingtonPortable.ttf',(0,0,0,1),(0,-0.25,0),(0.7,1,0.7),'THE MIDDLE SIX',9)

        self.kartFT = loader.loadModel("phase_12/models/bossbotHQ/Coggolf_cart3.bam")
        self.kartFT.reparentTo(self.np)
        self.kartFT.setPos(149,-84,0)
        self.kartFT.setHpr(56.31,0,0)

        #Back Nine
        self.backNine = self.environ.find("**/Gate_2")
        self.signNB = self.backNine.find("**/sign_origin")
        self.baseline(self.signNB,'vtRemingtonPortable.ttf',(0,0,0,1),(0,-0.25,0),(0.7,1,0.7),'THE BACK NINE',9)

        self.kartNB = loader.loadModel("phase_12/models/bossbotHQ/Coggolf_cart3.bam")
        self.kartNB.reparentTo(self.np)
        self.kartNB.setPosHprScale(-55,17,0,255.96,0,0,1,1,1)

        #Golf Club
        self.golfClub = self.environ.find("**/GateHouse")
        self.signGC = self.golfClub.find("**/sign_origin")
        self.baseline(self.signGC,'vtRemingtonPortable.ttf',(0,0,0,1),(0,-0.5,0),(1.0,1.3,0.7),'COUNTRY CLUB',13)
        
        x,y,z = self.signGC.getPos()
        self.placesign(x,y,0,0,True)
        
        #entrace
        self.entrace = self.environ.find('**/TunnelEn*')
        self.baseline(self.entrace.find('**/sign_origin'),'vtRemingtonPortable.ttf',(0,0,0,1),(0.2,-0.25,0),(1,1.3,0.7),'MINI GOLF',6)
        from funAreas import *
        Tunnel(self.entrace,BitMask32(8),self,(MiniGolfZone,'AREA_MINIGOLF'))
        
        if tp:tp.done()
        
    def baseline(self,parent,font,color,pos,scale,text,ww=7):
        fonto = loader.loadFont("data/fonts/{0}".format(font))
        frame = DirectFrame(frameColor=(0,0,0,0),parent=parent)
        frame.setY(-.2)
        self.text = OnscreenText(text=text,font=fonto,pos=pos,scale=scale,parent=frame,fg=color,wordwrap=ww)
    
    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
