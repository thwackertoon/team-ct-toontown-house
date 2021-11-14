class ConnHandler:
    def __init__(self,conn):
        self.zoneId = -1
        self.acc = None
        self.cToon = None
        self.conn = conn
        
class AccHandler:
    def __init__(self, acc):
       self.acc = acc
       
class ToonHandler:
    def __init__(self,toonDna,name):
        self.dna = toonDna
        self.name = ""
        self.poshpr = [0,0,0,0,0,0]
        
    def setX(self,a): self.poshpr[0] = a
    def setY(self,a): self.poshpr[1] = a
    def setZ(self,a): self.poshpr[2] = a
    def setPos(self,a,b,c):
        self.poshpr[0] = a
        self.poshpr[1] = b
        self.poshpr[2] = c
    def setH(self,a): self.poshpr[3] = a
    def setP(self,a): self.poshpr[4] = a
    def setR(self,a): self.poshpr[5] = a
    def setHpr(self,a,b,c):
        self.poshpr[3] = a
        self.poshpr[4] = b
        self.poshpr[5] = c
    
    def read(self):
        return make_buffer([self.name,self.dna,self.poshpr])