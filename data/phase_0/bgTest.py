import direct.directbase.DirectStart
from direct.gui.DirectGui import *

from panda3d.core import *

tex = loader.loadTexture("background.jpg")
ts = TextureStage('ts')
ts.setMode(TextureStage.MBlend)
ts.setColor(Vec4(1,1,1,1))

cm = CardMaker('OnscreenImage')
cm.setFrame(-1, 1, -1, 1)

self = NodePath('img')
self.assign(render2d.attachNewNode(cm.generate(), 0))
self.setTexture(ts,tex)

finalColor = Vec4(1,0,0,1)
self.setColor(finalColor,1)

run()