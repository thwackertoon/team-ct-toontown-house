import sys
version = sys.argv[-1]#raw_input('version >')
from glob import glob
from shutil import copy, copytree as ctree, rmtree
import shutil, py_compile
import os, sys, subprocess

from panda3d.core import *

if 0:
    modelFinder_phasesToLookAt = map(lambda x:'phase_'+str(x),[3,3.5,4,5,5.5,6,7,8,9,10,11,12,13])
    modelFinder_phasesRoot = sys.argv[1] if len(sys.argv)>1 else Filename(raw_input('Where are your phases?')).toOsGeneric()

    modelFinder_absPaths = map(lambda x:os.path.join(modelFinder_phasesRoot,x),modelFinder_phasesToLookAt)

    for x in modelFinder_absPaths:
        getModelPath().appendDirectory(x)

def processBam(file):
    bamFile = BamFile()
    if not bamFile.openRead(file):
        print '\tCould not read bam file %s' % (file)
        return
    if not bamFile.resolve(): raise StandardError, 'Could not resolve bam file %s' % (file)
    node = bamFile.readNode()
    if not node: raise StandardError, 'Not a model file: %s' % (file)

    scanTextures(node, file)

def scanTextures(node, filename):
    for tex in NodePath(node).findAllTextures():
        if not tex.hasFullpath() and tex.hasRamImage():
            tex.clearFilename()
            tex.clearAlphaFilename()

        else:
            if tex.hasFilename():tex.setFilename(addFoundTexture(tex.getFullpath()))
            if tex.hasAlphaFilename():tex.setAlphaFilename(addFoundTexture(tex.getAlphaFullpath()))

    bamFile = BamFile()
    stream = StringStream()
    bamFile.openWrite(stream)
    bamFile.getWriter().setFileTextureMode(bamFile.BTMUnchanged)
    bamFile.writeObject(node)
    bamFile.close()

    # Clean the node out of memory.
    node.removeAllChildren()
    
    with open(filename,'wb') as f: f.write(stream.getData())

def addFoundTexture(filename):
    if 'tth' in str(filename):pass
        #print '\tSkipping texture',filename
        #return filename
        
    filename = Filename(filename)
    filename.makeCanonical()

    # We have to copy the image into the plugin tree somewhere.
    newName = 'maps/' + filename.getBasename()
    
    print '\tAdding texture',newName
    
    try:shutil.copy(filename.toOsSpecific(),newName)
    except: print '\tFailed to copy LOL'

    return newName
    
def _scanTree(file="."):
    if os.path.isfile(file):
        _ext = Filename(file).getExtension()
        if _ext == 'bam':
            print 'Processing BAM',file
            processBam(file)
        
    elif os.path.isdir(file):
        for x in os.listdir(file):
            _scanTree(os.path.join(file, x))

_scanTree("data/models/toons/heads")
