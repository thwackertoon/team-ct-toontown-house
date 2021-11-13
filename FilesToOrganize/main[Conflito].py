# -*- coding: latin-1 -*-         #
# Autor: Junior and Nacib         #
# Modelos: Disney Toontown Online #
###################################

from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *

import __builtin__, os

#mount the MFs
mfRoot = "./"
if not hasattr(__builtin__,"isCompiled"): mfRoot = "data/"
mfs = [mfRoot+x for x in os.listdir(mfRoot) if x.endswith(".mf")]
vfs = VirtualFileSystem.getGlobalPtr()
for mf in mfs: print "mounting",mf,vfs.mount(mf,".",VirtualFileSystem.MFReadOnly,(lambda x,y:x.decode(y))("ggu0hf3","rot13"))
getModelPath().appendDirectory("./data")

from tth.avatar.loader import *
from tth.avatar.toon import *
from tth.lsc import *
from tth.areas.createatoon import *
from tth.datahnd.NetworkedBlob import *
from tth.datahnd.Blob import *

# start list of areas import
from tth.areas.Toontorial import *
from tth.areas.area51 import *
from tth.areas.hoods import *
from tth.areas.estate import *
from tth.areas.funAreas import *
from tth.areas.coghqs import *
from tth.areas.doyouthinkimcoolbecauseihaveawesomefilenamesideas import * #name written at hand !
from tth.areas.idk import * #idk why
#end list

from tth.l10n import l10n
from tth.managers import *
from tth.managers import MGR_SFX_speech as MSs

import os
import sys
import math
import time
import zlib
from urllib import urlopen as ulib_uo
from cPickle import loads as pkl_ld, dumps
import __builtin__

wp = WindowProperties.getDefault() 
wp.setTitle("Toontown House")
wp.setIconFilename("toontown.ico")
wp.setCursorFilename("toonmono.cur")
wp.setFixedSize('-locksize' in sys.argv)
wp.setSize(800,600)
WindowProperties.setDefault(wp)

loadPrcFileData("","default-model-extension .bam")
loadPrcFileData('','audio-library-name p3fmod_audio')
###############################

class Resolver:   
    def __init__(self,attr):
        self.attr = attr
        
        self.methods = {
                        'o':self._os_environ,
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
            
    def _os_environ(self):
        #look in on.environ
        #when looking into os.environ, add "TTH_" to the beggining and make it uppercase
        #eg. look for 'svaddr'->'TTH_SVADDR'
        
        return os.environ.get("TTH_"+self.attr.upper(),None)
        
VER_INC = True
if Resolver('svaddr').resolve('') not in ["localhost","78.236.116.224"]: #'-fp' in sys.argv and VER_INC:#
    if not hasattr(__builtin__,'isCompiled'):
        #print('HEY! I (nacib) am making some changes to the server! It means that if you connect it will crash!')
        print("HEY! I (s0r00t or nacib) am doing nothing! It means that if you connect it will crash!")
        #print('IF YOU WANNA PLAY DO ---- NOT ---- USE -fp')
        print('exiting!')
        sys.exit()
###############################

if not hasattr(__builtin__,"isCompiled"):
    print ('Not compiled! Using standard glob...')
    import glob
    __builtin__.glob = glob

class ToontownHouseError(Exception):pass

##################################################
#implemetation of Cogtown Injector for easy debugging!
def runInjectorCode():
        global text
        exec (text.get(1.0, "end"),globals())
    
def openInjector():
    import Tkinter as tk
    from direct.stdpy import thread
    root = tk.Tk()
    root.geometry('600x400')
    root.title('Cogtown (TTH version) Injector')
    root.resizable(False,False)
    global text
    frame = tk.Frame(root)
    text = tk.Text(frame,width=70,height=20)
    text.insert(1.0, "#set gags\n\ng = gamebase.toonAvatarStream.read('gags',[[-1]*7]*7)\ng[0][-1] = 0\ngamebase.toonAvatarStream.write('gags',g)\n\n#clone code > FOR DEBUGGING\nt=gamebase.toonAvatar[0]\na=gamebase.curArea\n\nx=base.cr.createDistributedObject\\\n\t(className='DistributedAvatar',zoneId=base.distMgr.get(a.zoneId))\n\nd=load_buffer(t.dna)\nd['toontype']='cat'\nx.b_setToonDna(make_buffer(d))\n\nt.b_speak('SUCCESSFULLY CLONED MYSELF LOL!')")
    text.pack(side="left")
    tk.Button(root,text="Inject!",command=runInjectorCode).pack()
    scroll = tk.Scrollbar(frame)
    scroll.pack(fill="y",side="right")
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    frame.pack(fill="y")
    
    thread.start_new_thread(root.mainloop,())
    

##################################################

if '--debug' in sys.argv or '-d' in sys.argv:
    if not '-nd' in sys.argv: loadPrcFileData("", "want-directtools #t")
    #loadPrcFileData("", "notify-level-gobj info")
    if '-tk' in sys.argv: loadPrcFileData("", "want-tk #t")
    if not '--noinj' in sys.argv and not '-ni' in sys.argv:openInjector()
    
if '--no-audio' in sys.argv or '-na' in sys.argv:
    loadPrcFileData("", "audio-library-name null")

import direct.directbase.DirectStart

base.isInjectorOpen = '--debug' in sys.argv #or '-d' in sys.argv
base.isCompiled = hasattr(__builtin__,"isCompiled")
    
def erroZuado(msg=None): #Can you edit this function to use l10n (and for me to understand :D) ? lol OK / Thanks ! (looool)
    import ctypes
    MessageBox = ctypes.windll.user32.MessageBoxA
    texts = [
            'Não foi possível movimentar seu Toon. Sugiro fazer uma dieta!',
            'Não foi possível criar esse Toon. O nome foi reprovado pelo Amizade Fácil!',
            'Não encontramos o arquivo z0eir2.tr00l, tente novamente!',
            'O arquivo z0eir2.tr00l está corrompido, chore!',
        #    'POOTISPOOTISPOOTISPOOTISPOOTISPOOTISPOOTIS' #huh? #nothing is in english so i want to add something i understand :D ~s0r00t
            ]
    if not msg: msg = __import__('random').choice(texts)
    MessageBox(None, 'Erro fatal:'+msg, 'Erro', 1)
    sys.exit()
    
base.accept('f6',erroZuado)

from direct.distributed.ClientRepository import ClientRepository
class MyClientRepository(ClientRepository):
    def __init__(self):
        dcFileNames = ['server/tth.dc']
        
        ClientRepository.__init__(self, dcFileNames = dcFileNames)
        
        self.onConnLoad = False
        self.isConnected2 = False
        
        self.kickCode = -1
        
        door = (4000,4011)[hasattr(__builtin__,'isCompiled')]
        if '-fp' in sys.argv: door = 4011 #force public
        self.url = URLSpec('http://%s:%s' % (Resolver('svaddr').resolve('gs-alpha.toontownhouse.net'), door ))
        self._connect()
        
    def _connect(self):
        self.connect([self.url],
                        successCallback = self.connectSuccess,
                        failureCallback = self.connectFailure)
        
    def connectFailure(self, statusCode, statusString):
        print "Not connected!",statusCode,statusString
        #base.transitions.fadeScreen(1)
        
        def _cb(a):
            print a
            self.diag.cleanup()
            if a == -1:
                sys.exit()
            self._connect()
            
        from tth.gui import dialog
        self.diag = dialog.OkCancelDialog(text="Failed to connect to the server! Error code: "+str(statusCode)+'. Try again?',
                                          command = _cb, fadeScreen=1, buttonGeomList=[dialog.okButtons,dialog.cancelButtons],
                                          button_relief = None, buttonTextList = [("","\n\nOK","\n\nOK"),("","\n\nExit","\n\nExit")])
        
    def connectSuccess(self):
        print ":CR: Connected!"
        self.setInterestZones([1000]) #hear AI async
        
        self.acceptOnce('createReady', self.createReady)
        
        taskMgr.doMethodLater(1,self.monitorConn,'monitor connection')
        
    def monitorConn(self,task):
        if not self.isConnected():
            def _exit(*a): raise ToontownHouseError('CR 0x001: the server kicked us out! Or maybe the player DC? IDK...')
            
            base.transitions.fadeScreen(1)
            
            from tth.gui import dialog
            dialog.OkDialog(text="Lost connection to server!", command = _exit,
                            fadeScreen=1, buttonGeomList=[dialog.okButtons])
        
        return task.again
        
    def createReady(self): 
        self.isConnected2 = True
        if self.onConnLoad:
            gamebase.ldScr.dismiss()
        self.createDistributedObject(className = 'AccountMgr', zoneId = 1000)
        
base.cr = MyClientRepository() 
base.distMgr = DistrictManager()
base.distMgr.district = sys.argv[sys.argv.index('-fd')+1] if ('-fd' in sys.argv) else base.distMgr.district
base.chatMgr = ChatManager()
base.codeRedemptionMgr = CDRManager()
base.hoodMgr = HoodManager()
base.frdMgr = FriendshipManager()

class SpeechBubble:
    def __init__(self, toon, speech, time = 6):
        self.toon = toon
        self.speech = speech
        self.time = time
        
        self.tag = toon.tag
        if self.tag: self.tag.hide()
        
        box = loader.loadModel("phase_3/models/props/chatbox.bam")
        
        box.setZ(box,1)
        
        box.setBillboardAxis()
        
        box.reparentTo(self.toon._m)
        box.setZ(box,self.toon._m.find('**/def_head').getZ(self.toon._toon))
        
        box.setScale(.5)
        
        getW = lambda i:sum(map(lambda x: max(x,-x),map(lambda x:x.getX(),i.getTightBounds())))
        getH = lambda i:sum(map(lambda x: max(x,-x),map(lambda x:x.getZ(),i.getTightBounds())))
        
        bw = getW(box)
        bh = getH(box)

        if not speech: speech = " "
        text = TextNode('chatbox_text')
        if not isinstance(speech,unicode): speech=unicode(speech,'latin-1')
        text.setWtext(speech)
        text.setFont(BTFont)
        text.setWordwrap(bw/.35)
        textNp = box.find('**/top').attachNewNode(text)
        textNp.setColor(Vec4(0,0,0,1),1)
        textNp.setScale(.6)
        textNp.setDepthOffset(100)
       
        w = text.getWidth()
        h = text.getHeight()
        
        l = text.getNumRows()
        
        textNp.wrtReparentTo(NodePath('void'))
        
        #print w,h,l
        #print bw,bh
        
        if w < bw:
            box.setSx(.2*w/bw)
            
        box.setSz(h/bh + (.075*l))
        
        textNp.wrtReparentTo(box.find('**/top'))
        textNp.setX(box,1)
        l -= 3
        textNp.setZ(box,box.find('**/top').getZ()+(l*.04))
        
        if l == -2:
            textNp.setZ(textNp,-.5)
        
        self.exists = True
        spc = self.toon.data['toontype']
        
        box.setScale(box,2)
        
        if spc:
            MSs(spc,speech).play()
        
        self.frame = box
        taskMgr.doMethodLater(time,self._destroyTask, 'destroyTask')
        
    def _destroyTask(self,task):
        self.frame.hide()
        self.frame.removeNode()
        self.exists = False
        if self.tag: self.tag.show()
        return task.done
        
    def destroy(self):
        self.frame.hide()
        self.tag = None
        self.exists = False

base.cTrav = CollisionTraverser('baseTraveser')

class GameBase(DirectObject):
    def __init__(self):
        base.disableMouse()
        
        if base.appRunner: self.dir = base.appRunner.multifileRoot
        elif hasattr(__builtin__,'isCompiled'):
            self.dir = '' #use absolute paths relative to mf root
            self.isCompiled = True
        else: self.dir = os.path.abspath(os.curdir)
        
        print self.dir
            
        sys.path.append(self.dir)
            
        self.accept("load-chooseatoon-screen",self.loadChooseAToonScr)
        self.accept("init-createatoon",self.enterCreateAToon)
        self.accept("end-createatoon",lambda:self.toonChosen(self.toonId))
        
        self.accept("f9",self.screenshot)
        
        self.curArea = None
        
        self.sounds = {}
        
        exts = ('mp3','wav','ogg')
        for x in (3,3.5,5,0):
            for ext in exts:
                for s in ToonGlobber.glob("phase_"+str(x)+"/audio/sfx/GUI_*."+ext,"phase_"+str(x)+"/audio/sfx"):
                    sf = s.split('/')[-1].split('.')[0]
                    self.sounds[sf] = loader.loadSfx(s)
        
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setIntoCollideMask(BitMask32.allOff())
        self.pickerNode.setFromCollideMask(BitMask32(16))
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        
        self.handler = CollisionHandlerQueue()
        
        self.clickTrav = CollisionTraverser('clickTrav')
        self.clickTrav.addCollider(self.pickerNP, self.handler)
        
        self.clickDict = {}
        self.accept('mouse1',self._click)
        
    def _click(self):
        #print 'click!',

        if not base.mouseWatcherNode.hasMouse(): return
        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
        
        self.clickTrav.traverse(render)

        entriesNumb = self.handler.getNumEntries() 
        #print entriesNumb
        if entriesNumb > 0:
            self.handler.sortEntries()
            for i in xrange(min(1,entriesNumb)): #only one
                e = self.handler.getEntry(i)
                node = e.getIntoNodePath()
                #print i, node
                if node in self.clickDict:
                    self.clickDict[node](e)
            
    def screenshot(self):
        base.win.saveScreenshot("toontownhouse_{0}.jpg".format(str(int(time.time()))))
    
    def findpath(self,path):
        #returns path relative to main.py dir
        p = os.path.join(self.dir,path)
        #if self.isCompiled: p = p.replace('/','\\')
        return p
    
    def loadChooseAToonScr(self):
        self.chooseAtoonScr = ChooseAToonScreen()
        if '-fast' in sys.argv:
            try:
                v = sys.argv[sys.argv.index('-fast')+1]
                self.toonChosen(int(v))
            except Exception as e:
                print 'FastMode: couldn\'t load toon!',e
        
    def toonChosen(self,toonId):
        print 'Toon chosen:',toonId
        self.themeMusic.stop()
        self.chooseAtoonScr.dismiss()
        self.toonId = toonId
        self.toonAvatar = loadToonAvatar(toonId)
        
        self.toonAvatarStream = AvatarStream(self.toonId)
        
        if not self.toonAvatar[0]: return #entered create a toon
        
        #load last area
        messenger.send('loadToon')
        
        def evalArea(a):
            return eval(a.replace('tth.areas.',''))
        
        if "-51" in sys.argv:
            print "It looks like somebody want to know what's inside the Area 51 ! Let's torture him..." #lol
            Teleporter(Area51,"AREA_51").go() #btw, there was a L10N glich here, quite funny... :D
        elif "-fa" in sys.argv:
            print "Forcing an area..."
            Teleporter(evalArea(sys.argv[sys.argv.index('-fa')+1]),'').go()
        elif "-le" in sys.argv:
            print "Going onto Level Editor..."
            Teleporter(AStreet,"AREA_EDITOR").go()
        else:
            print 'Loaded (LA):',self.toonAvatar[2],self.toonAvatar[3]
            Teleporter(evalArea(self.toonAvatar[2]),self.toonAvatar[3]).go()
    
    def enterCreateAToon(self):
        Teleporter(CreateAToon,"CAT",[self.toonId]).go()
    
pversion = "1.8.0"
if '-v' in sys.argv:
	print "Warning: Using deprecated -v option!!" #dafuq

__builtin__.load_buffer = lambda buff: pkl_ld(zlib.decompress(buff.decode('base64')))#,enconding="latin-1")
__builtin__.make_buffer = lambda data: zlib.compress(dumps(data)).encode('base64')
#process key (if comp.)
def _load_buffer(buff): return pkl_ld(zlib.decompress(buff.decode('base64')))
if hasattr(__builtin__,"isCompiled"):
    if not '-k' in sys.argv:
        print 'NO KEY!'
        sys.exit()
        
    key = sys.argv[sys.argv.index('-k')+1]
    rs = _load_buffer(ulib_uo("https://toontownhouse.net/play/keyinfo2.py?key="+key).read())
    if "error" in rs: sys.exit('KEY_ERROR:'+str(rs['error']))
    _USER = rs['u']
    lang = rs['lang']
    __builtin__.glob = glob_copy

else:
    lang = Resolver('l').resolve('en')
    _USER = Resolver('u').resolve('test')

props = WindowProperties()
props.setTitle('Toontown House [{0}]'.format(lang.upper()))
props.setIconFilename("toontown.ico")
props.setCursorFilename("toonmono.cur")
props.setFixedSize('-locksize' in sys.argv)
props.setSize(800,600)
base.win.requestProperties(props)

gamebase = GameBase()

__builtin__.gamebase = gamebase
__builtin__.ToontownHouseError = ToontownHouseError
__builtin__.erroZuado = erroZuado 
__builtin__.L10N = l10n(lang)
__builtin__.pversion = pversion
__builtin__.SpeechBubble = SpeechBubble
__builtin__.BTFont = loader.loadFont('phase_3/models/fonts/ImpressBT.ttf')

base.user = _USER

_server = Resolver('svaddr').resolve('gs-alpha.toontownhouse.net')
print _server,__import__('socket').gethostbyname(_server)
if not '--nonet' in sys.argv: __builtin__.globalBlob = NetworkedBlob(_server,36911,_USER) #Connect to data server
else: __builtin__.globalBlob = Blob('userdata.blob') #local blob
        
def _print(*args): print args
__builtin__._print = _print 

gamebase.ldScr = LoadingScreen()

run()
