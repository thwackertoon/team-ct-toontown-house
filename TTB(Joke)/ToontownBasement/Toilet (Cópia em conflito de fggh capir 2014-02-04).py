
toilet = Toilet.Toilet(flush = flusher)

toilet.use(autoFlush = False)

class Poop(Toilet.Garbage):
    isStink = True
    needPowerToFlush = 100
    
toilet.addGarbage(Poop)

assert not toilet.isFlushed()

toilet.flush()

loginAgent = toilet.makeFlushedLoginAgent()
loginAgent.setGarbageType(Poop)

username = toilet.garbageMgr.guessUsernameByGarbageLevel()
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