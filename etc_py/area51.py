from direct.directbase.DirectStart import *
from panda3d.core import *
from direct.gui.DirectGui import *

for s in DGG.FrameStyleDict.keys():
    pos = .9-DGG.FrameStyleDict.keys().index(s)*.2
    DirectEntry(scale=.05,numLines = 1,focus=1,relief = DGG.FrameStyleDict[s],initialText=s,pos=(0,0,pos))
    
run()