from panda3d.core import *
loadPrcFileData('','window-type none')

from ToonGlobber import *

import time
def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f s' % (f.func_name, (time2-time1))
        return ret
    return wrap
    
for x in map(lambda x:"../../data/phase_"+str(x)+".mf",(3,3.5,4,5.5,5,6,7,8,9,10,11,12,13)):
    print x,vfs.mount(x,".",0)

@timing
def main():
    for i in xrange(1):
        x = smartScan()
        print
        print len(x)
        
        skirt = set(filterByGender(x,"skirt"))
        torso = set(filterByPart(x,"torso"))
        l = set(filterByKind(x,"l"))
        
        print "skirt",len(skirt)
        print "torso",len(torso)
        print "l",len(l)
        
        print
        all = skirt & torso & l
        print "skirt and torso and l",len(all)
        print all == loadTorsoAnims(x,"skirt","l")
    
main()