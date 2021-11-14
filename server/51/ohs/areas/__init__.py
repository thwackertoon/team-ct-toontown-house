from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

class ZoneHandler:
    def __init__(self,isSafeZone):
        self.toons = []
        self.isSafeZone = isSafeZone
        if not isSafeZone:
            self.cogs = []
        
    def readToons(self):
        d = []
        for toon in self.toons:
            d.append(toon.read())