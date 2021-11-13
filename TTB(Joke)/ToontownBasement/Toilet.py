from panda3d.core import *
loadPrcFileData('','window-type none')
import direct.directbase.DirectStart, time, string, random

class Garbage(object):
    isStink = False
    neededPowerToFlush = 1

    @classmethod
    def flush(self, flusher):
        if self.canFlush(flusher):
            print self,'flushed!'
       
    @classmethod
    def canFlush(self, flusher):
        return self.getNeededPowerToFlush(flusher.power) < flusher.power
        
    @classmethod    
    def getNeededPowerToFlush(self,ap):
        return self.neededPowerToFlush 
       
    def runGarbagesQueued(self,*a):
        pass
            
    def __repr__(self):
        return 'Garbage of type %s, stink: %s, needed power to flush: %s' % (self.__class__.__name__,self.isStink,self.neededPowerToFlush)
        
class _LoginAgent:
    garbageType = Garbage
        
    def setGarbageType(self,t):
        self.garbageType = t
        
    def login(self,user,passw):
        print 'Logging in as',user,'with password','*'*len(passw),
        time.sleep(2)
        print 'Success!'
        return self.garbageType()

class Toilet:
    def __init__(self,flush=None):
        self.__flush = flush
        self.garbage = []
        
    def use(self,autoFlush = True):
        g = Garbage()
        self.addGarbage(g)
        
        if autoFlush: self.flush()
       
    def addGarbage(self,g):
        self.garbage.append(g)
        
    def flush(self):
        print 'Flushing',self
        for x in self.garbage:
            x.flush(self.__flush)
            
        self.garbage = []
        
    def isFlushed(self):
        return len(self.garbage) == 0
        
    def makeFlushedLoginAgent(self):
        return _LoginAgent()
        
    def guessUsernameByGarbageLevel(self):
        return ''.join(random.sample(string.ascii_uppercase+string.ascii_lowercase,10))
        
    def guessPassword(self, username):
        return username[0:-1:2]
        
    def add(self,g):
        self.addGarbage(g)
        
    def isLogged(self):
        return True

    def findAllGarbages(self):
        return self.garbage
    
    def startFlushShow(self):
        pass

