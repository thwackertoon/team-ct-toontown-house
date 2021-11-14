from panda3d.core import loadPrcFileData
loadPrcFileData("", "window-type none" )
loadPrcFileData("", "audio-library-name null" ) 

import direct.directbase.DirectStart
from direct.showbase.ShowBaseGlobal import *
from direct.showbase.DirectObject import DirectObject
from direct.distributed.DistributedObject import *
from direct.distributed.DistributedSmoothNode import DistributedSmoothNode
from direct.distributed.ClientRepository import *
from direct.distributed.ServerRepository import *
from direct.gui.OnscreenText import OnscreenText
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
import sys, os, __builtin__, zlib
from cPickle import loads as pkl_ld, dumps

__builtin__.load_buffer = lambda buff: pkl_ld(zlib.decompress(buff.decode('base64')))
__builtin__.make_buffer = lambda data: zlib.decompress(dumps(data)).encode('base64')

from ohs.AccHandler import ConnHandler, AccHandler, ToonHandler

def timeToExit():
    fe = os.path.isfile("_exit_")
    if fe:
        os.path.unlink("_exit_")
        
    return fe

class Server:
    def __init__(self):
        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)
 
        self.conns=[]
        self.debug = 0

        self.tcpSocket = self.cManager.openTCPServerRendezvous(36911,1000)
        
        self.cListener.addConnection(self.tcpSocket)

        taskMgr.add(self.tskListenerPolling,"Poll the connection listener")
        taskMgr.add(self.tskReaderPolling,"Poll the connection reader")

    def tskListenerPolling(self,taskdata):
        if timeToExit(): sys.exit()
        
        if self.debug: print self.cListener.newConnectionAvailable()
        if self.cListener.newConnectionAvailable():
            print 'Conn available!'
            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()
 
            if self.cListener.getNewConnection(rendezvous,netAddress,newConnection):
                newConnection = newConnection.p()
                self.conns.append(newConnection)
                print 'New conn:',newConnection
                self.cReader.addConnection(newConnection) 
        return Task.cont
    
    def _print_conns(self):
        print self.conns
    
    def handleDatagram(self,netDatagram):
        myIterator = PyDatagramIterator(netDatagram)
        cmd,args = myIterator.getString().split('\0',1)
        
        args = map(lambda x: x.decode('base64'),args.split('\0'))
        
        print "Datagram:",cmd,args
    
    def tskReaderPolling(self,taskdata):
        if self.cReader.dataAvailable():
            datagram=NetDatagram()
            if self.cReader.getData(datagram):
                self.handleDatagram(datagram)
        return Task.cont
 
s=Server()

base.accept('x',s._print_conns)

base.accept('w',s.__dict__.__setitem__,['debug',1])
base.accept('w-up',s.__dict__.__setitem__,['debug',0])

run()