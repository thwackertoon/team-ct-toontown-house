from __init__ import Area, Tunnel

from panda3d.core import *
from tth.avatar.toon import EToon, rgb2p
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.actor.Actor import *
import random
from tth.fishing.FishingHandler import *

from tth.effects.FireworkShow import *

import streets
       
class Hood(Area):

    PREFIX2PHASE = {
                    'TT':'4',
                    'TTC':'4',
                    
                    'DD':'6',
                    'DG':'8',
                    'MM':'6',
                    'BR':'8',
                    'DL':'8',
                    }
                    
    def __init__(self,*a,**kw):
        Area.__init__(self,*a,**kw)
        self.haveFires = False
                    
    def startFires(self):
        self.haveFires = True
        color = LerpColorInterval(self.sky,3,Vec4(0,0,0,1))
        color.start()
        self.startFireworks()
		
    #doors
    def door(self,doors,type,color,parent):
        door = loader.loadModel("phase_3.5/models/modules/doors_{0}.bam".format(doors)).find('**/'+type)
        door.reparentTo(parent)
        door.setColor(color)
        
    def restartSky2Theme(self):
        self.haveFires = False
        self.sky.setColor(255,255,255)
        self.newtheme.stop()
        self.theme.play()
       
    def startFireworks(self):
        self.theme.stop()
        self.newtheme = loader.loadMusic("data/sounds/fireworks.mp3")
        self.newtheme.play()
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
        seq.start() #why this t .-.

    def firework(self,pos):
        FireworkShow(pos)
                    
    def enterTrolley(self,entry):
        try:
            assert not base.isCompiled
            self.trolleyMgr.d_requestBoard(self.toon.doId)
        except:
            pass
        
    def baseline(self,parent,font,color,pos,scale,textx,ww):
        fonto = loader.loadFont("phase_3/models/fonts/{0}".format(font))
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
        
    def addCollisionSphere(self,pos,scale):
        CS = self.np.attachNewNode(CollisionNode('colNode'))
        CS.node().addSolid(CollisionSphere(pos,scale))
    
class TTCentral(Hood):
    name = "AREA_TTC"
    zoneId = 1000
    music = "phase_4/audio/bgm/TC_nbrhood.mid"
    
    def __init__(self,tp=None):
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
        #self.startFires()
        
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
        
        self.tunnel1 = self.placetun((-56.6, -238, -6.3), 360, False)
        self.sign1 = loader.loadModel("phase_3.5/models/props/tunnel_sign_orange.bam")
        self.sign1.reparentTo(self.tunnel1.find("**/sign_origin"))
        self.sign1.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon1 = loader.loadModel("phase_3.5/models/props/mickeySZ.bam")
        self.icon1.reparentTo(self.sign1.find("**/g1"))
        self.icon1.setPos(0,-.1,1.6)
        self.icon1.setScale(1.9)
        self.baseline(self.sign1,'MickeyFont.bam',(0,0.501961,0,1),(0,-1,0),(.9,.8,.9),"Loopy Lane Toontown Central",12)

        self.tunnel2 = self.placetun((209,-65,-3.7), 420, False)
        self.sign2 = loader.loadModel("phase_3.5/models/props/tunnel_sign_orange.bam")
        self.sign2.reparentTo(self.tunnel2.find("**/sign_origin"))
        self.sign2.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon2 = loader.loadModel("phase_3.5/models/props/mickeySZ.bam")
        self.icon2.reparentTo(self.sign2.find("**/g1"))
        self.icon2.setPos(0,-.1,1.6)
        self.icon2.setScale(1.9)
        self.baseline(self.sign2,'MickeyFont.bam',(0,0.501961,0,1),(0,-1,0),(.9,.8,.9),"Silly Street Toontown Central",12)

        self.tunnel3 = self.placetun((-176,32,-6.3), 261, False)
        self.sign3 = loader.loadModel("phase_3.5/models/props/tunnel_sign_orange.bam")
        self.sign3.reparentTo(self.tunnel3.find("**/sign_origin"))
        self.sign3.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon3 = loader.loadModel("phase_3.5/models/props/mickeySZ.bam")
        self.icon3.reparentTo(self.sign3.find("**/g1"))
        self.icon3.setPos(0,-.1,1.6)
        self.icon3.setScale(1.9)
        self.baseline(self.sign3,'MickeyFont.bam',(0,0.501961,0,1),(0,-1,0),(.9,.8,.9),"Punchline Place Toontown Central",14)

        self.speedway = self.placebldg("phase_4/models/modules/Speedway_Tunnel.bam", (-172,22,3), 305)
       
        self.baseline(self.speedway.find("**/sign_origin"),'MickeyFont.bam',(0.00392157,0.403922,0.803922,1),(2.07014,0.591417,0),(2.67969,1,2.12201),L10N('AREA_SPEEDWAY'),7)

        self.trolley = self.placebldg("phase_4/models/modules/trolley_station_TT.bam", (83,-118,0.4), 218.5)
        
        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))
        
        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley
        
        self.baseline(self.trolley.find("**/sign_origin"),'MickeyFont.bam',(0.992157,0.968627,0.00784314,1),(0.5,0,1.33),(1.4,1,1.4),L10N('PROP_TROLLEY'),7)

        self.building1 = Actor("phase_5/models/char/tt_r_ara_ttc_B2.bam",{"dance":"phase_5/models/char/tt_a_ara_ttc_B2_dance.bam"})
        #anim doesnt exist
        self.building1.reparentTo(self.np)
        self.building1.loop("dance")
        self.building1.setPos(37,-143,0)
        self.building1.setH(553)
        #self.sign('all',self.building1,'TTC_sign2',(-0.35,0,0.3),(0,0,0),(0.9,1,0.9))
        #self.baseline(self.building1.find("**/sign_origin"),'MickeyFont.bam',(1,0.501961,0,1),(0,1,0),(1.5,1,1.8),"Loony Labs",7)
 
        self.library = self.placebldg("phase_4/models/modules/library.bam", (45.9,93,4), 270)
        #self.door('practical','door_double_round_ur',(0.88,0.45,0.38,1),self.library,'library_door_origin')
        self.libraryName = "Library"

        self.bank = self.placebldg("phase_4/models/modules/bank.bam", (-36.1796,58.6656,4), -270)
        #self.door('practical','door_double_round_ur',(0.88,0.45,0.38,1),self.bank,'bank_door_origin')
        self.baseline(self.bank.find("**/sign_origin"),'MickeyFont.bam',(1,0.662745,0.32549,1),(0,-1.58,0),(2.9,1,3.4),L10N('PROP_BANK'),7)

        self.schoolHouse = self.placebldg("phase_4/models/modules/school_house.bam", (-66,-126,0), 135)
        #self.door('practical','door_double_square_ur',(0.88,0.45,0.38,1),self.schoolHouse,'bank_door_origin')
        self.sign('TTC',self.schoolHouse,'TTC_sign3',(-0.35,0,0.3),(0,0,0),(0.9,1,0.9))
        self.baseline(self.schoolHouse.find("**/sign_origin"),'MickeyFont.bam',(1,0.501961,0,1),(0,1,0),(1.5,1,1.8),L10N('PROP_SCHOOLHOUSE'),7)
 
        self.clothshop = self.placebldg("phase_4/models/modules/clothshopTT.bam", (-118,125,2), 25)
        self.baseline(self.clothshop.find("**/sign_origin"),'MickeyFont.bam',(1,0.611765,0.423529,1),(0,-0.5,0),(1.7,1,1.7),L10N('PROP_CLOTHSTORE'),9)

        self.hall = self.placebldg("phase_4/models/modules/toonhall.bam", (-22.1796,119.6656,4.03), -360)
        #self.door('practical','door_double_round_ur',(0.88,0.45,0.38,1),self.hall,'toonhall_door_origin')
        self.baseline(self.hall.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(0.3,0,-1.4),(2.2,1,2.3),L10N('PROP_HALL'),5)

        self.placebldg("phase_4/models/modules/gazebo.bam", (10.8,-59.9,-2), -268)

        #These need new positions.
        #self.signDG = loader.loadModel("data/models/TTC/neighborhood_sign_DG.bam")
        #self.signDG.reparentTo(self.np)
        #self.signDG.setPos(21.3941,-144.665,2.99998)
        #self.signDG.setHpr(-35,0,0)
        #self.signDG1 = loader.loadModel("data/models/TTC/neighborhood_sign_DG.bam")
        #self.signDG1.reparentTo(self.np)
        #self.signDG1.setPos(44.1038,-157.906,2.99998)
        #self.signDG1.setHpr(148,0,0)

        #self.signMM = loader.loadModel("data/models/TTC/neighborhood_sign_MM.bam")
        #self.signMM.reparentTo(self.np)
        #self.signMM.setPos(-143.503,-8.9528,0.499987)
        #self.signMM.setHpr(90,0,0)
        #self.signMM1 = loader.loadModel("data/models/TTC/neighborhood_sign_MM.bam")
        #self.signMM1.reparentTo(self.np)
        #self.signMM1.setPos(-143.242,16.9541,0.499977)
        #self.signMM1.setHpr(-90,0,0)

        #self.signDD = loader.loadModel("data/models/TTC/neighborhood_sign_DD.bam")
        #self.signDD.reparentTo(self.np)
        #self.signDD.setPos(-59.1768,92.9836,0.499824)
        #self.signDD.setHpr(-9,0,0)
        #self.signDD1 = loader.loadModel("data/models/TTC/neighborhood_sign_DD.bam")
        #self.signDD1.reparentTo(self.np)
        #self.signDD1.setPos(-33.749,88.9499,0.499825)
        #self.signDD1.setHpr(170,0,0)

        self.placebldg("phase_3.5/models/props/big_planter.bam", (-50,21,5), 0)
        self.placebldg("phase_3.5/models/props/big_planter.bam", (50,21,5), 0)
        self.placebldg("phase_4/models/props/toontown_central_fountain.bam", (3,63,4), 0)
        self.placebldg("phase_4/models/props/mickey_on_horse.bam", (-121,77,2), 0)

        self.gagShop = self.placebldg("phase_4/models/modules/gagShop_TT.bam", (93,-89,0.4), 800)
        #self.door('practical','door_double_square_ur',(1,0.63,0.38,1),self.gagShop,'door_origin')

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
        #self.door('practical','door_double_round_ur',(1,0.87,0.38,1),self.pet,'door_origin')
        self.baseline(self.pet.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(-0.0715486,0.575594,0),(1.58014,1,2.42354),L10N("PROP_PETSHOP"),9)
        
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
        
        from funAreas import Speedway
        self._tunnelMovie((
		                    #(self.model,"Name of the hood/area",funcname)
                            (self.tunnel3,"AREA_ST_2300",streets.TTC_2300),
                            (self.tunnel1,"AREA_ST_2200",streets.TTC_2200),
                            (self.tunnel2,"AREA_ST_2100",streets.TTC_2100),
                            (self.speedway,"AREA_SPEEDWAY",Speedway)
                            ),tp.getTunnel())
 
        self.setHolidayProps("Christmas")
        
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
            self.placetree_TT('prop_tree_fat_no_box_ur',(-100,5,2.5),1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(100,5,2.5),1)
            self.placetree_TT('prop_tree_large_no_box_ul',(-81,-73,0.2),1)
            self.placetree_TT('prop_tree_large_no_box_ul',(-48,-123,0.2),1)
            self.placetree_TT('prop_tree_large_no_box_ul',(21,-128,0.2),1)
            self.placetree_TT('prop_tree_small_no_box_ul',(47,121,2.5),1)
            self.placetree_TT('prop_tree_small_no_box_ul',(65,130,2.5),1)
            self.placetree_TT('prop_tree_small_no_box_ul',(59,117,2.5),1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-77,121,2.5),1)
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
            self.placelight_TT('prop_post_sign',(-53,-132,0.5),60,1)
            self.decorationProps(1)
        elif holiday == "Christmas":
            self.placetree_TT('prop_tree_fat_no_box_ur',(-100,5,2.5),2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(100,5,2.5),2)
            self.placetree_TT('prop_tree_large_no_box_ul',(-81,-73,0.2),2)
            self.placetree_TT('prop_tree_large_no_box_ul',(-48,-123,0.2),2)
            self.placetree_TT('prop_tree_large_no_box_ul',(21,-128,0.2),2)
            self.placetree_TT('prop_tree_small_no_box_ul',(47,121,2.5),2)
            self.placetree_TT('prop_tree_small_no_box_ul',(65,130,2.5),2)
            self.placetree_TT('prop_tree_small_no_box_ul',(59,117,2.5),2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-77,121,2.5),2)
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
    zoneId = 2000
    music = "phase_6/audio/bgm/DD_nbrhood.mid"
    name = "AREA_DDK"
    
    def loadRing(self,ring): return loader.loadSfx("phase_6/audio/sfx/SZ_DD_{0}.mp3".format(ring))
        
    def requestStormCheck(self):
         isStorm = random.randint(1,4)
         if int(isStorm) == 4:
             self.sky1.hide()
             self.sky2.show()
             self.harborFog = Fog("Harbor Fog")
             self.harborFog.setExpDensity(0.001)
             self.np.setFog(self.harborFog)
         else:
             self.sky1.show()
             self.sky2.hide()
             self.np.clearFog()
        
    def makeSeq(self):
        self.moveBoat1 = self.boat.posInterval(4, (50.1,25,-4))
        self.moveBoat2 = self.boat.hprInterval(4, (120,0,0))
        self.moveBoat3 = self.boat.posHprInterval(4, (8.43079, -26.5, -4), (90,0,0))
        self.moveBoat4 = self.boat.posHprInterval(4, (-33.5692, -26.5, -4), (0,0,0))
        self.moveBoat5 = self.boat.posHprInterval(4, (-50, -10, -4), (0,0,0))
        self.moveBoat6 = self.boat.posHprInterval(4, (-50, 40, -4), (-80,0,0))
        self.moveBoat7 = self.boat.posHprInterval(4, (9.08847, 50.4189, -4), (-80,0,0))
        self.moveBoat8 = self.boat.posHprInterval(4, (60, 25, -4), (-180,0,0))
        
        self.upEPier = self.EPier.hprInterval(4, (89.9995,-0,-0.000199231))
        self.downEPier = self.EPier.hprInterval(4, (89.9995,-44.2599,-0.000199231))
        self.upWPier = self.WPier.hprInterval(4, (-90.399,-0,-0.185446))
        self.downWPier = self.WPier.hprInterval(4, (-90.399,-47.5673,-0.185446))
        
        self.seq = Sequence(
                            self.sfxInterval_bell,
                            Parallel(
                                self.sfxInterval_creack,
                                self.upEPier),
                            Wait(8),
                            self.sfxInterval_creack,
                            self.downEPier,
                            self.moveBoat1,
                            self.moveBoat2,
                            self.moveBoat3,
                            self.moveBoat4,
                            Parallel(self.upWPier,
                                     self.sfxInterval_water,
                                     self.sfxInterval_bell,
                                     self.moveBoat5),
                            Wait(8),
                            self.sfxInterval_creack,
                            self.downWPier,
                            self.moveBoat6,
                            self.moveBoat7,
                            self.moveBoat8,
                            )
 
        #self.check = Sequence(Wait(100),Func(self.requestStormCheck)) ### eventual crash: AssertionError: !is_empty() at line 5385 of panda/src/pgraph/nodePath.cxx
        #self.check.loop()

    def __init__(self,tp=None):        
        self.sfx_bell = self.loadRing('shipbell')
        self.sfx_creack = self.loadRing('dockcreak')
        self.sfx_water = self.loadRing('waterlap')
        
        self.sfxInterval_bell = SoundInterval(self.sfx_bell,loop=0)
        self.sfxInterval_creack = SoundInterval(self.sfx_creack,loop=0)
        self.sfxInterval_water = SoundInterval(self.sfx_water,loop=0)
 
        self.av_startpos = (
                            ((19,106,6.7),(213,0,0)),
                            )
                            
        Hood.__init__(self,"phase_0/streets/street_donalds_dock_sz.bam")
        
        ft = None
        if tp:
            if hasattr(tp,'tunnel') and tp.tunnel:
                ft = tp.tunnel.area.name
 
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
        self.EPier = self.environ.find("**/east_pier")
        self.WPier = self.environ.find("**/west_pier")

        self.trolley = self.environ.find("**/*lley_stat*")
        
        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))
        
        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley
        
        from funAreas import AcornAcres
        
        self.tunnelAA = self.environ.find('**/linktunnel*')
        self.tunnelTTC = self.np.find('**/link*110*')
        self.tunnel2 = self.np.find('**/link*12*')
        self.tunnel3 = self.np.find('**/link*13*')
        
        self.makeSeq()
        
        self._tunnelMovie((
                            (self.tunnelTTC,"AREA_ST_1100",streets.DD_1100),
                            (self.tunnel2,"AREA_ST_1200",streets.DD_1200),
                            (self.tunnel3,"AREA_ST_1300",streets.DD_1300),
                            (self.tunnelAA,"AREA_ACRES",AcornAcres)
                            ),ft)
        
        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
                
class Garden(Hood):
    zoneId = 3000
    music = "phase_8/audio/bgm/DG_nbrhood.mid"
    name = "AREA_GAR"

    def __init__(self,tp=None):         
        self.av_startpos = (
                            ((0,0,0),(0,0,0)),
                            )
                            
        Hood.__init__(self,"phase_0/streets/street_daisys_garden_sz.bam")
        
        ft = None
        if tp:
            if hasattr(tp,'tunnel') and tp.tunnel:
                ft = tp.tunnel.area.name
 
        self.sky1 = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.sky1.reparentTo(self.np)

        self.environ.reparentTo(self.np)
        
        self.trolley = self.environ.find("**/*lley_stat*")
        
        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))
        
        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley
        
        self.tunnelDD = self.environ.find('**/link*520*')
        self.tunnelTTC = self.np.find('**/link*510*')
        self.tunnelSB = self.np.find('**/link*530*')
        
        self._tunnelMovie((
                            (self.tunnelTTC,"AREA_ST_5100",streets.DG_5100),
                            (self.tunnelDD,"AREA_ST_5200",streets.DG_5200),
                            (self.tunnelSB,"AREA_ST_5300",streets.DG_5300),
                            ),tp.getTunnel())
        
        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
                
class Melodyland(Hood):
    zoneId = 4000
    music = "phase_6/audio/bgm/MM_nbrhood.mid"
    name = "AREA_MML"

    def __init__(self,tp=None):         
        self.av_startpos = (
                            ((0,0,0),(0,0,0)),
                            )
                            
        Hood.__init__(self,"phase_0/streets/street_minnies_melody_land_sz.bam")
        
        ft = None
        if tp:
            if hasattr(tp,'tunnel') and tp.tunnel:
                ft = tp.tunnel.area.name
 
        self.sky1 = loader.loadModel("phase_6/models/props/MM_sky.bam")
        self.sky1.reparentTo(self.np)

        self.environ.reparentTo(self.np)
        
        self.trolley = self.environ.find("**/*lley_stat*")
        
        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))
        
        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley
        
        self.tunnelBR = self.environ.find('**/link*42*')
        self.tunnelTTC = self.np.find('**/link*41*')
        self.tunnelDL = self.np.find('**/link*43*')
        
        self._tunnelMovie((
                            (self.tunnelTTC,"AREA_ST_4100",streets.MM_4100),
                            (self.tunnelBR,"AREA_ST_4200",streets.MM_4200),
                            (self.tunnelDL,"AREA_ST_4300",streets.MM_4300),
                            ),tp.getTunnel())
        
        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
                
class Brrrgh(Hood):
    zoneId = 5000
    music = "phase_8/audio/bgm/TB_nbrhood.mid"
    name = "AREA_BRG"

    def __init__(self,tp=None):         
        self.av_startpos = (
                            ((0,0,0),(0,0,0)),
                            )
                            
        Hood.__init__(self,"phase_0/streets/street_the_burrrgh_sz.bam")
        
        ft = None
        if tp:
            if hasattr(tp,'tunnel') and tp.tunnel:
                ft = tp.tunnel.area.name
 
        self.sky1 = loader.loadModel("phase_3.5/models/props/BR_sky.bam")
        self.sky1.reparentTo(self.np)

        self.environ.reparentTo(self.np)
        
        self.trolley = self.environ.find("**/*lley_stat*")
        
        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))
        
        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley
        
        self.tunnelMM = self.environ.find('**/link*32*')
        self.tunnelDD = self.np.find('**/link*31*')
        self.tunnelLB = self.np.find('**/link*33*')
        
        print self.tunnelMM,self.tunnelDD,self.tunnelLB
        #print [x for x in self.environ.findAllMatches('**/link*')]
        #exit()
        
        self._tunnelMovie((
                            (self.tunnelDD,"AREA_ST_3100",streets.BR_3100),
                            (self.tunnelMM,"AREA_ST_3200",streets.BR_3200),
                            (self.tunnelLB,"AREA_ST_3300",streets.BR_3300),
                            ),tp.getTunnel())
        
        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
                
class Dreamland(Hood):
    zoneId = 6000
    music = "phase_8/audio/bgm/DL_nbrhood.mid"
    name = "AREA_DDL"

    def __init__(self,tp=None):         
        self.av_startpos = (
                            ((0,0,0),(0,0,0)),
                            )
                            
        Hood.__init__(self,"phase_0/streets/street_donalds_dreamland_sz.bam")
        
        ft = None
        if tp:
            if hasattr(tp,'tunnel') and tp.tunnel:
                ft = tp.tunnel.area.name
 
        self.sky1 = loader.loadModel("phase_8/models/props/DL_sky.bam")
        self.sky1.reparentTo(self.np)

        self.environ.reparentTo(self.np)
        
        self.trolley = self.environ.find("**/*lley_stat*")
        
        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))
        
        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley
        
        self.tunnelCB = self.environ.find('**/link*92*')
        self.tunnelMM = self.np.find('**/link*91*')
        
        self._tunnelMovie((
                            (self.tunnelMM,"AREA_ST_9100",streets.DL_9100),
                            (self.tunnelCB,"AREA_ST_9200",streets.DL_9200),
                            ),tp.getTunnel())
        
        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
