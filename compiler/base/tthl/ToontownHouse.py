# based on Panda's VFSImporter.py
import sys

class Logger(object):
        def __init__(self, filename="Default.log"):
            self.terminal = sys.stdout
            self.log = open(filename, "a")

        def write(self, message):
            try: self.terminal.write(message)
            except: pass
            self.log.write(message)

print 'Setting up log...'
#if not os.path.isdir('logs'): os.makedirs("logs")
#sys.stdout = Logger("logs/tth_{0}.log".format(datetime.datetime.now().strftime('%d%b%y_%H%M%S')))
#sys.stderr = sys.stdout

sys.path = ['.','..\\dlls','./dlls']

__import__('imp').load_dynamic("libpandaexpress","dlls/libpandaexpress.dll")

from libpandaexpress import VirtualFileSystem, Filename, Multifile
vfs = VirtualFileSystem.getGlobalPtr()

pdmf = Multifile()
pdmf.openRead("pythondata.tth")
print pdmf
print 'Mount python data:',vfs.mount(pdmf,".",0)

import _vfsimporter
__import__('VFSImporter').register()

import os

#preload PYDs
for x in os.listdir('./dlls'):
    if x.endswith('.pyd'):
        print 'preloading',x
        __import__(x[:-4],globals(),locals())

cdirf = '/c/'+str(Filename(os.path.abspath(os.curdir)))[2:].replace('\\','/')[1:]+'/'
def FullScanVFS(dir,sp = None):
        if sp is None: sp = []
        if not dir: return []
        scan = vfs.scanDirectory(Filename(dir))
        if not scan: return []
        
        for item in scan:
            item = str(item)
            if vfs.isDirectory(Filename(dir)):
                if not FullScanVFS(item,sp):
                    sp.append(item)
                
            else:
                sp.append(item)
         
        return map(lambda item:item.replace(cdirf,''),sp)

#vfs.lsAll(Filename("."))

import new,os,marshal,imp,struct,types,sys,datetime,__builtin__
from cStringIO import StringIO
from zipfile import ZipFile

#print os.environ
#print sys.path

# Possible file types.
FTPythonSource = 0
FTPythonCompiled = 1
FTExtensionModule = 2
FTFrozenModule = 3

compiledExtensions = [ 'pyc', 'pyo' ]
if not __debug__: compiledExtensions = [ 'pyo', 'pyc' ]
    
_key = "tthc.is.awesome!"
#__builtin__._tthm = None
#_tthloader_verbose = 0

def rc4(data, key):
        j = 0L
        s = range(256L)
        for i in range(256L):
            j = (j + s[i] + ord(key[i % len(key)])) % 256L
            (s[i], s[j]) = (s[j], s[i])
        (j, i) = (0L, 0L)
        results = []
        for c in data:
            j = (j + 1L) % 256L
            i = (i + s[j]) % 256L
            (s[j], s[i]) = (s[i], s[j])
            results.append(chr(ord(c) ^ s[(s[j] + s[i]) % 256L]))
        return ''.join(results)

def _read_zip(_zip):
        with open(_zip,'rb') as f:
            _data = f.read()
        _data = rc4(_data,_key)[::-1]
        SIO = StringIO()
        SIO.write(_data)
        return ZipFile(SIO)
        
class TTHMount:
    def __init__(self,file):
        self._fz = _read_zip(file)
        #self._fzLib = ZipFile(StringIO(),'r')

    def dump(self):
        print "DUMPING TTH INFO..."
        print "Subfiles:"
        for f in self._fz.namelist(): print '\t',f
        
    def exists(self,file,il=0):
        if il: return self.existsLib(file)
        prefix = '__data__/'
        if isinstance(file,list): file=''.join(file)
        file = prefix+(file.replace('\\','/').replace('./',''))
        if _tthloader_verbose:print '[TTHMount] looking for', file, file in self._fz.namelist()
        return file in self._fz.namelist()
        
    def readFile(self,file,il=0):
        if il: return self.readFileLib(file)
        prefix = '__data__/'
        file = prefix+(file.replace('\\','/').replace('./',''))
        return self._fz.read(file)
        
    def existsLib(self,file):
        if isinstance(file,list): file=''.join(file)
        file = file.replace('\\','/').replace('./','')
        if _tthloader_verbose:print '[TTHMount:Lib] looking for', file
        return vfs.exists(file)
        
    def readFileLib(self,file):
        file = file.replace('\\','/').replace('./','')
        return vfs.readFile(file,True)
        
class TTHImporter:
    """ This class serves as a Python importer to support loading
    Python .py and .pyc/.pyo files from a file compiled by the TTHC,
    which allows loading Python source files from .tth files
    (among other places). """

    def __init__(self, path):
        self.dir_path = path
        __list = FullScanVFS(".")
        self.problematics = map(lambda x:x.split('.',1)[0].replace('/','.'),__list) #by default include all
    
    def find_module(self, fullname, path = None):
        
        #_tthm.dump()
        if path is None:
            dir_path = self.dir_path
        else:
            dir_path = path
        
        if _tthloader_verbose:print 'Looking for',fullname,'path=',path
                
        isLib = fullname.split('.')[0] in ['direct','pandac','panda3d','encodings','unittest','unicodedata'] or any([s in fullname.split('.') for s in self.problematics])
        if _tthloader_verbose:print '[TTHMount:Importer] Info.IsLib {0}:{1}'.format(fullname,isLib)
        
        basename = fullname.replace('.','/')#fullname.split('.')[-1]
        path = basename #os.path.join(dir_path, basename)

        # First, look for Python files.
        filename = basename+'.py'
        if _tthm.exists(filename,isLib):
            return TTHLoader(dir_path, filename, FTPythonSource, isLib)

        # If there's no .py file, but there's a .pyc file, load that anyway.
        for ext in compiledExtensions:
            filename = basename+'.'+ext
            if _tthm.exists(filename,isLib):
                return TTHLoader(dir_path, filename, FTPythonCompiled, isLib)

        # Finally, consider a package, i.e. a directory containing __init__.py.
        filename = os.path.join(path, '__init__.py')
        #print path,'FN:',filename
        if _tthm.exists(filename,isLib):
            return TTHLoader(dir_path, filename, FTPythonSource, isLib, packagePath = path)
        for ext in compiledExtensions:
            filename = os.path.join(path, '__init__.' + ext)
            if _tthm.exists(filename,isLib):
                return TTHLoader(dir_path, filename, FTPythonCompiled, isLib, packagePath = path)

        return None

class TTHLoader:
    """ The second part of TTHImporter, this is created for a
    particular .py file or directory. """
    
    def __init__(self, dir_path, filename, fileType, isLib = False, desc = None, packagePath = None):
        self.dir_path = dir_path
        self.timestamp = None
        self.filename = filename
        self._filename = ""
        self.fileType = fileType
        self.desc = desc
        self.packagePath = packagePath
        self.isLib = isLib
    
    def load_module(self, fullname, loadingShared = False):
        
        self._filename = fullname
        if _tthloader_verbose:print '[TTHMount:Loader] Loading',fullname
        code = self._loadPyc(_tthm.readFile(self.filename,self.isLib))
        #print code
        if not code:
            raise ImportError, 'No Python code in %s' % (fullname)
        
        mod = sys.modules.setdefault(fullname, new.module(fullname))
        mod.__file__ = self.filename
        mod.__loader__ = self
        if self.packagePath:
            mod.__path__ = [self.packagePath]

        exec code in mod.__dict__
        return mod

    def getdata(self, path):
        path = os.path.join(self.dir_path, path)
        return _tthm.readFile(path)

    def is_package(self, fullname):
        return bool(self.packagePath)

    def get_code(self, fullname):
        return self._read_code()

    def get_source(self, fullname):
        return None #self._read_source()

    def get_filename(self, fullname):
        return self.filename
        
    def _loadPyc(self, data):
        """ Reads and returns the marshal data from a .pyc file.
        Raises ValueError if there is a problem. """
        
        code = None
        if data[:4] == imp.get_magic():
            t = struct.unpack('<I', data[4:8])[0]
            if 1:
                code = marshal.loads(data[8:])
            else:
                raise ValueError, 'Failed to load!'
        else:
            if _tthloader_verbose:print '[TTHMount:LoadPYC] Invalid pyc data! Returning compiled version of data...'
            code = __builtin__.compile(data,'','exec')
            
        return code
        
_registered = False
def mount(_f,verbose=False):
    """ Register the TTHLoader on the path_hooks, if it has not
    already been registered, so that future Python import statements
    will vector through here (and therefore will take advantage of
    TTH VFS). """

    global _registered
    if not _registered:
        _registered = True
        sys.path_hooks.insert(0, TTHImporter)
        sys.meta_path.insert(0, TTHImporter(''))
        
        __builtin__._tthm = TTHMount(_f)
        __builtin__._tthloader_verbose = verbose
        
        # Blow away the importer cache, so we'll come back through the
        # TTHLoader for every folder in the future, even those
        # folders that previously were loaded directly.
        sys.path_importer_cache = {}

print 'Mounting TTH...'
_tth_to_mount = 'toontownhouse.tth'
mount(_tth_to_mount,'-tthmv' in sys.argv)

print 'Init modules...'
from panda3d.core import VirtualFileSystem as VFS, Filename, Multifile

__builtin__.isCompiled = True
        
print 'Hooking glob...'
        
from direct.stdpy.file import open as ds_open, file as ds_file
#from direct.stdpy import glob as ds_glob
__builtin__.open = ds_open
__builtin__.file = ds_file

import fnmatch as fnm
class ds_glob:
    def _recurse_dir(self,dir,sp = None):
        if sp is None: sp = []
        if not dir: return []
        scan = vfs.scanDirectory(Filename(dir))
        if not scan: return []
        
        for item in scan:
            item = str(item)
            if vfs.isDirectory(Filename(dir)):
                if not self._recurse_dir(item,sp):
                    sp.append(item)
                
            else:
                sp.append(item)
        
        return sp
        
    def _ef(self):
        x = os.path.abspath(os.curdir)
        return '/'+x[0].lower()+x[2:]
        
    def glob(self,data):
        _dir = '/'.join('/'.join(data.split('\\')).split('/')[:-1]).replace(self._ef(),'')
        pattern = '/'.join(data.split('\\')).split('/')[-1]
        
        #print _dir,pattern
        rs = []
    
        for item in self._recurse_dir(_dir):
            item = str(item)
            #print item,fnm.fnmatch(item.replace('\\','/').split('/')[-1],pattern)
            if fnm.fnmatch(item.replace('\\','/').split('/')[-1],pattern): rs.append(item.replace(self._ef(),''))
            
        return rs

__builtin__.glob = ds_glob()
__builtin__.glob_copy = __builtin__.glob

print 'Running!'
print

#print 'G:',glob.glob("data/models/toons/dgl/shorts/*.bam")

import main