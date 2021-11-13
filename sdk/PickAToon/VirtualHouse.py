#test file
#creates a virtual environ with fake toons/data

from PATMgr import ToonSpot, PATMgr
import random, sys

names1 = ("Super","Testing","Weird","Crazy","Professor")
names2 = ("SDK","Test","Coder","Dev","Dude","Bug")

class Resolver:   
    def __init__(self,attr):
        self.attr = attr
        
        self.methods = {
                        'a':self._sys_argv,
                        }
    
        
    def resolve(self,default=None,method=None):
        if type(method) is not str:
            method = ''.join(self.methods.keys())
        
        for m in method:
            r = self.methods[m]()
            if r: return r
            
        return default
        
    def _sys_argv(self):
        #look in sys.argv
        #when looking into sys.argv, add "-" to the beggining
        #eg. look for 'svaddr'->'-svaddr'
        
        if '-'+self.attr in sys.argv:
            return sys.argv[sys.argv.index('-'+self.attr)+1]
     
THEMENAME = Resolver('-themename').resolve()
if not THEMENAME:
    THEMENAME = Resolver('t').resolve()
    if not THEMENAME:
        print 'Error: Not theme specified!'
        print 'How to specify a theme:'
        print '\tVirtualHouse -t <name>'
        print '\t\tOR'
        print '\tVirtualHouse --themename <name>'
        sys.exit(1) 
        
def getName():
    return random.choice(names1)+" "+random.choice(names2)
    
def makeData():
    return {
            'toontype':random.choice(('dog','cat','horse','mouse','rabbit','duck','monkey','bear','pig')),
            'color1':random.random(),
            'color2':random.random(),
            'color3':random.random(),
            'gender':random.choice(('skirt','shorts')),
            'numb':random.choice(range(4)),
           }

total_toons = random.choice(range(3,7))
spots = [ToonSpot(i) for i in xrange(6)]

for x in xrange(total_toons):
    _index = random.choice(range(6))
    while spots[_index].exists:
        _index = random.choice(range(6))
        
    spots[_index].exists = True
    spots[_index].name = getName()
    spots[_index].data = makeData()
    
print "-------------------------"
print
print "Spots:"
print
for spot in spots: print spot
print
print "-------------------------"

from ToonnHead import ToonHead
class HookedHead(ToonHead):
    def __init__(self,head,color,gender):
        self.head = head
        
        self.color = color
        self.gender = gender
        
        ToonHead.__init__(self)
        self.setupHead(self,True)
        
    def getGender(self): return self.gender
    def getHeadColor(self): return self.color
    def getAnimal(self):
        return {'d': 'dog','c': 'cat','h': 'horse',
                'm':'mouse','r':'rabbit','f':'duck',
                'p':'monkey','b':'bear','s':'pig'}[self.head[0]]

def loadToonHead(toontype,color1,color2,color3,numb,gender):

    _color = Vec4(color1,color2,color3,1)
    
    tt = {'d': 'dog','c': 'cat','h': 'horse','m':'mouse','r':'rabbit','f':'duck','p':'monkey','b':'bear','s':'pig'}
    tt = dict(zip(tt.values(),tt.keys()))[toontype]
    
    if tt[0] == "m": numb %= 2
    tt += (("ss","sl","ls","ll"),("ss","ls"))[tt=="m"][int(numb)]
    
    _gender = gender.lower()
    if len(_gender) != 1: _gender = {"shorts":"m","skirt":"f"}[_gender]
    
    #print 'HEAD DNA HOOKER: CONVERTED:',toontype,numb,gender,'->',tt,_gender
    
    head = HookedHead(tt,_color,_gender)
    
    head.startLookAround()
    head.startBlink()
            
    return head

from panda3d.core import *

loadPrcFileData("","window-title Virtual House [TEST ENVIRON FOR PICK A TOON SDK]")
loadPrcFileData("","default-model-extension .bam")
vfs = VirtualFileSystem.getGlobalPtr()
print vfs.mount("../../data/phase_3.mf",".",0)

import direct.directbase.DirectStart

patMgr = PATMgr(spots)
patMgr._generateHeads(loadToonHead)

from ThemeLoader import *
t = loadTheme(THEMENAME)
t.enter(patMgr)

run()