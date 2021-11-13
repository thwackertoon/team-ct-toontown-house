from __init__ import Area, Tunnel

from panda3d.core import *
from tth.avatar.toon import EToon, rgb2p
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.actor.Actor import *
import random
from tth.fishing.FishingHandler import *

from tth.effects.FireworkShow import *
       
class Hood(Area):

    PREFIX2PHASE = {
                    'TT':'4',
                    'TTC':'4',
                    
                    'DD':'6',
                    'DG':'8',
                    'MM':'6',
                    'BR':'8',
                    'DL':'8',
                    'FF':'14',
                    }
                    
    def __init__(self,*a,**kw):
        Area.__init__(self,*a,**kw)
        self.haveFires = False
                    
    def startFires(self,t):
        self.haveFires = True
        color = LerpColorInterval(self.sky,3,Vec4(0,0,0,1))
        color.start(t)
        self.startFireworks(t)
        
    def restartSky2Theme(self):
        self.haveFires = False
        self.sky.setColor(255,255,255)
        self.newtheme.stop()
        self.theme.play()
       
    def startFireworks(self,t):
        self.theme.stop()
        self.newtheme = loader.loadMusic("data/sounds/fireworks.mp3")
        self.newtheme.play()
        self.rocket.loop('launch')
        self.lnch = loader.loadSfx("data/sounds/rocket_launch.mp3")
        self.lnch.play()
        seq = Sequence()
        seq.append(Wait(4)) #-_- can't you create one sequence?
        seq.append(Func(self.firework,(0,-270,50)))
        seq.append(Wait(3))
        seq.append(Func(self.hideRocket))
        seq.append(Func(self.firework,(50,-270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(100,270,50)))
        seq.append(Wait(4))
        seq.append(Func(self.firework,(0,270,50)))
        seq.append(Wait(1))
        seq.append(Func(self.firework,(110,270,50)))
        seq.append(Wait(3))
        seq.append(Func(self.firework,(-250,270,50)))
        seq.append(Wait(1))
        seq.append(Func(self.firework,(250,270,50)))
        seq.append(Wait(3))
        seq.append(Func(self.firework,(0,-270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(80,270,50)))
        seq.append(Wait(4))
        seq.append(Func(self.firework,(250,270,50)))
        seq.append(Wait(6))
        seq.append(Func(self.firework,(-250,270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(0,-270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(80,270,50)))
        seq.append(Wait(3))
        seq.append(Func(self.firework,(-250,270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(250,-270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(80,270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(0,-270,50)))
        seq.append(Wait(4))
        seq.append(Func(self.firework,(-250,270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(80,270,50)))
        seq.append(Wait(3))
        seq.append(Func(self.firework,(80,270,50)))
        seq.append(Wait(5))
        seq.append(Func(self.firework,(0,-270,50)))
        seq.append(Wait(1))
        seq.append(Func(self.restartSky2Theme))
        seq.append(Func(self.showRocket))
        seq.start(t)

    def firework(self,pos):
        FireworkShow(pos)
        
    def hideRocket(self):
        self.rocket.hide()
        
    def showRocket(self):
        self.rocket.show()
        
    def loadRocket(self,pos=(11,-60,14)):
        self.rocket = Actor("phase_13/models/parties/rocket_model",
                            {"launch":"phase_13/models/parties/rocket_launch"})
        self.rocket.reparentTo(self.np)
        self.rocket.setPos(pos)
                    
    def enterTrolley(self,entry):
        try:
            assert not base.isCompiled
            self.trolleyMgr.d_requestBoard(self.toon.doId)
        except:
            pass
 
    def door(self,doors,type,color,parent):
        door = loader.loadModel("phase_3.5/models/modules/doors_{0}.bam".format(doors)).find('**/'+type)
        door.reparentTo(parent)
        door.setColor(color)
        
    def baseline(self,parent,font,color,pos,scale,textx,ww):
        fonto = loader.loadFont("data/fonts/{0}".format(font))
        frame = DirectFrame(frameColor=(0,0,0,0),parent=parent)
        frame.setY(-.2)
        self.text = OnscreenText(text=textx,font=fonto,pos=pos,scale=scale,parent=frame,fg=color,wordwrap=ww)
        
    def placelight(self,pos,h):
        l = loader.loadModel("phase_3.5/models/props/streetlight_TT.bam")
        l.reparentTo(self.np)
        l.setPos(pos)
        l.setH(h)
        return l
        
    def placebldg(self, path, pos, h):
        nmodel = loader.loadModel(path)
        nmodel.reparentTo(self.np)
        nmodel.setPos(pos)
        nmodel.setH(h)
        return nmodel
       
    def placetun(self, pos, h, sign = False, hood = 'TT'):
        tunnel = loader.loadModel("phase_{0}/models/modules/safe_zone_tunnel_{1}.bam".format(self.PREFIX2PHASE[hood],hood))
        tunnel.reparentTo(self.np)
        tunnel.setPos(pos)
        tunnel.setH(h)
        if sign:
            sign = loader.loadModel("phase_4/models/props/construction_sign.bam")
            sign.reparentTo(tunnel.find("**/sign_origin"))
            sign.setPos(0,0,-17)
            sign.find("**/sign_board").setPos(0,0,-0.25)
            sign.find("**/p7_3").setPos(0,0,-0.25)
            sign.find("**/stand").setPos(0,0,-0.15)
            
        return tunnel
        
    def placesign(self, x, y, z, h, full = False):
        sign = loader.loadModel("phase_4/models/props/construction_sign.bam")
        sign.reparentTo(self.np)
        sign.setX(x)
        sign.setY(y)
        sign.setZ(z)
        sign.setH(h)
        if not full:
            sign.find("**/sign_board").removeNode()
            sign.find("**/p7_3").removeNode()
            sign.find("**/stand").removeNode()
            
        return sign
        
    def sign(self,nbr,parent,sign,pos,hpr,scale):
        sign = loader.loadModel("phase_{0}/models/props/signs_{1}.bam".format(self.PREFIX2PHASE[nbr],nbr)).find("**/"+sign)
        sign.reparentTo(parent.find("**/sign_origin"))
        sign.setPos(pos)
        sign.setHpr(hpr)
        sign.setScale(scale)
        return sign
        
    def makeMask(self,wall,parent): 
        toMask = wall.find("**/wall_collide")
        toMask.node().setFromCollideMask(BitMask32(8))
        toMask.reparentTo(parent)
        
    def placewall(self, pos, type, h, width, height, color):
        wallm = loader.loadModel("phase_3.5/models/modules/walls.bam")
        wall = wallm.find("**/"+type)
        wall.reparentTo(self.np)
        wall.setPos(pos)
        wall.setH(h)
        wall.setSz(height)
        wall.setSx(width)
        wall.setColor(color)
        self.makeMask(wallm,wall)
        return wall
 
    def placelight_TT(self, type, pos, h, arg):
        if arg == 1:
            light = loader.loadModel('phase_3.5/models/props/streetlight_TT.bam').find('**/'+type)
        elif arg == 2:
            light = loader.loadModel('phase_3.5/models/props/tt_m_ara_TT_streetlight_winter.bam').find('**/'+type)
        light.reparentTo(self.np)
        light.setPos(pos)
        light.setH(h)
        return light
 
    def placetree_TT(self, type, pos, h, arg=1):
        if arg == 1:
            tree = loader.loadModel('phase_3.5/models/props/trees.bam').find('**/'+type)
        elif arg == 2:
            tree = loader.loadModel('phase_3.5/models/props/winter_trees.bam').find('**/'+type)
        tree.reparentTo(self.np)
        tree.setPos(pos)
        tree.setH(h)
        return tree
 
    def placetree_FF(self, x, y):
        tree = loader.loadModel('phase_14/models/modules/tree_FF.bam')
        tree.reparentTo(self.np)
        tree.setPos(x,y,0)
        return tree
 
    def placefence_FF(self, pos, h):
        fence = loader.loadModel('phase_5.5/models/estate/terrain_fence.bam')
        fence.reparentTo(self.np)
        fence.setPos(pos)
        fence.setH(h)
        fence.setScale(0.75)
        return fence
 
    def addCollisionSphere(self,pos,scale):
        CS = render.attachNewNode(CollisionNode('colNode'))
        CS.node().addSolid(CollisionSphere(pos,scale))
 
class OldTTCentral(Hood):
    def __init__(self,tp=None):
        self.name = "AREA_TTC"
        self.zoneId = 1000
        self.music = "data/sounds/ttc/ttc.ogg"
        
        self.av_startpos = (
        ((-11.03705883026123,39.30888748168945,4.015645503997803),(-545.7789916992188,0.0,0.0)),
        ((14.714707374572754,2.844557762145996,4.027131080627441),(-492.5708312988281,0.0,0.0)),
        ((25.963918685913086,-24.225643157958984,0.015818731859326363),(-533.1298217773438,0.0,0.0)),
        ((18.48322105407715,-37.39312744140625,-0.5424529314041138),(-579.6152954101562,0.0,0.0)),
        ((-23.09368133544922,-49.44618225097656,-3.3533806800842285),(-608.7874755859375,0.0,0.0)),
        ((-11.975284576416016,-115.15393829345703,0.018701769411563873),(-515.4699096679688,0.0,0.0)),
        ((52.929527282714844,-111.75133514404297,0.5203400254249573),(-463.4405822753906,0.0,0.0)),
        ((67.84265899658203,-53.23139572143555,0.025164341554045677),(-362.22943115234375,0.0,0.0)),
        ((72.93415069580078,-3.088984966278076,0.43976959586143494),(-393.5452575683594,0.0,0.0)),
        ((113.36840057373047,20.807981491088867,2.516672134399414),(-411.7684326171875,0.0,0.0)),
        ((127.08181762695312,45.851768493652344,2.516672134399414),(-358.1191711425781,0.0,0.0)),
        ((112.93789672851562,68.28999328613281,2.516672134399414),(-312.8993835449219,0.0,0.0)),
        ((-73.6427993774414,7.083807468414307,2.0421409606933594),(-297.6528625488281,0.0,0.0)),
        ((-113.28948974609375,75.28752899169922,2.515838623046875),(-581.64599609375,0.0,0.0))
        )
        
        Hood.__init__(self,"data/models/TTC/ttc.bam") #recomp causes texture problems for me #can you recompile it for yourself?

        self.sky = loader.loadModel("data/models/TTC/TT_sky.bam")
        self.sky.reparentTo(self.np)
        self.sky.setScale(2)
 
        self.environ.reparentTo(self.np)

        self.placebldg("data/models/TTC/gazebo.bam", (10.8,-59.9,-2), -268) #thanks to JuniorCog for the positions
        
        tr = self.placebldg("data/models/TTC/trolleyTT.bam", (83,-118,0.4), 218.5)
        #for m in tr.findAllMatches("**/tunn*"): m.removeNode()
        
        self.placebldg("data/models/TTC/toonhall.bam", (-18.1796,103.6656,4), -360)
        self.placebldg("data/models/TTC/library.bam", (45.9,93,4), 270)
        self.placebldg("data/models/TTC/bank.bam", (-36.1796,58.6656,4), -270)
        self.placebldg("data/models/TTC/school_house.bam", (125,140,2.5), -45)
        self.placebldg("data/models/TTC/gagShop_TT.bam", (91,-90,0.4), 800)
        self.placebldg("data/models/TTC/clothshopTT.bam", (-110,122,2), -5)
        self.placebldg("data/models/TTC/petshopTT.bam", (-70,-123,0.4), 120)
        self.placebldg("data/models/TTC/hqTT.bam", (-29.1796,26.6656,4), 230)
        self.placebldg("data/models/TTC/partyGate_TT.bam", (154,95,2.60), -55)
        self.speedwayTun = self.placebldg("data/models/TTC/Speedway_Tunnel.bam", (-172,22,3), 300)
        
        from funAreas import Speedway
        Tunnel(self.speedwayTun, BitMask32(8), self, (Speedway,'AREA_SPEEDWAY'))
                
        self.placetun((-56.6, -243, -6.3), 360, True)
        self.placetun((209,-65,-3.7), 420, True)
        self.ddkTunnel = self.placetun((-178,32,-6.3), 261, False)
        Tunnel(self.ddkTunnel, BitMask32(8), self, (Dock,'AREA_DDK'))
        
        self.placesign(74.7426, -131.237, 0.4, -145, True)
        self.placesign(88.0317, -112.015, 0.516633, -120.000015259, True)
        self.placesign(52.3783, -141.175, 0.516633, -160.0, True)
        self.placesign(31.9725, -145.567, 0.516633, -159.999969482, True)
        
        self.placewall((87.6,-111.073,0.5),"wall_lg_brick_ur",-119,9,10,(0.5, 0.9, 0.33, 1))
        self.placewall((87.6,-111.073,10.5),"wall_lg_brick_ur",-119,9,10,(0.5, 0.9, 0.33, 1))
        self.placewall((91.77,-103.573,0.5),"wall_sm_cement_ur",-119,9,20,1)
        self.placewall((95.94,-96.073,0.5),'wall_md_dental_ul',-119,9,10,(1, 0.9, 0.33, 1))
        self.placewall((95.94,-96.073,10.5),"wall_md_dental_ul",-119,9,10,(1, 0.9, 0.33, 1))
        self.placewall((59.69,-137.525,0.5),'wall_md_pillars_ul',198,19,20,(1, 0.9, 0.33, 1))

        if tp: tp.done()
        
    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
  
class TTCentral(Hood):
    def __init__(self,tp=None):
        self.name = "AREA_TTC"
        self.zoneId = 1000
        self.music = "data/sounds/hoods/ttc/ttc.ogg"
        
        self.av_startpos = (
                            ((225.436, 128.112, -2.98415),(44.7877, 0, 0)),
                            ((197.028, 132.371, -5.36338),(99.4396, 0, 0)),
                            ((167.44, 124.961, -4.96797),(118.174, 0, 0)),
                            ((113.385, 123.432, 0.221016),(44.7238, 0, 0)),
                            ((117.516, 144.381, 1.01667),(-1.27803, 0, 0)),
                            ((85.9526, 159.852, 1.01585),(89.1646, 0, 0)),
                            ((149.311, 192.369, -0.811632),(-27.174, 0, 0)),
                            ((149.418, 281.535, -0.483394),(-205.42, 0, 0)),
                            ((86.847, 72.4855, -2.96953),(-139.41, 0, 0)),
                            ((71.9911, 52.8175, -0.90902),(-304.261, 0, 0)),
                            ((14.6187, 78.9323, -0.484146),(-317.732, 0, 0)),
                            ((-29.663, 116.255, -0.484157),(-525.121, 0, 0)),
                            )
        
        Hood.__init__(self,"phase_4/models/neighborhoods/toontown_central.bam")
        
        self.sky = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.sky.reparentTo(self.np)
        self.sky.setScale(2)
        self.skyFog = Fog("Sky Fog")
        self.skyFog.setExpDensity(0.001)
        self.sky.setFog(self.skyFog)
 
        self.environ.reparentTo(self.np)
        
        self.environ.find('**/hill').removeNode()
        self.environ.find('**/base_grass').setScale(1.5)
        self.bd = loader.loadModel("phase_6/models/karting/GasolineAlley_TT.bam")
        self.backdrop = self.bd.find('**/environment_background')
        self.backdrop.reparentTo(self.environ)
        self.backdrop.setScale(1.2,1.2,1)
        self.backdrop.setPos(-70,50,0)
        self.backdrop.setHpr(45,0,0)
        self.fence7 = loader.loadModel('phase_3.5/models/modules/wood_fence.bam') 
        self.fence7.reparentTo(self.environ) 
        self.fence7.setPos(22.36,-148.113,0.5) 
        self.fence7.setH(723.5)
        
        self.tunnel1 = self.placetun((-56.6, -238, -6.3), 360, True)
        self.sign1 = loader.loadModel("phase_3.5/models/props/tunnel_sign_orange.bam")
        self.sign1.reparentTo(self.tunnel1.find("**/sign_origin"))
        self.sign1.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon1 = loader.loadModel("phase_3.5/models/props/mickeySZ.bam")
        self.icon1.reparentTo(self.sign1.find("**/g1"))
        self.icon1.setPos(0,-.1,1.6)
        self.icon1.setScale(1.9)
        self.baseline(self.sign1,'MickeyFont.bam',(0,0.501961,0,1),(0,-1,0),(1.1,1,.9),"Loopy Lane Toontown Central",12)

        self.tunnel2 = self.placetun((209,-65,-3.7), 420, True)
        self.sign2 = loader.loadModel("phase_3.5/models/props/tunnel_sign_orange.bam")
        self.sign2.reparentTo(self.tunnel2.find("**/sign_origin"))
        self.sign2.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon2 = loader.loadModel("phase_3.5/models/props/mickeySZ.bam")
        self.icon2.reparentTo(self.sign2.find("**/g1"))
        self.icon2.setPos(0,-.1,1.6)
        self.icon2.setScale(1.9)
        self.baseline(self.sign2,'MickeyFont.bam',(0,0.501961,0,1),(0,-1,0),(1.1,1,.9),"Silly Street Toontown Central",12)

        self.tunnel3 = self.placetun((-176,32,-6.3), 261, False)
        Tunnel(self.tunnel3,BitMask32(8),self,(Dock,'AREA_DDK'))
        self.sign3 = loader.loadModel("phase_3.5/models/props/tunnel_sign_orange.bam")
        self.sign3.reparentTo(self.tunnel3.find("**/sign_origin"))
        self.sign3.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon3 = loader.loadModel("phase_3.5/models/props/mickeySZ.bam")
        self.icon3.reparentTo(self.sign3.find("**/g1"))
        self.icon3.setPos(0,-.1,1.6)
        self.icon3.setScale(1.9)
        self.baseline(self.sign3,'MickeyFont.bam',(0,0.501961,0,1),(0,-1,0),(1.1,1,.9),"Punchline Place Toontown Central",14)

        self.speedway = self.placebldg("phase_4/models/modules/Speedway_Tunnel.bam", (-172,22,3), 305)
        
        from funAreas import Speedway
        Tunnel(self.speedway,BitMask32(8),self,(Speedway,'AREA_SPEEDWAY'))
        self.baseline(self.speedway.find("**/sign_origin"),'MickeyFont.bam',(0.00392157,0.403922,0.803922,1),(0.57014,-3.391417,0),(2.67969,2.5,2.12201),L10N('AREA_SPEEDWAY'),7)
        self.baseline(self.speedway.find("**/sign_origin"),'MickeyFont.bam',(0.00392157,0.803922,0.403922,1),(2.17014,0.591417,0),(1.67969,1.5,2.12201),'Toontown House',7)

        self.trolley = self.placebldg("phase_4/models/modules/trolley_station_TT.bam", (83.15,-118.85,0.4), 218.5)
        
        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))
        
        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley
        
        self.baseline(self.trolley.find("**/sign_origin"),'MickeyFont.bam',(0.701961,0,0,1),(0.5,0,1.33),(2,2.5,1.4),'Games',7)
        self.baseline(self.trolley.find("**/sign_origin"),'MickeyFont.bam',(0.992157,0.968627,0.00784314,1),(0.5,-2,-2.33),(2.4,2.3,1.4),'Trolley',7)

        self.building1 = Actor("phase_5/models/char/tt_r_ara_ttc_B2.bam",{"dance":"phase_5/models/char/tt_a_ara_ttc_B2_dance.bam"})
        self.building1.reparentTo(self.np)
        self.building1.loop("dance")
        self.building1.setPos(37,-143,0)
        self.building1.setH(553)
        self.loony = self.sign('TTC',self.building1,'TTC_sign2',(-0.35,0,-1.3),(0,0,0),(0.9,1,0.7))
        self.baseline(self.loony,'MickeyFont.bam',(1,0.501961,0,1),(0,-0.4,0),(1.5,1.8,1.8),"Loony Labs",7)
        self.loony.setR(10)
        self.rock1 = self.loony.hprInterval(1,(0,0,-10))
        self.rock2 = self.loony.hprInterval(1,(0,0,8))
        self.rock = Sequence(self.rock1,self.rock2)
        self.rock.loop()
 
        self.library = self.placebldg("phase_4/models/modules/library.bam", (45.9,93,4), 270)
        self.door('practical','door_double_round_ur',(0.88,0.45,0.38,1),self.library.find('**/library_door_origin'))
        self.libraryName = "Library"

        self.bank = self.placebldg("phase_4/models/modules/bank.bam", (-36.1796,58.6656,4), -270)
        self.door('practical','door_double_round_ur',(0.88,0.45,0.38,1),self.bank,'bank_door_origin')
        self.baseline(self.bank.find("**/sign_origin"),'MickeyFont.bam',(1,0.662745,0.32549,1),(0,-1.58,0),(2.9,1.7,3.4),L10N('PROP_BANK'),7)

        self.schoolHouse = self.placebldg("phase_4/models/modules/school_house.bam", (-66,-126,0), 135)
        self.door('practical','door_double_square_ur',(0.88,0.45,0.38,1),self.schoolHouse,'school_door_origin')
        self.sign('TTC',self.schoolHouse,'TTC_sign3',(-0.45,0,0.3),(0,0,0),(0.9,1,0.9))
        self.baseline(self.schoolHouse.find("**/sign_origin"),'MickeyFont.bam',(1,0.501961,0,1),(-0.35,1,0),(1.5,1,1.8),L10N('PROP_SCHOOLHOUSE'),7)
 
        self.clothshop = self.placebldg("phase_4/models/modules/clothshopTT.bam", (-118,125,2), 25)
        self.baseline(self.clothshop.find("**/sign_origin"),'MickeyFont.bam',(1,0.611765,0.423529,1),(0,-0.5,0),(1.7,1.6,1.7),L10N('PROP_CLOTHSTORE'),9)
        self.door('practical','door_double_clothshop',(0.91,0.34,0.34,1),self.clothshop.find('**/door_origin'))

        self.hall = self.placebldg("phase_4/models/modules/toonhall.bam", (-22.1796,119.6656,4.03), -360)
        self.door('practical','door_double_round_ur',(0.88,0.45,0.38,1),self.hall,'toonhall_door_origin')
        self.baseline(self.hall.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(0.3,-0.75,-1.4),(2.2,1.7,2.3),"Flippy\'s ToonHall",6)

        self.placebldg("phase_4/models/modules/gazebo.bam", (10.8,-59.9,-2), -268)

        self.signDG = loader.loadModel("phase_4/models/props/neighborhood_sign_DG.bam")
        self.signDG.reparentTo(self.tunnel2.find("**/sign_origin"))
        self.signDG.setPos(-13,-1.5,-17.35)
        self.signDG.setHpr(0,0,0)
        self.signDG1 = loader.loadModel("phase_4/models/props/neighborhood_sign_DG.bam")
        self.signDG1.reparentTo(self.tunnel2.find("**/sign_origin"))
        self.signDG1.setPos(13,-1.5,-17.35)
        self.signDG1.setHpr(180,0,0)

        self.signDD = loader.loadModel("phase_4/models/props/neighborhood_sign_DD.bam")
        self.signDD.reparentTo(self.tunnel3.find("**/sign_origin"))
        self.signDD.setPos(-13,-1.5,-17.35)
        self.signDD.setHpr(0,0,0)
        self.signDD1 = loader.loadModel("phase_4/models/props/neighborhood_sign_DD.bam")
        self.signDD1.reparentTo(self.tunnel3.find("**/sign_origin"))
        self.signDD1.setPos(13,-1.5,-17.35)
        self.signDD1.setHpr(180,0,0)

        self.signMM = loader.loadModel("phase_4/models/props/neighborhood_sign_MM.bam")
        self.signMM.reparentTo(self.tunnel1.find("**/sign_origin"))
        self.signMM.setPos(-13,-1.5,-17.35)
        self.signMM.setHpr(0,0,0)
        self.signMM1 = loader.loadModel("phase_4/models/props/neighborhood_sign_MM.bam")
        self.signMM1.reparentTo(self.tunnel1.find("**/sign_origin"))
        self.signMM1.setPos(13,-1.5,-17.35)
        self.signMM1.setHpr(180,0,0)
 
        self.pier1 = loader.loadModel("phase_4/models/props/piers_tt.bam")
        self.pier1.reparentTo(self.np)
        self.pier1.setPos(-33,-57,-3.59855)
        self.pier1.setHpr(210,0,0)
        self.pier2 = loader.loadModel("phase_4/models/props/piers_tt.bam")
        self.pier2.reparentTo(self.np)
        self.pier2.setPos(-40.62,-65.49,-3.64)
        self.pier2.setHpr(240,0,0)
        self.pier3 = loader.loadModel("phase_4/models/props/piers_tt.bam")
        self.pier3.reparentTo(self.np)
        self.pier3.setPos(-43.64,-77.15,-3.59)
        self.pier3.setHpr(270,0,0)
        self.pier4 = loader.loadModel("phase_4/models/props/piers_tt.bam")
        self.pier4.reparentTo(self.np)
        self.pier4.setPos(-41.37,-87.36,-3.56)
        self.pier4.setHpr(310,0,0)

        self.placebldg("phase_3.5/models/props/big_planter.bam", (-50,21,5), 0)
        self.placebldg("phase_3.5/models/props/big_planter.bam", (50,21,5), 0)
        self.placebldg("phase_4/models/props/toontown_central_fountain.bam", (3,63,4), 0)
        self.placebldg("phase_4/models/props/mickey_on_horse.bam", (-121,77,2), 0)

        self.gagShop = self.placebldg("phase_4/models/modules/gagShop_TT.bam", (93,-89,0.4), 800)
        self.door('practical','door_double_square_ur',(1,0.63,0.38,1),self.gagShop.find('**/door_origin'))

        self.placewall((87.6,-111.073,0.5),"wall_lg_brick_ur",-119,9,10,(0.5, 0.9, 0.33, 1))
        self.placewall((87.6,-111.073,10.5),"wall_lg_brick_ur",-119,9,10,(0.5, 0.9, 0.33, 1))
        self.placewall((91.77,-103.573,0.5),"wall_sm_cement_ur",-119,9,20,1)
        self.placewall((95.94,-96.073,0.5),'wall_md_dental_ul',-119,9,10,(1, 0.9, 0.33, 1))
        self.placewall((95.94,-96.073,10.5),"wall_md_dental_ul",-119,9,10,(1, 0.9, 0.33, 1))
        self.placewall((59.69,-137.525,0.5),'wall_md_pillars_ul',198,19,20,(1, 0.9, 0.33, 1))

        self.hq = self.placebldg("phase_3.5/models/modules/hqTT.bam", (-29.1796,27.6656,4), 225)
        self.peris = Actor("phase_3.5/models/props/HQ_periscope-mod.bam",{"chan":"phase_3.5/models/props/HQ_periscope-chan.bam"})
        self.peris.reparentTo(self.hq)
        self.peris.setPos(7.17,-7.67,19.07)
        self.peris.setHpr(110,0,0)
        self.peris.setScale(4)
        self.peris.loop('chan')
        self.teles = Actor("phase_3.5/models/props/HQ_telescope-mod.bam",{"chan":"phase_3.5/models/props/HQ_telescope-chan.bam"})
        self.teles.reparentTo(self.hq)
        self.teles.setPos(7.003,0,13.191)
        self.teles.setHpr(168,81,0)
        self.teles.setScale(4)
        self.teles.loop('chan')

        self.pet = self.placebldg("phase_4/models/modules/PetShopExterior_TT.bam", (-167,88,3), 80)
        self.door('practical','door_double_round_ur',(1,0.87,0.38,1),self.pet.find('**/door_origin'))
        self.baseline(self.pet.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(-0.0715486,0.575594,0),(1.58014,1.5,2.42354),L10N("PROP_PETSHOP"),9)
 
        self.mickey = Actor("phase_3/models/char/mickey-1200.bam",{"wait":"phase_3/models/char/mickey-wait.bam"}) 
        self.mickey.reparentTo(self.np) 
        self.mickey.loop("wait") 
        self.mickey.setPos(0,10,4)
        self.mickey.setHpr(180,0,0) 
        fonto = loader.loadFont("phase_3/models/fonts/MickeyFont.bam")
        frame = DirectFrame(frameColor=(0,0,0,0),parent=self.mickey)
        frame.setY(-.2)
        self.text = OnscreenText(text="Mickey",font=fonto,pos=(0,4,0),scale=1,parent=frame,fg=(1,1,0.7,1),wordwrap=9)
        self.text.setBillboardAxis(1)
        
        self.fishs = Actor("phase_4/models/props/SZ_fish-mod.bam",{"swim":"phase_4/props/props/SZ_fish-swim.bam"})
        self.fishs.reparentTo(self.pet)
        self.fishs.setScale(1)
        self.fishs.loop('swim')

        self.gate = self.placebldg("phase_4/models/modules/partyGate_TT.bam", (154,95,2.60), -55)

        self.birds = []
        for i in xrange(3): self.birds.append(loader.loadSfx("data/sounds/TT_bird{0}.mp3".format(i+1)))
        seq = Sequence(Func(self.randomSounds),Wait(1),
                       Func(self.randomSounds),Wait(3),
                       Func(self.randomSounds),Wait(2))
        seq.loop()
 
        self.setHolidayProps(None)
        
        if tp: tp.done()

    def decorationProps(self, arg):
        if arg == 1:
            ropes = loader.loadModel('phase_4/models/modules/tt_m_ara_int_ropes.bam') 
            ropes.reparentTo(self.np) 
            ropes.setPos(109,68,2.5) 
            ropes.setScale(0.75) 
            gear = loader.loadModel("phase_9/models/char/gearProp.bam") 
            gear.reparentTo(self.np) 
            gear.setPos(109,68,11.5) 
            gear.hprInterval(15.0, Vec3(0, 360, 0), Vec3(-720, 0, -720)).loop()
            gear.setColorScale(0.6, 0.6, 1.0, 1.0)
            gear2 = loader.loadModel("phase_9/models/char/gearProp.bam") 
            gear2.reparentTo(self.np) 
            gear2.setScale(0.3)
            gear2.setPos(109,68,11.5) 
            gear2.hprInterval(15.0, Vec3(0, -720, 0), Vec3(360, 0, 360)).loop()
            gear2.setColorScale(0.6, 0.6, 1.0, 1.0)
        elif arg == 2:
            tree = loader.loadModel("phase_4/models/props/winter_tree_Christmas.bam")
            tree.reparentTo(self.np)
            tree.setPos(109,68,2.5)
        
    def setHolidayProps(self, holiday):
        if holiday == None:
            self.placetree_TT('prop_tree_fat_no_box_ur',(-100,5,2.5),1,1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(100,5,2.5),1,1)
            self.placetree_TT('prop_tree_large_no_box_ul',(-81,-73,0.2),1,1)
            self.placetree_TT('prop_tree_large_no_box_ul',(-48,-123,0.2),1,1)
            self.placetree_TT('prop_tree_large_no_box_ul',(21,-128,0.2),1,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(47,121,2.5),1,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(65,130,2.5),1,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(59,117,2.5),1,1)
            self.placetree_TT('prop_tree_small_ul',(144,120,3),50,1)
            self.placetree_TT('prop_tree_small_ul',(130,132,3),50,1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-77,121,2.5),1,1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-139,101,2.5),1,1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-59,113,2.5),1,1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-61,132,2.5),1,1)
            self.placelight_TT('prop_post_three_light',(72,-100,0.5),60,1)
            self.placelight_TT('prop_post_three_light',(42,-128,0.5),60,1)
            self.placelight_TT('prop_post_three_light',(88.5,45.3,3),0,1)
            self.placelight_TT('prop_post_three_light',(88.5,78.5,3),0,1)
            self.placelight_TT('prop_post_three_light',(-93,95,3),0,1)
            self.placelight_TT('prop_post_three_light',(-93,58.5,3),0,1)
            self.placelight_TT('prop_post_one_light',(23,105,4),0,1)
            self.placelight_TT('prop_post_one_light',(-23,105,4),0,1)
            self.placelight_TT('prop_post_one_light',(60,31,4),0,1)
            self.placelight_TT('prop_post_one_light',(-60,31,4),0,1)
            self.placelight_TT('prop_post_one_light',(-164,65,3),85.5,1)
            self.placelight_TT('prop_post_one_light',(-121,7,3),-25,1)
            self.placelight_TT('prop_post_sign',(-53,-132,0.5),60,1)
            self.decorationProps(1)
        elif holiday == "Christmas":
            self.placetree_TT('prop_tree_fat_no_box_ur',(-100,5,2.5),2,2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(100,5,2.5),2,2)
            self.placetree_TT('prop_tree_large_no_box_ul',(-81,-73,0.2),2,2)
            self.placetree_TT('prop_tree_large_no_box_ul',(-48,-123,0.2),2,2)
            self.placetree_TT('prop_tree_large_no_box_ul',(21,-128,0.2),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(47,121,2.5),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(65,130,2.5),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(59,117,2.5),2,2)
            self.placetree_TT('prop_tree_small_ul',(144,120,3),50,2)
            self.placetree_TT('prop_tree_small_ul',(130,132,3),50,2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-77,121,2.5),2,2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-139,101,2.5),1,2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-59,113,2.5),1,2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-61,132,2.5),1,2)
            self.placelight_TT('prop_post_three_light',(72,-100,0.5),60,2)
            self.placelight_TT('prop_post_three_light',(42,-128,0.5),60,2)
            self.placelight_TT('prop_post_three_light',(88.5,45.3,3),0,2)
            self.placelight_TT('prop_post_three_light',(88.5,78.5,3),0,2)
            self.placelight_TT('prop_post_three_light',(-93,95,3),0,2)
            self.placelight_TT('prop_post_three_light',(-93,58.5,3),0,2)
            self.placelight_TT('prop_post_one_light',(23,105,4),0,2)
            self.placelight_TT('prop_post_one_light',(-23,105,4),0,2)
            self.placelight_TT('prop_post_one_light',(60,31,4),0,2)
            self.placelight_TT('prop_post_one_light',(-60,31,4),0,2)
            self.placelight_TT('prop_post_one_light',(-164,65,3),85.5,2)
            self.placelight_TT('prop_post_one_light',(-121,7,3),-25,2)
            self.placelight_TT('prop_post_sign',(-53,-132,0.5),60,2)
            self.decorationProps(2)
 
    def randomSounds(self): random.choice(self.birds).play()
    
    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }

class Dock(Hood):
        
    def loadRing(self,ring): return loader.loadSfx("data/sounds/hoods/ddk/{0}".format(ring))
        
    def requestStormCheck(self):
         isStorm = random.randint(1,2)
         if self.zoneId == 2000:
             if int(isStorm) == 2:
                 self.sky1.hide()
                 self.sky2.show()
                 self.harborFog = Fog("Harbor Fog")
                 self.harborFog.setExpDensity(0.001)
                 self.np.setFog(self.harborFog)
             else:
                 self.sky1.show()
                 self.sky2.hide()
                 self.np.clearFog()
        else:
             self.check.finish()
        
    def makeSeq(self):
        self.moveBoat1 = self.boat.posHprInterval(6, (30.43079, -32.5, -4), (90,0,0))
        self.moveBoat2 = self.boat.posHprInterval(6, (-33.5692, -42.5, -4), (40,0,0))
        self.moveBoat3 = self.boat.posHprInterval(4, (-50, -10, -4), (0,0,0))
        self.moveBoat4 = self.boat.posHprInterval(6, (-50, 40, -4), (-50,0,0))
        self.moveBoat5 = self.boat.posHprInterval(6, (9.08847, 50.4189, -4), (-100,0,0))
        self.moveBoat6 = self.boat.posHprInterval(7, (50.1,25,-4), (-180,0,0))
        
        self.upEPier = self.EPier.hprInterval(4, (89.9995,-0,-0.000199231))
        self.downEPier = self.EPier.hprInterval(4, (89.9995,-44.2599,-0.000199231))
        self.upWPier = self.WPier.hprInterval(4, (-90.399,-0,-0.185446))
        self.downWPier = self.WPier.hprInterval(4, (-90.399,-47.5673,-0.185446))
        
        self.seq = Sequence(
                            Wait(14),
                            self.sfxInterval_bell,
                            Parallel(self.downEPier,
                                     self.sfxInterval_creack,
                                     self.moveBoat1),
                            self.moveBoat2,
                            Parallel(self.upWPier,
                                     self.sfxInterval_creack,
                                     self.moveBoat3),
                            Wait(14),
                            self.sfxInterval_bell,
                            Parallel(self.downWPier,
                                     self.sfxInterval_creack,
                                     self.moveBoat4),
                            self.moveBoat5,
                            Parallel(self.moveBoat6,
                                     self.sfxInterval_creack,
                                     self.upEPier),
                            )
 
        self.check = Sequence(Wait(45),Func(self.requestStormCheck)) ### eventual crash: AssertionError: !is_empty() at line 5385 of panda/src/pgraph/nodePath.cxx
        self.check.loop()

    def __init__(self,tp=None):
        self.music = "data/sounds/hoods/ddk/DD_nbrhood"
        self.name = "AREA_DDK"
        
        self.sfx_bell = self.loadRing('bell')
        self.sfx_creack = self.loadRing('creack')
        self.sfx_water = self.loadRing('water')
        
        self.sfxInterval_bell = SoundInterval(self.sfx_bell,loop=0)
        self.sfxInterval_creack = SoundInterval(self.sfx_creack,loop=0)
        self.sfxInterval_water = SoundInterval(self.sfx_water,loop=0)
 
        self.zoneId = 2000
        newModel = loader.loadModel
        
        self.av_startpos = (
                            ((-116.69, -34.2716, -0.245013),(-179.758, 0, 0)),
                            ((-92.9745, -38.4801, -0.00904583),(-72.1942, 0, 0)),
                            ((-59.2309, -43.7733, -0.00904993),(-117.784, 0, 0)),
                            ((18.9871, -15.2758, -0.00811336),(-211.235, 0, 0)),
                            ((-22.0924, -103.422, -0.00839086),(-242.26, 0, 0)),
                            ((-59.7771, -190.784, 2.40302),(-331.3, 0, 0)),
                            ((-167.607, -191.644, 2.37616),(-388.684, 0, 0)),
                            ((-200.292, -119.822, 2.4041),(-427.432, 0, 0)),
                            ((-165.27, -53.3781, 2.40303),(-487.091, 0, 0)),
                            ((-109.571, -118.602, 2.47348),(-480.476, 0, 0)),
                            )
        Hood.__init__(self,"phase_6/models/neighborhoods/donalds_dock.bam")
 
        self.sky1 = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.sky1.reparentTo(self.np)
        self.sky2 = loader.loadModel("phase_3.5/models/props/BR_sky.bam")
        self.sky2.reparentTo(self.np)
        self.sky2.hide()

        self.environ.setPos(-25,10,0)
        self.environ.setHpr(180,0,0)
        self.environ.reparentTo(self.np)
        self.boat = self.environ.find("**/donalds_boat")
        self.boat.setPos(50.1,25,-4)
        self.boat.setHpr(180,0,0)
        self.boat.find('**/wheel').hide()
        self.EPier = self.environ.find("**/east_pier")
        self.EPier.setHpr(89.9995,-0,-0.000199231)
        self.WPier = self.environ.find("**/west_pier")
 
        self.donald = Actor("phase_6/models/char/donald-wheel-1000.bam",{"wait":"phase_6/models/char/donald-wheel-wheel.bam"}) 
        self.donald.reparentTo(self.boat) 
        self.donald.loop("wait") 
        self.donald.setPos(0,-0.3,5)
        fonto = loader.loadFont("phase_3/models/fonts/MickeyFont.bam")
        frame = DirectFrame(frameColor=(0,0,0,0),parent=self.donald)
        frame.setY(-.2)
        self.text = OnscreenText(text="Donald",font=fonto,pos=(0,3.5,0),scale=1,parent=frame,fg=(1,1,0.7,1),wordwrap=9)
        self.text.setBillboardAxis(1)

        self.trolley = self.placebldg("phase_6/models/modules/trolley_station_DD.bam", (-25,-90,5.67), 180)
        
        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))
        
        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley
        
        signTr = self.trolley.find("**/sign_origin")
        self.baseline(signTr,'MickeyFont.bam',(0.701961,0,0,1),(0.5,0,1.33),(2,2.5,1.4),'Games',7)
        self.baseline(signTr,'MickeyFont.bam',(1,0.737255,0.501961,1),(0.5,-2,-2.33),(2.4,2.3,1.4),'Trolley',7)
        
        self.ttcTunnel = self.placetun((-198.22,-108.72,-0.975), -34, False)
        self.sign1 = loader.loadModel("phase_4/models/props/tunnel_sign_red.bam")
        self.sign1.reparentTo(self.ttcTunnel.find("**/sign_origin"))
        self.sign1.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon1 = loader.loadModel("phase_4/models/props/donaldSZ.bam")
        self.icon1.reparentTo(self.sign1.find("**/g1"))
        self.icon1.setPos(0,-.1,1.6)
        self.icon1.setScale(1.9)
        self.baseline(self.sign1,'MickeyFont.bam',(0.501961,0,0.155,1),(0,-0.2,0),(1.2,0.9,.9),"Barnacle Boulevard Donut's Dock",10)
        Tunnel(self.ttcTunnel, BitMask32(8), self, (TTCentral,'AREA_TTC'))
        
        self.mmlTunnel = self.placetun((164.82,-51.14,-0.975), 90, True, "DD")
        self.sign2 = loader.loadModel("phase_4/models/props/tunnel_sign_red.bam")
        self.sign2.reparentTo(self.mmlTunnel.find("**/sign_origin"))
        self.sign2.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon2 = loader.loadModel("phase_4/models/props/donaldSZ.bam")
        self.icon2.reparentTo(self.sign2.find("**/g1"))
        self.icon2.setPos(0,-.1,1.6)
        self.icon2.setScale(1.9)
        self.baseline(self.sign2,'MickeyFont.bam',(0.501961,0,0.155,1),(0,-0.87,0),(1.1,1,.9),"Lighthouse Lane Donut Docks",12)
 
        self.dgTunnel = self.placetun((-214.99,74.98,-0.975), -90, True, "DD")
        self.sign3 = loader.loadModel("phase_4/models/props/tunnel_sign_red.bam")
        self.sign3.reparentTo(self.dgTunnel.find("**/sign_origin"))
        self.sign3.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon3 = loader.loadModel("phase_4/models/props/donaldSZ.bam")
        self.icon3.reparentTo(self.sign3.find("**/g1"))
        self.icon3.setPos(0,-.1,1.6)
        self.icon3.setScale(1.9)
        self.baseline(self.sign3,'MickeyFont.bam',(0.501961,0,0.155,1),(0,-0.87,0),(1.1,1,.9),"Seaweed Street Donut Docks",12)

        self.clothshop = self.placebldg("phase_6/models/modules/clothshopDD.bam",(-88.0457,115.078,3.25565),45)
        self.baseline(self.clothshop.find("**/sign_origin"),'MickeyFont.bam',(0.701961,0,0,1),(0,-0.5,0),(1.7,1.6,1.7),L10N('PROP_CLOTHSTORE'),12)
        self.door('practical','door_double_clothshop',(0.91,0.34,0.34,1),self.clothshop)
        
        self.tunnelAA = self.placebldg("phase_6/models/golf/outdoor_zone_entrance.bam", (-53.1974,172.046,3.27967),52.125)
        
        from streets import ConiferousCreek
        Tunnel(self.tunnelAA,BitMask32(8),self,(ConiferousCreek,'STREET_ACRES_CC'))
        
        self.sign('DD',self.tunnelAA,'DD_sign2',(0,0,0),(0,0,0),(2,1,1.4))
        self.baseline(self.tunnelAA.find("**/sign_origin"),'Comedy.bam',(0.439216,0.247059,0.184314,1),(0,0,0),(2.5,1.5,5.7),"Coniferous Creek Acorn Acres",10)

        self.gs = self.placebldg("phase_6/models/modules/gagShop_DD.bam",(-121.761,-24.113,5.66699),-90)
        self.door('practical','door_double_square_ur',(1.000,0.737,0.302,1),self.gs)

        self.hq = self.placebldg("phase_6/models/modules/tt_m_ara_dod_SZ_hq.bam",(-10.4986,104.147,1.66701),-90)

        self.pier1 = newModel("phase_4/models/props/piers_tt.bam")
        self.pier1.reparentTo(self.np)
        self.pier1.setPos(-1.79822,139.984,3.59855)
        self.pier1.setHpr(135,0,0)
        self.pier2 = newModel("phase_4/models/props/piers_tt.bam")
        self.pier2.reparentTo(self.np)
        self.pier2.setPos(-11.6229,148.498,3.64751)
        self.pier2.setHpr(165,0,0)
        self.pier3 = newModel("phase_4/models/props/piers_tt.bam")
        self.pier3.reparentTo(self.np)
        self.pier3.setPos(-23.6427,149.15,3.59725)
        self.pier3.setHpr(-165,0,0)
        self.pier4 = newModel("phase_4/models/props/piers_tt.bam")
        self.pier4.reparentTo(self.np)
        self.pier4.setPos(-31.3754,141.368,3.56653)
        self.pier4.setHpr(-135,0,0)

        self.ps = self.placebldg("phase_6/models/modules/PetShopExterior_DD.bam", (40.2718,-89.8663,3.28834),-165)
        self.fish = Actor("phase_4/models/props/SZ_fish-mod.bam",{"swim":"phase_4/models/props/SZ_fish-swim.bam"})
        self.fish.reparentTo(self.ps)
        self.fish.loop('swim')
        self.door('practical','door_double_square_ur',(0.86,0.48,0.23,1),self.ps)        
        self.baseline(self.ps.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(0,0.180612,0),(1.51565,1.4,3.00508),L10N('PROP_PETSHOP'),12)

        self.gate = self.placebldg("phase_6/models/modules/partyGate_DD.bam", (36.9924,113.67,3.28138), 315)

        #Extras
        self.placelight_DD((-103.41,40.92,5.69),-180,'streetlight_DD_left')
        self.placelight_DD((-106.95,-41.49,5.67),-165,'streetlight_DD_left')
        self.placelight_DD((-60.98,-71.34,5.73),-120,'streetlight_DD_left')
        self.placelight_DD((2.52,-74.03,5.67),-135,'streetlight_DD_left')
        self.placelight_DD((58.21,-37.67,5.68),45,'streetlight_DD_left')
        self.placelight_DD((57.15,57.28,5.71),-45,'streetlight_DD_left')
        self.ch3 = newModel("phase_6/models/props/DD_flats.bam").find("**/prop_nets")
        self.ch3.reparentTo(self.np)
        self.ch3.setPos(-122.68,-38.45,5.57)
        self.ch3.setHpr(60,2,0)
        self.ch3.setScale(0.7)
        self.ch4 = newModel("phase_5/models/props/crate.bam")
        self.ch4.reparentTo(self.np)
        self.ch4.setPos(-108.75,44.58,5.7)
        self.ch4.setHpr(45,0,0)
        self.ch5 = newModel("phase_5/models/props/crate.bam")
        self.ch5.reparentTo(self.np)
        self.ch5.setPos(-108.87,41.47,5.7)
        self.ch5.setHpr(105,0,0)
        self.ch6 = newModel("phase_5/models/props/crate.bam")
        self.ch6.reparentTo(self.np)
        self.ch6.setPos(1.33,-75.44,5.71)
        self.ch6.setHpr(105,0,0)
        self.ch6 = newModel("phase_5/models/props/crate.bam")
        self.ch6.reparentTo(self.np)
        self.ch6.setPos(-1.26,-72.98,5.8)
        self.ch6.setHpr(60,0,0)
        self.ch7 = newModel("phase_5/models/props/crate.bam")
        self.ch7.reparentTo(self.np)
        self.ch7.setPos(-71.17,-77.38,5.65)
        self.ch7.setHpr(90,0,0)
        self.ch8 = newModel("phase_5/models/props/crate.bam")
        self.ch8.reparentTo(self.np)
        self.ch8.setPos(-74.57,-74.96,5.69)
        self.ch8.setHpr(45,0,0)
        self.ch9 = newModel("phase_6/models/props/DD_flats.bam").find("**/prop_ship_wheel")
        self.ch9.reparentTo(self.np)
        self.ch9.setPos(-79.04,-78.04,5.67)
        self.ch9.setHpr(90,0,0)
        self.ch9.setScale(0.5)
        self.ch10 = newModel("phase_5/models/props/crate.bam")
        self.ch10.reparentTo(self.np)
        self.ch10.setPos(61.03,55.59,5.65)
        self.ch10.setHpr(-75,0,0)
        self.ch11 = newModel("phase_5/models/props/crate.bam")
        self.ch11.reparentTo(self.np)
        self.ch11.setPos(58.24,51.29,5.7)
        self.ch11.setHpr(-120,0,0)
        self.ch12 = newModel("phase_5/models/props/crate.bam")
        self.ch12.reparentTo(self.np)
        self.ch12.setPos(-71.02,-69.91,5.67)
        self.ch12.setHpr(-90,0,0)
        self.ch13 = newModel("phase_5/models/props/chimneys.bam").find("**/prop_chimney")
        self.ch13.reparentTo(self.np)
        self.ch13.setPos(77.77,44.8,23.71)
        self.ch13.setHpr(-90,0,0)
        self.ch13.setColor(0.63,0.47,0.24,1)
        self.ch14 = newModel("phase_5/models/props/chimneys.bam").find("**/prop_chimney")
        self.ch14.reparentTo(self.np)
        self.ch14.setPos(-6,-94,25)
        self.ch14.setHpr(180,0,0)
        self.ch14.setColor(0.63,0.47,0.24,1)
        self.ch15 = newModel("phase_3.5/models/props/neighborhood_sign_TT.bam")
        self.ch15.reparentTo(self.np)
        self.ch15.setPos(-82.34,-70.8,5.67)
        self.ch15.setHpr(146,0,0)
        self.ch15.setScale(1.5)
        self.ch16 = newModel("phase_3.5/models/props/neighborhood_sign_TT.bam")
        self.ch16.reparentTo(self.np)
        self.ch16.setPos(-107.27,-53.79,5.67)
        self.ch16.setHpr(-35,0,0)
        self.ch16.setScale(1.5)
        self.ch17 = newModel("phase_4/models/props/neighborhood_sign_DG.bam")
        self.ch17.reparentTo(self.np)
        self.ch17.setPos(-118.81,-0.75,5.67)
        self.ch17.setHpr(89,0,0)
        self.ch17.setScale(1.5)
        self.ch18 = newModel("phase_4/models/props/neighborhood_sign_DG.bam")
        self.ch18.reparentTo(self.np)
        self.ch18.setPos(-118.86,30.91,5.67)
        self.ch18.setHpr(-90,0,0)
        self.ch18.setScale(1.5)
        self.ch19 = newModel("phase_4/models/props/neighborhood_sign_BR.bam")
        self.ch19.reparentTo(self.np)
        self.ch19.setPos(69.03,24.96,5.67)
        self.ch19.setHpr(-90,0,0)
        self.ch19.setScale(1.5)
        self.ch20 = newModel("phase_4/models/props/neighborhood_sign_BR.bam")
        self.ch20.reparentTo(self.np)
        self.ch20.setPos(68.83,-6.93,5.67)
        self.ch20.setHpr(90,0,0)
        self.ch20.setScale(1.5)
        self.ch21 = newModel("phase_6/models/props/palm_tree_topflat.bam")
        self.ch21.reparentTo(self.np)
        self.ch21.setPos(-55,115,3.25331)
        self.ch21.setHpr(0,0,0)
        self.ch21.setScale(1.3)
        self.ch22 = newModel("phase_6/models/props/palm_tree_topflat.bam")
        self.ch22.reparentTo(self.np)
        self.ch22.setPos(-59.7445,135.255,3.30638)
        self.ch22.setHpr(135,0,0)
        self.ch22.setScale(0.7)
        self.ch23 = newModel("phase_6/models/props/palm_tree_topflat.bam")
        self.ch23.reparentTo(self.np)
        self.ch23.setPos(-100,85,3.2338)
        self.ch23.setHpr(-75,0,0)
        self.ch23.setScale(1.1)
        self.ch24 = newModel("phase_6/models/props/palm_tree_topflat.bam")
        self.ch24.reparentTo(self.np)
        self.ch24.setPos(64.4875,91.0424,3.25886)
        self.ch24.setHpr(285,0,0)
        self.ch24.setScale(1.1)
        self.ch25 = newModel("phase_6/models/props/palm_tree_topflat.bam")
        self.ch25.reparentTo(self.np)
        self.ch25.setPos(59.0938,-64.9951,3.29744)
        self.ch25.setHpr(-159,0,0)
        self.ch25.setScale(1.5304)
        self.ch26 = newModel("phase_6/models/props/palm_tree_topflat.bam")
        self.ch26.reparentTo(self.np)
        self.ch26.setPos(51.4007,-72.6317,3.29744)
        self.ch26.setHpr(-18,0,0)
        self.ch26.setScale(0.8)
        self.ch27 = newModel("phase_6/models/props/palm_tree_topflat.bam")
        self.ch27.reparentTo(self.np)
        self.ch27.setPos(19.2,-83.3846,3.29744)
        self.ch27.setHpr(91,0,0)
        self.ch27.setScale(1.3)
        self.ch28 = newModel("phase_6/models/props/palm_tree_topflat.bam")
        self.ch28.reparentTo(self.np)
        self.ch28.setPos(-10.8767,181.675,3.23742)
        self.ch28.setHpr(-120,0,0)
        self.ch28.setScale(1.40798)
        self.ch29 = newModel("phase_6/models/props/palm_tree_topflat.bam")
        self.ch29.reparentTo(self.np)
        self.ch29.setPos(-15,180,3.23697)
        self.ch29.setHpr(45,0,0)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch30 = self.chw.find("**/wall_md_blank_ur")
        self.ch30.reparentTo(self.np)
        self.ch30.setColor(0.42,0.16,0.16,1)
        self.ch30.setPos(-122.3,34.38,5.67)
        self.ch30.setHpr(79,0,0)
        self.ch30.setSx(15)
        self.ch30.setSz(20)
        self.makeMask(self.chw,self.ch30)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch31 = self.chw.find("**/wall_md_blank_ur")
        self.ch31.reparentTo(self.np)
        self.ch31.setColor(0.38,0.3,0.18,1)
        self.ch31.setPos(-124.96,-49.96,5.67)
        self.ch31.setHpr(90,0,0)
        self.ch31.setSx(15.6)
        self.ch31.setSz(20)
        self.makeMask(self.chw,self.ch31)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch32 = self.chw.find("**/wall_md_board_ur")
        self.ch32.reparentTo(self.np)
        self.ch32.setColor(0.71,0.49,0.35,1)
        self.ch32.setPos(-112.88,-57.6,5.67)
        self.ch32.setHpr(147,0,0)
        self.ch32.setSx(15)
        self.ch32.setSz(20)
        self.makeMask(self.chw,self.ch32)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch33 = self.chw.find("**/wall_md_blank_ur")
        self.ch33.reparentTo(self.np)
        self.ch33.setColor(0.42,0.16,0.16,1)
        self.ch33.setPos(-64.61,-90.2,5.67)
        self.ch33.setHpr(146,0,0)
        self.ch33.setSx(20.7)
        self.ch33.setSz(20.3)
        self.makeMask(self.chw,self.ch33)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch34 = self.chw.find("**/wall_lg_brick_ur")
        self.ch34.reparentTo(self.np)
        self.ch34.setColor(0.17,0.44,0.28,1)
        self.ch34.setPos(-55,-90,5.67)
        self.ch34.setHpr(-180,0,0)
        self.ch34.setSx(10)
        self.ch34.setSz(20.3)
        self.makeMask(self.chw,self.ch34)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch35 = self.chw.find("**/wall_md_blank_ur")
        self.ch35.reparentTo(self.np)
        self.ch35.setColor(0.42,0.16,0.16,1)
        self.ch35.setPos(5.6,-99.86,5.67)
        self.ch35.setHpr(90,0,0)
        self.ch35.setSx(10)
        self.ch35.setSz(20.3)
        self.makeMask(self.chw,self.ch35)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch36 = self.chw.find("**/wall_md_blank_ur")
        self.ch36.reparentTo(self.np)
        self.ch36.setColor(0.42,0.16,0.16,1)
        self.ch36.setPos(5.6,-90,5.67)
        self.ch36.setHpr(-180,0,0)
        self.ch36.setSx(15.6)
        self.ch36.setSz(20.3)
        self.makeMask(self.chw,self.ch36)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch37 = self.chw.find("**/wall_sm_wood_ur")
        self.ch37.reparentTo(self.np)
        self.ch37.setColor(0.874016,0.610097,0.610097,1)
        self.ch37.setPos(75,60,5.67)
        self.ch37.setHpr(-90,0,0)
        self.ch37.setSx(15)
        self.ch37.setSz(20.3)
        self.makeMask(self.chw,self.ch37)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch38 = self.chw.find("**/wall_sm_wood_ur")
        self.ch38.reparentTo(self.np)
        self.ch38.setColor(0.75,0.75,0.75,1)
        self.ch38.setPos(75,45,5.67)
        self.ch38.setHpr(-90,0,0)
        self.ch38.setSx(20)
        self.ch38.setSz(20.3)
        self.makeMask(self.chw,self.ch38)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch39 = self.chw.find("**/wall_md_board_ur")
        self.ch39.reparentTo(self.np)
        self.ch39.setColor(0.93,0.15,0.15,1)
        self.ch39.setPos(75,-10,5.67)
        self.ch39.setHpr(-90,0,0)
        self.ch39.setSx(15)
        self.ch39.setSz(20.3)
        self.makeMask(self.chw,self.ch39)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch40 = self.chw.find("**/wall_md_blank_ur")
        self.ch40.reparentTo(self.np)
        self.ch40.setColor(0.38,0.31,0.19,1)
        self.ch40.setPos(75,-25,5.67)
        self.ch40.setHpr(-90,0,0)
        self.ch40.setSx(15)
        self.ch40.setSz(20.5)
        self.makeMask(self.chw,self.ch40)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch41 = self.chw.find("**/wall_md_blank_dr")
        self.ch41.reparentTo(self.np)
        self.ch41.setColor(0.384314,0.305635,0.187618,1)
        self.ch41.setPos(-124,-14.56,5.67)
        self.ch41.setHpr(90,0,0)
        self.ch41.setSx(10)
        self.ch41.setSz(20.3)
        self.makeMask(self.chw,self.ch41)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch42 = self.chw.find("**/wall_sm_wood_ur")
        self.ch42.reparentTo(self.np)
        self.ch42.setColor(0.874016,0.610097,0.610097,1)
        self.ch42.setPos(90,60,5.67)
        self.ch42.setHpr(180,0,0)
        self.ch42.setSx(15)
        self.ch42.setSz(20.3)
        self.makeMask(self.chw,self.ch42)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch43 = self.chw.find("**/wall_md_blank_ur")
        self.ch43.reparentTo(self.np)
        self.ch43.setColor(0.42,0.16,0.16,1)
        self.ch43.setPos(-119.44,49.1,5.67)
        self.ch43.setHpr(165,0,0)
        self.ch43.setSx(15)
        self.ch43.setSz(20.3)
        self.makeMask(self.chw,self.ch43)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch44 = self.chw.find("**/wall_lg_brick_ur")
        self.ch44.reparentTo(self.np)
        self.ch44.setColor(0.17,0.44,0.28,1)
        self.ch44.setPos(-10,-90,5.67)
        self.ch44.setHpr(-180,0,0)
        self.ch44.setSx(15)
        self.ch44.setSz(20.3)
        self.makeMask(self.chw,self.ch44)
        self.chw = newModel("phase_3.5/models/modules/walls.bam")
        self.ch45 = self.chw.find("**/wall_md_blank_ur")
        self.ch45.reparentTo(self.np)
        self.ch45.setColor(0.38,0.31,0.19,1)
        self.ch45.setPos(75,-40,5.67)
        self.ch45.setHpr(0,0,0)
        self.ch45.setSx(15)
        self.ch45.setSz(20)
        self.makeMask(self.chw,self.ch45)
        
        self.makeSeq()
        
        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
