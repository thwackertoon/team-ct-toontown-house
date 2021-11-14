"""
Toontown House Compiler (TTHC) is a tool made by Nacib to generate relatively safe EXEs
from Panda code. The basic process is:

- Copy the files.
- Obfuscate all .py files.
- Generate P3D.
- Use Pdeploy to get a standalone.

"""
import sys
version = sys.argv[-1]#raw_input('version >')
from glob import glob
from shutil import copy, copytree as ctree, rmtree
import shutil, py_compile
import os, sys, subprocess
import zlib, cPickle as pkl
from zipfile import ZipFile as zf

from panda3d.core import *

_build_dir = 'built/'+version
getModelPath().appendDirectory(_build_dir)
if not os.path.isdir(_build_dir): os.makedirs(_build_dir)

rmtmps = lambda file: file.replace('./tmp/','').replace('\\','/')
rmtmpszip = lambda file: file.replace(_build_dir+'\\','__data__/').replace(_build_dir+'/','__data__/')

ptj = os.path.join

_files_to_copy = ["main.py","toonmono*","*.ico"] #accepts wildcards
_dirs_to_copy = ["tth"] #also accepts wildcards

_to_include_at_the_end = ['../toonmono.cur','../toontown.ico']

if '--nodata' in sys.argv: _dirs_to_copy.remove('data')

_tth_root = ".." #relative to here
_tmp_dir = os.path.join(os.curdir,_build_dir)

def lct(src, dst, rmdir={}):
    if (os.path.isdir(src)):
        if (rmdir.has_key(os.path.basename(src))):
            return
        if (not os.path.isdir(dst)): os.mkdir(dst)
        for x in os.listdir(src):
            lct(os.path.join(src,x), os.path.join(dst,x), rmdir)
    else:
        if os.path.exists(dst):
            if os.path.getmtime(src) > os.path.getmtime(dst):
                print 'Updating...',src,'->',dst
                shutil.copyfile(src, dst)
            else: return
        else: shutil.copyfile(src, dst)

def remove_by_ext(file,*exts):
    if os.path.isfile(file):
        if file.split('.')[-1] in exts:
            print 'Removing',file
            os.unlink(file)
            
    elif os.path.isdir(file):
        for x in os.listdir(file):
            remove_by_ext(os.path.join(file, x),*exts)

def remove_ccs(file,*exts): #conflict copies
    if os.path.isfile(file):
        if ' (' in file:
            print 'Removing COPY',file
            os.unlink(file)
            
    elif os.path.isdir(file):
        for x in os.listdir(file):
            remove_by_ext(os.path.join(file, x),*exts)
            
if not '--nocp' in sys.argv:
    for _file in _files_to_copy:
        for globbed in glob(ptj(_tth_root,_file)):
            dt = ptj(_tmp_dir,globbed.replace('..\\',''))
            print 'Copying',globbed,'to',dt
            copy(globbed,dt)
        
    for _file in _dirs_to_copy:
        for globbed in glob(ptj(_tth_root,_file)):
            dt = ptj(_tmp_dir,globbed.replace('..\\',''))
            print 'Copying tree',globbed,'to',dt
            #try: rmtree(dt)
            #except: pass
            try: lct(globbed,dt)
            except: pass #dont ever overwrite
    
    remove_by_ext(_tmp_dir+"/tth",'bat','pyw','pyc','pyo')
    remove_ccs(_tmp_dir+"/tth")

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
   
def py2pyc(file):
    print "Compiling python "+file
    pyc = file[:-3]+'.pyc'
    pyo = file[:-3]+'.pyo'
    if (os.path.exists(pyc)): os.unlink(pyc)
    if (os.path.exists(pyo)): os.unlink(pyo)
    try: py_compile.compile(file)
    except Exception as e: print ("Cannot compile "+str(e))
    os.unlink(file)

def CompileFiles(file):
    if (os.path.isfile(file)):
        if (file.endswith(".py")):
            py2pyc(file)
        else: pass
    elif (os.path.isdir(file)):
        for x in os.listdir(file):
            CompileFiles(os.path.join(file, x))
            
if not "--norecm" in sys.argv:
    print 'Generating toontownhouse.tth...'
    _key = "tthc.is.awesome!"
    
    def _run(cmd):
        print cmd
        subprocess.Popen(cmd,stdout=sys.stdout,stderr=sys.stderr,shell=True).wait()
        
    def _make_zip(zfile,files,_f=None):
        if not _f: _f = zf(zfile,'w')
        for file in files:
            #print 'TEST',file
            if os.path.isfile(file):
                if '-zpv' in sys.argv: print 'ZIP: Adding',file,rmtmpszip(file)
                _f.write(file,rmtmpszip(file))
            
            elif os.path.isdir(file):
                if '-zpv2' in sys.argv: print 'ZIP: is a dir!'
                for x in os.listdir(file):
                    _make_zip(None,[os.path.join(file, x)],_f)
                    
        if zfile:_f.close()
        
    def _process_zip(_zip):
        with open(_zip,'rb') as f:
            _data = f.read()
        _data = rc4(_data[::-1],_key)
        with open(_zip,'wb') as f:
            f.write(_data)
            
    print 'Compiling PYs...'
    CompileFiles(_build_dir)
     
    _files = glob(_build_dir+'/*.*')
    _files += (_build_dir+'/tth',)
    rmvs = map(lambda x:x.replace('0.0.1a',version),['built/0.0.1a\\data.tth', 'built/0.0.1a\\toonmono.cur','built/0.0.1a\\toontown.ico','built/0.0.1a\\toontownhouse.tth'])
    for r in rmvs:
        try: _files.remove(r)
        except: print r,'not in files!'
    print _files
    _make_zip(_build_dir+'/toontownhouse.tth',_files)
    print 'Processing ZIP...'
    _process_zip(_build_dir+'/toontownhouse.tth')

for f in _to_include_at_the_end: copy(f,os.path.join(_build_dir,f.rsplit('/',1)[-1]))