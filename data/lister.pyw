from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "window-type none")
from direct.directbase.DirectStart import *
x = loader.loadModel(raw_input("File?"))
print(x.ls())