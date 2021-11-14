"""
File: loader.py
    Module: tth.avatar
Author: Nacib
Date: JULY/25/2013
Description: Handle avatar stuff: models(actor), basics, avatar class, etc
FROM COGTOWN #LOOOOOOOL
"""

from toon import *
from direct.actor.Actor import *
from direct.showbase.DirectObject import *

from direct.task.Task import *

from direct.gui.DirectGui import *
from pandac.PandaModules import *

import math, pickle
from StringIO import *

def loadToonData(id):
    data = globalBlob.all()
    for key in data.keys():
        if not key.endswith(str(id)): del data[key]
    nd = {}
    for key in data.keys():
        nd[key[:-1]] = data[key]
    return nd

def writeToonData(id,attr,overwrite=1):
    for key in attr.keys():
        globalBlob.write(key+str(id),attr[key],not overwrite)
    globalBlob.flush()
   
def getAvatarName(slot):
    data = loadToonData(slot)
    name=None
    if "name" in data:
        name = data["name"]
    return name

def saveNewToon(slot,name,body,legs,head,texture1,texture2,color1,color2,color3,spc,gender,nmba='',_nta=''):
    toonId = globalBlob.newToon(name,nmba,slot,_nta)
    writeToonData(slot, {"toonId":toonId,
                        "name":name,
                        "head":head,
                        "body":body,
                        "legs":legs,
                        "top":texture1,
                        "bot":texture2,
                        "color1":color1,
                        "color2":color2,
                        "color3":color3,
                        "lastArea":"tth.areas.Tutorial",
                        "lastAreaName":"AREA_Toontorial",
                        "hp":"15",
                        "curhp":"15",
                        "gender":gender,
                        "spc":spc,
                        "other":pickle.dumps({}) #put pickled extra data here
                        })
    
def loadToonAvatar(slot):
    print 'Loading toon at slot',slot
    data = loadToonData(slot)
    if not "name" in data:
        print 'No such toon! Launching create-a-toon...'
        #there is not a toon in this slot! (WAT? cog?)(Fixed LOL)
        messenger.send('init-createatoon')
        return (None,None)
        
    zone = 1
    if "lastZoneId" in data:
        zone = data["lastZoneId"]
        
    zone = int(zone)
    #load avatar model
    
    _map = lambda *a,**k: tuple(map(*a,**k))
    dna = EToon(render,["cat","pig","dog","horse","bear","mouse","duck","rabbit","monkey"][int(data['spc'])],
        _map(lambda x:float(x.strip('()')),data["color1"].split(',')),_map(lambda x:float(x.strip('()')),data["color2"].split(',')),
        _map(lambda x:float(x.strip('()')),data["color3"].split(',')),data["body"],{"M":"shorts","F":"skirt"}[data["gender"]],
        float(data["legs"]),data['head'],False,(data['top'],data['bot'],None),data["name"],{"toonId":data["toonId"]}).makeDna()

    t = base.cr.createDistributedObject(className = 'DistributedAvatar', zoneId = base.distMgr.get(zone))
    t.isLocalToon = True
    t.b_setToonDna(dna)
    
    tag = t.toon.tag
    
    from direct.controls.GravityWalker import GravityWalker
        
    if True:
        wc = GravityWalker(legacyLifter=True)
        wc.setWallBitMask(BitMask32(1))
        wc.setFloorBitMask(BitMask32(2))
        wc.setWalkSpeed(18.0, 24.0, 8.0, 80.0)
        wc.initializeCollisions(base.cTrav, t._toon, floorOffset=0.025, reach=4.0)

        wc.enableAvatarControls()
        t._m.physControls = wc
        t._m.physControls.placeOnFloor()
    
    return (t,tag,data["lastArea"],data["lastAreaName"])
                        
class AvatarStream(DirectObject):
    def __init__(self,toonSlot):
        self.slot = toonSlot
        self.data = loadToonData(toonSlot)
        self._ex_attr = ["name","head","body","texture1","texture2","level","lastArea","spc",
                            "lastAreaName","hp","curhp","color1","color2","color3","lastZoneId","toonId"]
                            
        self.accept('stream_reload',self.__reload)
        
    def __reload(self):
        self.data = loadToonData(self.slot)
        
    def read(self, attr, default=None):
        if attr in self._ex_attr:
            return self.data[attr]
        else:
            return self.loadInPickled(self.data["other"],attr,default)
        
    def write(self, attr, value):
        if attr in self._ex_attr:
            self.data[attr] = value
            writeToonData(self.slot,{attr:value})
            
        else:
            self.saveInPickled(attr,value)
            writeToonData(self.slot,{"other":self.data["other"]})
            
    def loadInPickled(self, data, attr, default=None):
        _data = pickle.loads(data)
        if not attr in _data:
            self.saveInPickled(attr,default)
            writeToonData(self.slot,{"other":self.data["other"]})
            _data = pickle.loads(self.data["other"])
        return _data.get(attr,default)   
    
    def saveInPickled(self, attr, value):
        data = pickle.loads(self.data["other"])
        data[attr] = value
        self.data["other"] = pickle.dumps(data)
        
    def add(self, attr, value):
        cur = self.read(attr,0)
        new = cur+value
        self.write(attr,new)
        
    def sub(self, attr, value):
        cur = self.read(attr,0)
        new = cur-value
        self.write(attr,new)
    
    def setPlayRate (self, *args,**kw): self._toon.setPlayRate(*args,**kw)
