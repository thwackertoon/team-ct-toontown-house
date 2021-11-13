
sky1 = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
sky1.reparentTo(render)
sky1.setScale(2)
 
tunnel = loader.loadModel("phase_4/models/modules/safe_zone_tunnel_TT.bam")
tunnel.reparentTo(render)
tunnel.setPos(60,175,-7)
tunnel.setHpr(180,0,0)
tunnel.setScale(1)
tunnelsign = loader.loadModel("phase_4/models/props/tunnel_sign_green.bam")
tunnelsign.reparentTo(tunnel)
tunnelsign.setPos(60,95.01,23.7)
tunnelsign.setHpr(180,0,0)
tunnelsign.setScale(1.6)
SZsign = loader.loadModel("phase_4/models/props/goofySZ.bam")
SZsign.reparentTo(tunnel)
SZsign.setPos(60,95.025,23.7)
SZsign.setHpr(180,0,0)
SZsign.setScale(4)
 
kartshop = loader.loadModel("phase_6/models/karting/kartShop.bam")
kartshop.reparentTo(render)
kartshop.setPos(0,10,0)
 
scoreboard = loader.loadModel("phase_6/models/karting/tt_m_ara_gfs_leaderBoardCrashed.bam")
scoreboard.reparentTo(render)
scoreboard.setPos(1,-111,0)
scoreboard.setHpr(180,0,0)
 
wrench = loader.loadModel("phase_6/models/karting/KartArea_WrenchJack.bam")
wrench.reparentTo(render)
wrench.setPos(-33,5,0)
wrench.setHpr(180,0,0)
 
tires = loader.loadModel("phase_6/models/karting/KartArea_Tires.bam")
tires.reparentTo(render)
tires.setPos(33,5,0)
 
trees1 = loader.loadModel("phase_6/models/karting/GoofyStadium_TreeBase.bam")
trees1.reparentTo(render)
trees1.setPos(-13,58,-0.3)
trees1.setScale(12)
 
trees2 = loader.loadModel("phase_6/models/karting/GoofyStadium_TreeBase.bam")
trees2.reparentTo(render)
trees2.setPos(13,58,-0.3)
trees2.setScale(12)
 
trees3 = loader.loadModel("phase_6/models/karting/GoofyStadium_TreeBase.bam")
trees3.reparentTo(render)
trees3.setPos(-13,-35,-0.3)
trees3.setScale(12)
 
trees4 = loader.loadModel("phase_6/models/karting/GoofyStadium_TreeBase.bam")
trees4.reparentTo(render)
trees4.setPos(13,-35,-0.3)
trees4.setScale(12)
 
trees5 = loader.loadModel("phase_6/models/karting/GoofyStadium_TreeBase.bam")
trees5.reparentTo(render)
trees5.setPos(-10,-76,-0.3)
trees5.setScale(12)
 
trees6 = loader.loadModel("phase_6/models/karting/GoofyStadium_TreeBase.bam")
trees6.reparentTo(render)
trees6.setPos(10,-76,-0.3)
trees6.setScale(12)
 
light1 = loader.loadModel("phase_6/models/karting/GoofyStadium_Lamppost_Base1.bam")
light1.reparentTo(render)
light1.setPos(-10,-52,-0.7)
light1.setScale(14)
 
light2 = loader.loadModel("phase_6/models/karting/GoofyStadium_Lamppost_Base1.bam")
light2.reparentTo(render)
light2.setPos(10,-52,-0.7)
light2.setScale(14)
 
box = loader.loadModel("phase_6/models/karting/GoofyStadium_Mailbox.bam")
box.reparentTo(render)
box.setPos(16,-50,0)
box.setHpr(210,0,0)
box.setScale(10)
 
flag1 = loader.loadModel("phase_6/models/karting/flag.bam")
flag1.reparentTo(render)
flag1.setPos(-18,6,-0.2)
 
flag2 = loader.loadModel("phase_6/models/karting/flag.bam")
flag2.reparentTo(render)
flag2.setPos(18,6,-0.2)
 
sign = loader.loadModel("phase_6/models/karting/KartShowBlockSign.bam")
sign.reparentTo(render)
sign.setPos(-16,-50,0)
sign.setHpr(-120,0,0)
sign.setScale(26)
 
announcer1 = loader.loadModel("phase_6/models/karting/announcer.bam")
announcer1.reparentTo(render)
announcer1.setPos(25,-150,-0.7)
announcer1.setHpr(-140,0,0)
 
announcer2 = loader.loadModel("phase_6/models/karting/announcer.bam")
announcer2.reparentTo(render)
announcer2.setPos(-26,-149,-0.7)
announcer2.setHpr(-212,0,0)
 
announcer3 = loader.loadModel("phase_6/models/karting/announcer.bam")
announcer3.reparentTo(render)
announcer3.setPos(-38,-135,-0.7)
announcer3.setHpr(-212,0,0)
 
announcer4 = loader.loadModel("phase_6/models/karting/announcer.bam")
announcer4.reparentTo(render)
announcer4.setPos(37,-137.5,-0.7)
announcer4.setHpr(-140,0,0)
 
cone1 = loader.loadModel("phase_6/models/karting/cone.bam")
cone1.reparentTo(render)
cone1.setPos(13,-4,-0.3)
 
cone2 = loader.loadModel("phase_6/models/karting/cone.bam")
cone2.reparentTo(render)
cone2.setPos(13,20,-0.3)
 
cone3 = loader.loadModel("phase_6/models/karting/cone.bam")
cone3.reparentTo(render)
cone3.setPos(-14,18,-0.3)
 
cone4 = loader.loadModel("phase_6/models/karting/cone.bam")
cone4.reparentTo(render)
cone4.setPos(-14,-3,-0.3)
 
cone5 = loader.loadModel("phase_6/models/karting/cone.bam")
cone5.reparentTo(render)
cone5.setPos(-23,9,-0.3)
 
cone6 = loader.loadModel("phase_6/models/karting/cone.bam")
cone6.reparentTo(render)
cone6.setPos(45,-138,-0.6)
 
cone7 = loader.loadModel("phase_6/models/karting/cone.bam")
cone7.reparentTo(render)
cone7.setPos(25,-109,0)
 
cone8 = loader.loadModel("phase_6/models/karting/cone.bam")
cone8.reparentTo(render)
cone8.setPos(24,-111,0)
cone8.setHpr(45,0,0)
 
cone9 = loader.loadModel("phase_6/models/karting/cone.bam")
cone9.reparentTo(render)
cone9.setPos(75,-106,0)
cone9.setHpr(0,0,-120)
 
cone10 = loader.loadModel("phase_6/models/karting/cone.bam")
cone10.reparentTo(render)
cone10.setPos(76.5,-107.5,0)
cone10.setHpr(0,120,0)
 
cone11 = loader.loadModel("phase_6/models/karting/cone.bam")
cone11.reparentTo(render)
cone11.setPos(26,-154,-0.7)
cone11.setHpr(42,0,0)
 
cone12 = loader.loadModel("phase_6/models/karting/cone.bam")
cone12.reparentTo(render)
cone12.setPos(1,-187,1.22)
cone12.setHpr(42,0,0)
 
krate1 = loader.loadModel("phase_6/models/karting/krate.bam")
krate1.reparentTo(render)
krate1.setPos(1,-187,-0.7)
krate1.setScale(1.2)
 
krate2 = loader.loadModel("phase_6/models/karting/krate.bam")
krate2.reparentTo(render)
krate2.setPos(-48,-115,-0.7)
krate2.setScale(1.2)
 
krate3 = loader.loadModel("phase_6/models/karting/krate.bam")
krate3.reparentTo(render)
krate3.setPos(-50,-113,-0.7)
krate3.setHpr(45, 0, 0)
krate3.setScale(1.2)
 
krate4 = loader.loadModel("phase_6/models/karting/krate.bam")
krate4.reparentTo(render)
krate4.setPos(-49,-114,1.22)
krate4.setHpr(60, 0, 0)
krate4.setScale(1.2)

base.oobe()
run()
