from panda3d.core import *
import fnmatch as fnm, os

vfs = VirtualFileSystem.getGlobalPtr()
ALL_PHASES = map(lambda x:"phase_"+str(x),(3,3.5,4,5,5.5,6,7,8,9,10,11,12,13))

cdirf = '/c/'+os.path.abspath(os.curdir)[2:].replace('\\','/')[1:]+'/'
def FullScanVFS(dir,sp = None):
        if sp is None: sp = []
        if not dir: return []
        scan = vfs.scanDirectory(Filename(dir))
        if not scan: return []

        for item in scan:
            item = str(item)
            if vfs.isDirectory(Filename(item)):
                if not FullScanVFS(item,sp):
                    sp.append(item)
                
            else: sp.append(item)
         
        return set(map(lambda item:item.replace(cdirf,''),sp))

def glob(data,d="."):
        pattern = data.replace('\\','/')
        return filter(lambda x:fnm.fnmatch(x,pattern),FullScanVFS(d))

def smartScan(kind="*", gender="*", part="*"):
    r = []
    for p in ALL_PHASES:
        r.extend(glob(p+"/models/char/tt_a_chr_dg{0}_{1}_{2}_*.bam".format(kind,gender,part),p+"/models/char"))
        
    return r
    
def test_field(field,needle,item):
    try:
        return item.split('/')[-1].split('_')[field] == needle
    
    except IndexError:
        return False

def filterByGender(items,gender): #generator
    for item in items:
        if test_field(4,gender,item):
            yield item
            
def filterByPart(items,part): #generator
    for item in items:
        if test_field(5,part,item):
            yield item
            
def filterByKind(items,kind): #generator
    for item in items:
        if test_field(3,"dg"+kind,item):
            yield item
    
def loadTorsoAnims(all,gender,kind):
    return set(filterByGender(all,gender)) & set(filterByKind(all,kind)) & set(filterByPart(all,"torso"))
    
def loadLegsAnims(all,gender,kind):
    return set(filterByGender(all,gender)) & set(filterByKind(all,kind)) & set(filterByPart(all,"legs"))