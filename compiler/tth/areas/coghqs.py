from hoods import *

from panda3d.core import *
from tth.avatar.toon import EToon, rgb2p
from direct.gui.DirectGui import *

import random

class BossbotHQ(Hood):
    music = "phase_12/audio/bgm/Bossbot_Entry_v"+str(random.choice(range(1,4)))+".mid"
    zoneId = 10000
    name = "AREA_HQ_BOSS"
    tunOutDelay = .5
    
    CAM_TUNNEL_DELTA = (40,70,10)
        
    def __init__(self,tp=None):
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
        self.baseline(self.signSF,'vtRemingtonPortable.ttf',(0,0,0,1),(0.2,0,0),(0.7,1,0.7),L10N('COGHQ_FRONT3'),9)

        self.kartSF = loader.loadModel("phase_12/models/bossbotHQ/Coggolf_cart3.bam")
        self.kartSF.reparentTo(self.np)
        self.kartSF.setPosHprScale(165,42,0,115.46,0,0,1,1,1)

        #Middle Six
        self.middleSix = self.environ.find("**/Gate_3")
        self.signFT = self.middleSix.find("**/sign_origin")
        self.baseline(self.signFT,'vtRemingtonPortable.ttf',(0,0,0,1),(0.2,0,0),(0.7,1,0.7),L10N('COGHQ_MIDDLE6'),9)

        self.kartFT = loader.loadModel("phase_12/models/bossbotHQ/Coggolf_cart3.bam")
        self.kartFT.reparentTo(self.np)
        self.kartFT.setPos(149,-84,0)
        self.kartFT.setHpr(56.31,0,0)

        #Back Nine
        self.backNine = self.environ.find("**/Gate_2")
        self.signNB = self.backNine.find("**/sign_origin")
        self.baseline(self.signNB,'vtRemingtonPortable.ttf',(0,0,0,1),(0.2,0,0),(0.7,1,0.7),L10N('COGHQ_BACK9'),9)

        self.kartNB = loader.loadModel("phase_12/models/bossbotHQ/Coggolf_cart3.bam")
        self.kartNB.reparentTo(self.np)
        self.kartNB.setPosHprScale(-55,17,0,255.96,0,0,1,1,1)

        #Golf Club
        self.golfClub = self.environ.find("**/GateHouse")
        self.signGC = self.golfClub.find("**/sign_origin")
        self.baseline(self.signGC,'vtRemingtonPortable.ttf',(0,0,0,1),(0.2,0,0),(0.7,1,0.7),'COUNTRY CLUB')
        
        x,y,z = self.signGC.getPos()
        self.placesign(x,y,0,0,True)
        
        #entrace
        self.entrace = self.environ.find('**/TunnelEn*')
        self.baseline(self.entrace.find('**/sign_origin'),'vtRemingtonPortable.ttf',(0,0,0,1),(0.2,0,0),(0.7,1,0.7),'MINI GOLF')
        
        self.entrace.find('**/tun*origin').setPos((4.37416, -2.15352, -16.5616))
        self.entrace.find('**/tun*origin').setH(0)
        
        from funAreas import MiniGolfZone
        self._tunnelMovie(
                          ((self.entrace,'AREA_MINIGOLF',MiniGolfZone),),tp.getTunnel()
                          )
        
        if tp:tp.done()
        
    def baseline(self,parent,font,color,pos,scale,text,ww=7):
        fonto = loader.loadFont("phase_3/models/fonts/{0}".format(font))
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

class SellbotHQ(Hood):
    music = "phase_9/audio/bgm/encntr_suit_HQ_nbrhood.mid"
    zoneId = 7000
    name = "AREA_HQ_SELL"
    tunOutDelay = .5
    
    cogPoints = (
                 (91,-203,0.3),
                 (89,-157,0.3),
                 (62,-96,0.3),
                 (39,-87,0.3),
                 (15,-88,0.3),
                 (5,-88,0.3),
                 (-5,-88,0.3),
                 (-15,-88,0.3),
                 (-48,-93,0.3),
                 (-88,-107,0.3),
                 (-94,-127,0.3),
                 (-77,-138,0.3),
                 (-15,-119,0.3),
                 (28,-111,0.3),
                 (61,-122,0.3),
                 (74,-146,0.3),
                 (82,-182,0.3),
                 (81,-203,0.3),
                 (71,-215,0.3),
                 (51,-230,0.3),
                 (25,-241,0.3),
                 (2,-245,0.3),
                 (-35,-238,0.3),
                 (-66,-218,0.3),
                 (-73,-203,0.3),
                 (-78,-178,0.3),
                 (-64,-161,0.3),
                 (-38,-147,0.3),
                 (-17,-140,0.3),
                 (39,-133,0.3),
                 (43,-125,0.3),
                 (25,-117,0.3),
                 (-45,-138,0.3),
                 (-84,-170,0.3),
                 (-80,-220,0.3),
                 (-48,-241,0.3),
                 (-29,-245,0.3),
                 (-3,-256,0.3),
                 (24,-248,0.3),
                 (54,-236,0.3),
                )
      
    cogWalkDur = 159.2
    def __init__(self,tp=None):
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
        Hood.__init__(self,"phase_9/models/cogHQ/SellbotHQExterior.bam")
        
        self.environ.reparentTo(self.np)
        self.entrace = self.np.find('**/Tunnel1')
        self.factTun = self.np.find('**/Tunnel2')

        from streets import DG_5300
        self._tunnelMovie((
                          (self.entrace,'AREA_ST_5300',DG_5300),
                          (self.factTun,'AREA_HQ_SELL_FACTORYEXT',SellbotHQFactoryExterior),
                          ),tp.getTunnel())
        
        if tp:tp.done()
        
    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
                
class SellbotHQFactoryExterior(Hood):
    music = "phase_9/audio/bgm/encntr_suit_HQ_nbrhood.mid"
    zoneId = 7100
    name = "AREA_HQ_SELL_FACTORYEXT"
    tunOutDelay = .5
    DONT_STORE = True
    
    cogPoints = ( #needs to be fixed
                 (27,-341,0.05),
                 (0,-341,0.05),
                 (-27,-341,0.05),
                 (-27,-300,0.05),
                 (13,-300,0.05),
                 (13,-278,0.05),
                 (-27,-278,0.05),
                 (-27,-260,0.05),
                 (-27,-236,0.05),
                 (-27,-212,0.05),
                 (-34,-204,0.05),
                 (-60,-200,0.05),
                 (-90,-200,0.05),
                 (-145,-200,0.05),
                 (-188,-200,0.05),
                 (-188,-167,0.05),
                 (-137,-167,0.05),
                 (-41,-167,0.05),
                 (-37,-191,0.05),
                 (-31,-200,0.05),
                 (-13,-212,0.05),
                 (13,-212,0.05),
                 (31,-200,0.05),
                 (55,-182,0.05),
                 (112,-182,0.05),
                 (165,-182,0.05),
                 (165,-200,0.05),
                 (112,-200,0.05),
                 (55,-200,0.05),
                 (34,-206,0.05),
                 (27,-212,0.05),
                 (27,-236,0.05),
                 (-13,-236,0.05),
                 (-13,-260,0.05),
                 (27,-260,0.05),
                 (27,-278,0.05),
                 (27,-300,0.05),
                 (0,-143,0.05),
                 (96,-143,0.05),
                 (96,-120,0.05),
                 (159,-120,0.05),
                 (159,18,0.05),
                 (159,120,0.05),
                 (0,111,0.05),
                 (-193,103,0.05),
                 (-187,0,0.05),
                 (-182,-144,0.05),
                 (-110,-144,0.05),
                 (-110,-80,0.05),
                 (-170,-80,0.05),
                 (-170,-24,0.05),
                 (-73,-24,0.05),
                 (-73,5,0.05),
                 (-23,5,0.05),
                 (-23,-24,0.05),
                 (-23,-120,0.05),
                 (-80,-120,0.05),
                 (-80,-143,0.05),
                 (-23,18,0.05),
                 (63,18,0.05),
                 (147,18,0.05),
                 (147,-96,0.05),
                 (-23,-96,0.05)
                )
        
    def __init__(self,tp=None):
        self.av_startpos = (
                            ((0, 0, 0),(0,0,0)),
                            )
        Hood.__init__(self,"phase_9/models/cogHQ/SellbotFactoryExterior.bam")
        
        gamebase.toonAvatarStream.write("lastArea",str(SellbotHQ).rsplit('.',1)[-1])
        gamebase.toonAvatarStream.write("lastAreaName",SellbotHQ.name)
        gamebase.toonAvatarStream.write("lastZoneId",SellbotHQ.zoneId)
        
        self.environ.reparentTo(self.np)
        self.entrace = self.np.find('**/tunnel*')

        self._tunnelMovie(
                          ((self.entrace,'AREA_HQ_SELL',SellbotHQ),),tp.getTunnel()
                          )
        
        if tp:tp.done()
        
    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
                
class CashbotHQ(Hood):
    music = "phase_9/audio/bgm/encntr_suit_HQ_nbrhood.mid"
    zoneId = 8000
    name = "AREA_HQ_CASH"
    tunOutDelay = .5
        
    def __init__(self,tp=None):
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
        Hood.__init__(self,"phase_10/models/cogHQ/CashBotShippingStation")
        
        self.environ.reparentTo(self.np)
        self.entrace = self.np.find('**/Link*1')

        from streets import DL_9200
        self._tunnelMovie(
                          ((self.entrace,'AREA_ST_9200',DL_9200),),tp.getTunnel()
                          )
        
        if tp:tp.done()
        
    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
                
class LawbotHQ(Hood):
    music = "phase_11/audio/bgm/LB_courtyard.mid"
    zoneId = 9000
    name = "AREA_HQ_LAW"
    tunOutDelay = .5
         
    cogPoints = (
                    (251,106,-68.4),
                    (170,81,-68.4),
                    (107,39,-68.4),
                    (24,78,-68.4),
                    (-55,103,-68.4),
                    (-32,17,-68.4),
                    (41,-9,-68.4),
                    (135,6,-68.4),
                    (222,44,-68.4),
                    (-10,-26,-68.4),
                    (-16,-76,-68.4),
                    (23,-122,-68.4),
                    (-26,-163,-68.4),
                    (20,-180,-68.4),
                    (75,-151,-68.4),
                    (74,-83,-68.4),
                    (148,-82,-68.4),
                    (206,-67,-68.4),
                    (257,-14,-68.4),
                    (232,24,-68.4),
                    (155,-8,-68.4),
                    (96,-39,-68.4),
                    (29,-37,-68.4),
                    (188,-100,-68.4),
                    (207,-173,-68.4),
                    (137,-243,-68.4),
                    (87,-179,-68.4),
                    (115,-101,-68.4),
                    (71,-180,-68.4),
                    (22,-197,-68.4),
                    (-11,-219,-68.4),
                    (13,-262,-68.4),
                    (-16,-306,-68.4),
                    (-30,-345,-68.4),
                    (-56,-378,-68.4),
                    (-68,-435,-68.4),
                    (-21,-474,-68.4),
                    (15,-448,-68.4),
                    (23,-371,-68.4),
                    (41,-280,-68.4),
                    (61,-219,-68.4),
                    (172,-247,-68.4),
                    (241,-315,-68.4),
                    (264,-398,-68.4),
                    (222,-452,-68.4),
                    (159,-362,-68.4),
                    (88,-314,-68.4),
                    (85,-247,-68.4),
                    (150,-258,-68.4)
                )
     
    cogWalkDur = 465
    def __init__(self,tp=None):
        self.av_startpos = (
                            ((-139.068, -188.536, -28.6182),(90,0,0)),
                            )
        Hood.__init__(self,"phase_11/models/lawbotHQ/LawbotPlaza")
        
        self.environ.reparentTo(self.np)
        self.entrace = self.np.find('**/Link*1')
        
        #the shitty DA door must be worked out (add a solid)
        self.doorDA = self.np.find('**/door_0').find('**/left*')
        self.doorDACn = CollisionNode('door_triggerPlaceholder')
        self.doorDACnP = self.doorDA.attachNewNode(self.doorDACn)
        self.doorDACn.setCollideMask(1)
        self.doorDACn.addSolid(CollisionSphere(0,0,0,10))
        #self.doorDACnP.show()
        self.doorDACnP.setPos(11,11,-20)
        self.doorDACnP.setSx(2.2)

        from streets import BR_3300
        self._tunnelMovie(
                          ((self.entrace,'AREA_ST_3300',BR_3300),),tp.getTunnel()
                          )
                          
        #self._doorMovie(((self.doorDA,"AREA_HQ_LAW_DAEXT",LawbotHQDALobby),),tp.getDoor())      
        
        if tp:tp.done()
        
    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
                
class LawbotHQDALobby(Hood): #just a prototype at the moment
    music = "phase_11/audio/bgm/LB_courtyard.mid"
    zoneId = 9100
    name = "AREA_HQ_LAW_DAEXT"
    tunOutDelay = .5
    DONT_STORE = True
        
    def __init__(self,tp=None):
        self.av_startpos = (
                            ((0, 0, 0),(0,0,0)),
                            )
        Hood.__init__(self,"phase_11/models/lawbotHQ/LB_DA_Lobby.bam")
        
        gamebase.toonAvatarStream.write("lastArea",str(LawbotHQ).rsplit('.',1)[-1])
        gamebase.toonAvatarStream.write("lastAreaName",LawbotHQ.name)
        gamebase.toonAvatarStream.write("lastZoneId",LawbotHQ.zoneId)
        
        self.environ.reparentTo(self.np)
        self.entrace = self.np.find('**/tunnel*')

        self._tunnelMovie(
                          ((self.entrace,'AREA_HQ_SELL',SellbotHQ),),tp.getTunnel()
                          )
        
        if tp:tp.done()
        
    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }