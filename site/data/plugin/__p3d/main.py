#coding: latin-1

import sys,os,urllib2,struct,time,hashlib,math,__builtin__ as __btin__
from panda3d.core import *
import direct.directbase.DirectStart
from direct.gui.DirectGui import *
from direct.stdpy.thread import start_new_thread as stn
from base64 import *

subprocess = __import__('subprocess')
print subprocess.__file__

base.win.setClearColor(Vec4(1,1,1,1))

TTH_ROOT = 'C:\\ToontownHouse'
TTH_ROOT_P = '/c/ToontownHouse'

def makeUA():
    stamp = int(time.time())
    dump = b64encode(struct.pack("<I",stamp))
    
    return str(stamp)+".House/"+dump
    
def crawlUrl(url,data=""):
    headers = {'User-Agent' : makeUA()}
    req = urllib2.Request('https://www.toontownhouse.net/play/'+url, data, headers)
    response = urllib2.urlopen(req)
    data = response.read()

    return data

#determine key

if base.appRunner: key = base.appRunner.getToken('key')
else: key = "local"
if not key: key="local"

keydata = crawlUrl('plugin/keyinfo.py',"key="+key).strip().split('\n')

__btin__.ldbar = DirectWaitBar(text="",value=0,pos=(0,0,-.8))
__btin__.ldtext = OnscreenText(text="",pos=(-1,-.15),parent=ldbar,scale=.065,mayChange=1,align=TextNode.ALeft)
__btin__.smallLogo = OnscreenImage(image="logo.jpg",pos=Vec3(1.2,0,1.7),parent=ldbar,scale=.1)

#if error with key, log and exit
if len(keydata) == 1:
    print 'Failed to load! The server said: '+keydata[0]
    ldbar['text'] = 'Failed to load! The server said:'+keydata[0]
    run()
    
#now we know lang, build dict

lang = keydata[1]

_DOWNLOADING,_LOADING,_STARTING,_NOWRUNNING = map(lambda x:x[lang],(
                                                   {
                                                   'en':'Downloading',
                                                   'fr':'Téléchargement',
                                                   'pt':'Baixando',
                                                   },
                                                   {
                                                   'en':'Loading',
                                                   'fr':'Chargement',
                                                   'pt':'Carregando',
                                                   },
                                                   {
                                                   'en':'Starting',
                                                   'fr':'Lancement',
                                                   'pt':'Iniciando',
                                                   },
                                                   {
                                                   'en':'Toontown House is now running! Do not close this page!',
                                                   'fr':'Toontown House est maintenant lancé ! Ne fermez pas cette page !',
                                                   'pt':'Toontown House está rodando agora! Não feche esta página!',
                                                   },
                                                   ))

def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    f = open(f,'rb')
    while True:
        data = f.read(block_size)
        if not data: break
        md5.update(data)
    return md5.hexdigest()
    
def test_md5(file,expected): return md5_for_file(file) == expected

print 'Fetching contents...'
try:
    contents = map(lambda x:x.split('*'),crawlUrl('contents.py').split(','))
    _files = dict(zip(map(lambda x:x[0],contents),map(lambda x:x[1:],contents)))
except:
    _files = {}
    
FILES_TO_DOWN = []
totalSize = 0

def buildEnv():
    if not base.appRunner:
        return os.environ
    
    import _winreg
    _env = {}
    t = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
    try:
        count = 0
        while 1:
            name, value, _type = _winreg.EnumValue(t, count)
            _env[str(name)] = str(value)
            count += 1
    except WindowsError:
        pass
    
    _env["SystemRoot"] = os.environ["SystemRoot"]
    return _env

def runInThread(_exe):
    print _exe
    
    DETACHED_PROCESS = 0x00000008
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    os.chdir(TTH_ROOT)
    env = buildEnv()
    code = subprocess.Popen('"{0}" -k {1}'.format(_exe,key),creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
                            close_fds = True,cwd=TTH_ROOT,env=env).wait()
    
    print "Process exited:",code
    messenger.send("time2exit")

def startGame():
    print 'Running...'
    ldbar.destroy()
    rnText = OnscreenText(text=unicode(_NOWRUNNING,'latin-1'),pos=(0,.8),scale=.135,wordwrap=2/.135)
    rnImage = OnscreenImage(image="logo.png",pos=Vec3(0,0,-.1),scale=.5)
    _exe = "ToontownHouse.exe"
    #if 1: _exe = "ToontownHouse_dev.exe"
    stn(runInThread,[_exe])
    #runInThread(_exe)
    
def _exit():
    print "Exiting..."
    os._exit(0)

for file,info in _files.items():
    if not os.path.isfile(os.path.join(TTH_ROOT,file)) or not test_md5(os.path.join(TTH_ROOT,file),info[0]):
        FILES_TO_DOWN.append(file)
        totalSize += int(info[1])

def convertSize(size):
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   if (s > 0):
       return '%s %s' % (s,size_name[i])
   else:
       return '0B'
        
print 'Must download {0} files!'.format(len(FILES_TO_DOWN))
if FILES_TO_DOWN: print 'Total size:',convertSize(totalSize)

class Downloader(object):
    def __init__(self,files,totalSize):
        self.files = files
        self.ts = totalSize
        self.ds = 0
        self.cs = 0
        
    def download(self): #go to next file
        self.file = self.files[0]
        self.files = self.files[1:]
        self.http = HTTPClient()
        self.channel = self.http.makeChannel(True)
        self.channel.beginGetDocument(DocumentSpec('https://www.toontownhouse.net/play/data/'+self.file))
        self.rf = Ramfile()
        self.channel.downloadToRam(self.rf)
        taskMgr.add(self.downloadTask, 'download')
 
    def downloadTask(self, task):
        if self.channel.run():
            self.cs = self.channel.getBytesDownloaded()
            ldbar['value'] = round(100*float(self.cs+self.ds)/self.ts,2)
            ldtext.setText('{0} Toontown House [{1}] ({2}%)'.format(_DOWNLOADING,self.file,ldbar['value']))
            return task.cont
            
        if not self.channel.isDownloadComplete():
            print "Error downloading file."
            ldtext.setText("Error downloading file.")
            return task.done
            
        #assuming it downloaded everything correctly
        self.cs = self.channel.getBytesDownloaded()
        print 'Finished downloading {0} (size={1}), total={2}'.format(self.file,self.cs,round(100*float(self.cs+self.ds)/self.ts,2))
        self.ds += self.cs
        self.cs = 0
        
        #write to disk
        self.save(os.path.join(TTH_ROOT,self.file))
        
        if self.files: self.download()
        else: messenger.send('downloadDone')
        return task.done
        
    def save(self,path):
        _path = Filename(path).toOsGeneric().split('/')[:-1]
        #print _path
        for i in xrange(1,len(_path)+1):
            _p = '\\'.join(_path[:i])
            if not os.path.isdir(_p):
                #print 'gotta makedir',_p
                try:
                    os.makedirs(_p)
                except:
                    print "FAILED OS.MAKEDIRS!"
        
        with open(path,'wb')as f: f.write(self.rf.getData())

base.accept('downloadDone',startGame)        
base.accept('time2exit',_exit)        
if FILES_TO_DOWN: Downloader(FILES_TO_DOWN,totalSize).download()
else: messenger.send('downloadDone')
run()