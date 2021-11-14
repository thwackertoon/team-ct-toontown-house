# -*- coding: latin-1 -*-
"""
File: etc.py
    Module: cogtown.areas
Author: Nacib
Date: AUGUST/14/2013
Description: some util stuff
FROM COGTOWN
"""

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import *
from random import choice, random, randint
from tth.managers import Timer

import sys

class TeleportScreen:
    def __init__(self,name,_time=3):
        if not name.startswith('AREA_'): name = 'AREA_'+name
        self.loadingImage = OnscreenImage(image="phase_3/maps/background.jpg",parent=render2d)
        _text = u"{0} {1}...".format(L10N('TPS_GOINGTO'),L10N(name))
        self.text = OnscreenText(text=_text,pos=(-1.2,-.72),scale=.07,fg=(0,0,139,139),font=loader.loadFont("phase_3/models/fonts/ImpressBT.ttf"),align=TextNode.ALeft)
        self.ttlogo = OnscreenImage(image="phase_0/toontown-logo.png",scale=.3,pos=(0,0,.75))
        self.ttlogo.setSx(.8)
        self.ttlogo.reparentTo(self.loadingImage)
        self.ttlogo.setTransparency(TransparencyAttrib.MAlpha)
        self.tipFrame = loader.loadModel('phase_3/models/gui/toon_council').find('**/scroll')
        self.tipFrame.reparentTo(self.ttlogo)
        self.tipFrame.setZ(-2.175)
        self.tipFrame.setSz(1.3)
        self.tipFrame.setSx(.675)
        self.ttlogo.setTransparency(TransparencyAttrib.MAlpha)

        selected=L10N('TPS_TIPTITLE')+'\n'+L10N.tip()
        
        self.tipText = TextNode('tiptext')
        self.tipText.setWordwrap(20)
        self.tipText.setWtext(selected)
        self.tipText.setFont(loader.loadFont("phase_3/models/fonts/ImpressBT.ttf"))
        self.tipText.setTextColor(0,0,0,1)
        self.tipTextNp = self.tipFrame.attachNewNode(self.tipText)
        self.tipTextNp.setScale(.12)
        self.tipTextNp.setX(-1.2)
        self.tipTextNp.setZ(.15)
        
        self.falseBar = DirectWaitBar(text = "", value = 0, pos = (0,0,-.8))
        self.falseBar.setSz(.5)
        self.falseBar.setSx(1.2)
        
        Timer(_time,lambda:0,self.step)
        
        self.bar_anim_brpoints = [0]
        for i in xrange(8): self.bar_anim_brpoints.append(randint(1,68))
        self.bar_anim_brpoints.append(83)
        self.bar_anim_brpoints.append(100)
        self.bar_anim_brpoints.sort(key=int)
        
    def step(self,time):
       self.falseBar['value'] = [i for i in self.bar_anim_brpoints if i<=(3-time)/3*100][-1]

    def dismiss(self):
        print 'Removing tp screen...'
        self.loadingImage.destroy()
        self.text.destroy()
        taskMgr.remove('timerTask')
        self.falseBar.destroy()

class Teleporter:
    def __init__(self, target, name="", extraArgs=[], tunnel = None, door = None):
        self.target = target
        self.name=name
        self.extraArgs=extraArgs
        self.tunnel = tunnel
        self.door = door
        
        if not hasattr(self.target,"__tth_area__"): raise ToontownHouseError('Teleporter 0x000: alvo fornecido invalido!') #WTF
        
    def go(self):
        #load new after 1 sec (4 if debbuging)
        _time = (1,4)[base.isInjectorOpen]
        if '-fast' in sys.argv:
            time = .1
        self.lsc = TeleportScreen(self.name)
        #destroy current area
        if gamebase.curArea is not None:
            a = gamebase.curArea.__tth_area__()
            if a:
                taskMgr.remove(a['name'])
                gamebase.curArea.avatar.reparentTo(NodePath('dummy'))
                base.cam.wrtReparentTo(render)#gamebase.curArea.avatar)

                if hasattr(gamebase.curArea,"seq"): gamebase.curArea.seq.finish()
                
                a["models"].removeNode()
                a["gui"].destroy()
                a["bgm"].stop()
               
                for s in a["speeches"]:
                    try:
                        s.frame.destroy()
                    except:
                        pass
                print 'Removed',a["name"]
                gamebase.curArea.destroy()
                gamebase.curArea.ignoreAll()

        if len(self.extraArgs): taskMgr.doMethodLater(_time,self._goTaskArgs, 'tpTask', extraArgs = [self.extraArgs])
        else: taskMgr.doMethodLater(_time,self._goTask, 'tpTask')
        
    def _goTask(self,task):
        self.target(tp = self)
        return Task.done
    
    def _goTaskArgs(self,*args):
        l = args
        self.target(*l,tp = self)
        return Task.done
        
    def getTunnel(self):
        try: return self.tunnel.area.name
        except: return None
        
    def getDoor(self):
        try: return self.door.area.name
        except: return None
        
    def done(self):
        self.lsc.dismiss()
