from panda3d.core import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject

from tth.avatar.toon import EToon

from random import randint
import sys

class Timer:
    def __init__(self,time,callback,stepCb=lambda *t:0):
        self.starttime=time
        self.time=time
        self.cb=callback
        self.scb=stepCb
        self.task = taskMgr.add(self.timeDown,"timerTask")
        self.text = None
        
    def timeDown(self, task):
        self.time = self.starttime-task.time
        if self.time<0:
            self.cb()
            return task.done
        if self.text: self.text.setText(str(int(self.time)))
        self.scb(self.time)
        return task.cont
    
class GlobalClock(Timer):
    def __init__(self,frame,time,callback,stepCb=lambda *t:0):
        self.callback = callback
        Timer.__init__(self,time,self.timeup,stepCb)
        self.clock = OnscreenImage(image="data/clock.png",pos=(1.1,0,.85),scale=.1,parent=frame)
        self.text = OnscreenText(text="",scale=.6,parent=self.clock,mayChange=True)
    
    def timeup(self):
        self.clock.removeNode()
        self.callback()
    
def MGR_SFX_speech(spc,text):
    #print "MSs:",spc,text
    _file = "phase_3.5/audio/dial/AV_{0}_[].mp3".format(spc)
    
    if 'ooo' in text: return loader.loadSfx(_file.replace('[]','howl'))
    if text.endswith('?'): return loader.loadSfx(_file.replace('[]','question'))
    if text.endswith('!'): return loader.loadSfx(_file.replace('[]','exclaim'))
    if len(text.split())>=6: return loader.loadSfx(_file.replace('[]','long'))
    if len(text.split())>=3: return loader.loadSfx(_file.replace('[]','med'))
    else: return loader.loadSfx(_file.replace('[]','short'))
    
class ChatManager(DirectObject):
    def __init__(self):
        self.menuGui = None
        
    def parse(self,_str):
        while '@' in _str:
            _pos = _str.find('@')
            _pattern = _str[_pos:].split(' ',1)[0]
            _new = L10N.sc_fetch(_pattern[1:])[0][0]
            _str = _str.replace(_pattern,_new)
            
        return _str
        
class DistrictManager(DirectObject):
    def __init__(self):
        
        self.names = filter(lambda x: '(' not in x,[
                      "", #none at id 0
                      "Loblao's Zone", #id 1 loblao
                      "Folicity", #id 2 s0r00t
                      "Strogonoff City", #id 3 pitbull
                      "(this one is for junior)", #id 4 junior
                      "Lesados dos Campos", #id 5 matheus
                      "DXDlandia", #id 6 davi
                      "(this one is for lucas)", #id 7 lucas
                      "Toontropolis", #id 8 fritz
                      "Raw Juice", #id 9 hassan
					  "Nutty River" #id 10 Jean
                      ])
                      #based on skype, plz complete if someone has been forgotten
                      #if its not set will be kicked out!
                      
        self.names.sort()
        
        self.district = min(randint(1,len(self.names)),1) #never 0
        
    def goTo(self,district):
        self.district = district
        _av = gamebase.toonAvatar[0]
        cArea = gamebase.curArea
        
        from tth.areas.etc import Teleporter
        Teleporter(cArea.__class__,cArea.name).go()
        
    def goToWithMovie(self,district):
        self.district = district
        gamebase.toonAvatar[0].b_setState("Teleport",str(gamebase.curArea.zoneId))
        
    def get(self,zone):
        return zone+(10**7)*self.district
        
class CDRManager:
    def redeemCode(self, code, callback):
        self.callback = callback
        taskMgr.doMethodLater(1,self.__callback,"cdr callback")
        
    def __callback(self,task = None):
        self.callback(6,0)
        if task: return task.done
        
class HoodManager:
    def __init__(self):
        taskMgr.doMethodLater(10,self.__def,"hoodmgrdef")
        
        from tth.areas.hoods import TTCentral, Dock, Garden, Melodyland, Brrrgh, Dreamland
        from tth.areas.funAreas import Speedway, AcornAcres
        from tth.areas.coghqs import BossbotHQ, SellbotHQ, CashbotHQ, LawbotHQ, SellbotHQFactoryExterior
        
        self.symbols = {
                        2000:(Dock,"AREA_DDK"),
                        1000:(TTCentral,"AREA_TTC"),
                        5000:(Brrrgh,"AREA_BRG"),
                        4000:(Melodyland,"AREA_MML"),
                        3000:(Garden,"AREA_GAR"),
                        2400:(AcornAcres,"AREA_ACRES"),
                        1400:(Speedway,"AREA_SPEEDWAY"),
                        6000:(Dreamland,"AREA_DDL"),
                        10000:(BossbotHQ,"AREA_HQ_BOSS"),
                        7000:(SellbotHQ,"AREA_HQ_SELL"),
                        8000:(CashbotHQ,"AREA_HQ_CASH"),
                        9000:(LawbotHQ,"AREA_HQ_LAW"),
                        }
                        
        #these are for cogPoints (fetched by CogStates.py)
        self.symbols[7100] = (SellbotHQFactoryExterior,"")
        
        #streets
        from tth.areas.streets import *
        self.symbols[7100] = (SellbotHQFactoryExterior,"")
        x = "TTC_2100,TTC_2200,TTC_2300,DD_1100,DD_1200,DD_1300,DG_5100,DG_5200,DG_5300,MM_4100,MM_4200,MM_4300,BR_3100,BR_3200,BR_3300,DL_9100,DL_9200".split(",")
        for y in x:
            id = y.split("_")[-1]
            self.symbols[int(id)] = eval(y)
    
    def __def(self,task): #have a delay till L10N is defined
        self.ids = (2000,1000,5000,4000,3000,2400,1400,6000,10000,7000,8000,9000)
        
        self.names = map(L10N,(
                                "AREA_DDK","AREA_TTC","AREA_BRG","AREA_MML",
                                "AREA_GAR","AREA_ACRES","AREA_SPEEDWAY",
                                "AREA_DDL","AREA_HQ_BOSS","AREA_HQ_SELL",
                                "AREA_HQ_CASH","AREA_HQ_LAW",
                                ))
        
        self.id2name = dict(zip(self.ids,self.names))
        
        return task.done
        
    def getFullnameFromId(self,id,sort=False):
        if sort:
            _ids = list(self.ids[:])
            _ids.sort(key=int)
            id = [p for p in _ids if p<id][-1]
            
        return self.id2name[id]
        
    def getNameFromId(self,id):
        return self.id2name[id]
        
    def bookTp(self,zone):
        x,y = self.symbols.get(zone,(None,None))
        if not x:
            print 'Failed to teleport to zone %s (no symbol)' % zone
            return
            
        from tth.areas.etc import Teleporter
        Teleporter(x,y).go()
        
    def getHQFromOldStyle(self,id,default=None):
        return {
                11000:self.symbols[7000][0],
                12000:self.symbols[8000][0],
                13000:self.symbols[9000][0],
                14000:self.symbols[10000][0],
               }.get(id,default)
        
class FriendshipManager(DirectObject):
    LIMIT = 75
    def __init__(self):
        self.friends = []
        self.accept('loadToon',self.update)
        self.accept('friendsListChanged',self.update)
        
        self.online = {}
        self.dna = {}
        
        self.requests = 0
        
    def update(self):
        self.friends = set(gamebase.toonAvatarStream.read("friends",[]))
        print self.friends
        for f in self.friends:
            self.requests += 1
            id = f[0]
            print 'Issue data request for',id
            messenger.send("requestToonData",[int(id),0,self.__gotInfo,id])
            
    def __gotInfo(self,data,id):
        io = data.get('isOnline',False)
        self.online[id] = io
        self.dna[id] = EToon.makeDnaStatic(data)
        print ':FriendshipMgr: Updated',id,io#,data
        self.requests -= 1
        
    def isLoaded(self):
        return self.requests == 0
            
    def isOnline(self,x):
        return self.online.get(str(x),False)
        
    def getDna(self,x):
        return self.dna.get(x,{}).copy()
    
    def isFriend(self,id):
        return str(id) in map(lambda x:x[0],self.friends)