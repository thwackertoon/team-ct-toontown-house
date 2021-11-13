dirs = ["skelecogHQ","neighboorhoods","modules"]

from panda3d.core import *
#loadPrcFileData("","window-type none")
getModelPath().appendDirectory("../../../..")
getModelPath().appendDirectory("../../..")
getModelPath().appendDirectory("../..")
getModelPath().appendDirectory("../")
import direct.directbase.DirectStart

def process(dir,egg,bam):
    np = loader.loadModel(dir+'/'+egg)
    np.reparentTo(render)

import glob
for x in dirs:
    for y in glob.glob(x+'/*.egg'):
        y = y.split('\\')[-1]
        bam = y.split('.')[0]+'.bam'
        
        print y,bam
        process(x,y,bam)
        
run()