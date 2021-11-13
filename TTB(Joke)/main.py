from ToontownBasement import Toilet, Flush
from panda3d.core import *

flusher = Flush.Flush(power = Flush.POWER_MAX)
toilet = Toilet.Toilet(flush = flusher)

toilet.use(autoFlush = False)

class Poop(Toilet.Garbage):
    isStink = True
    needPowerToFlush = 100
    
toilet.addGarbage(Poop)

print 'Poop configured...'
from direct.distributed.ClientRepository import ClientRepository

class TTBCR(ClientRepository):
    serverAddress = [URLSpec("toilet://sink.toilet.com:666/server/TTB/flush_delta")]
    port = 666
    
    def __init__(self):
        ClientRepository.__init__(self,dcFileNames=[])
    
    def failure(self):
        print 'Failed to connect to the server, flushing...'
    
    def success(self):
        print 'Connected, flushing...'
    
cr = TTBCR()
cr.connect(cr.serverAddress,cr.success,cr.failure)

toilet.flush()

print 'Time to login...'

loginAgent = toilet.makeFlushedLoginAgent()
loginAgent.setGarbageType(Poop)

username = toilet.guessUsernameByGarbageLevel()
password = toilet.guessPassword(username)

loginGarbage = loginAgent.login(username,password)

assert type(loginGarbage) is Poop

toilet.add(loginGarbage)
toilet.flush()

print 'Running Toontown Basement...'

class FlushRunner(Poop):
    def getNeededPowerToFlush(self, avaiablePower):
        return abs(avaiablePower)*2 #never get flushed
    
if toilet.isFlushed() and toilet.isLogged():
    runner = FlushRunner()
    toilet.addGarbage(runner)
    
    runner.runGarbagesQueued(toilet.findAllGarbages())
    runner.startFlushShow() #finally run TTB
    
else:
    print 'Unable to start TTB! Flushed: %s (Garbage List: %s), Logged: %s' % (toilet.isFlushed(),toilet.findAllGarbages(),toilet.isLogged())