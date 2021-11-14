# -*- coding: latin-1 -*-         #
# Autor: Junior and Nacib         #
# Modelos: Disney Toontown Online #
###################################

from pandac.PandaModules import *
import sys, time, signal, os, __builtin__

class fakeL10N:
    def __call__(self,*a): return u"-"
    
__builtin__.L10N = fakeL10N()

def __exit(*args):
    print 'exiting'
    os._exit(0)
    
#signal.signal(signal.CTRL_C_EVENT,os.kill)

USE_DS = 0
if USE_DS:
    from direct.stdpy import threading
else:
    import threading

sys.path.append("../..")

loadPrcFileData("","window-type none")
import direct.directbase.DirectStart

def threaded(f):
    import Queue

    def wrapped_f(q, *args, **kwargs):
        '''this function calls the decorated function and puts the 
        result in a queue'''
        ret = f(*args, **kwargs)
        q.put(ret)

    def wrap(*args, **kwargs):
        '''this is the function returned from the decorator. It fires off
        wrapped_f in a new thread and returns the thread object with
        the result queue attached'''

        q = Queue.Queue()

        t = threading.Thread(target=wrapped_f, args=(q,)+args, kwargs=kwargs)
        t.daemon = True
        t.start()
        t.result_queue = q        
        return t

    return wrap

from direct.distributed.ClientRepository import ClientRepository
from direct.distributed.PyDatagram import PyDatagram as PyDG

from tth.datahnd.DBMsgTypes import *

class MyClientRepository(ClientRepository):
    extraTypes = [100]
                
    def handleMessageType(self, msgType, di):
        #print 'got msg type'
        if msgType in self.extraTypes:
            if msgType == 100:
                self.handleDBOpResult(di)
                
        else:
            ClientRepository.handleMessageType(self, msgType, di)
                
    def __init__(self):
        dcFileNames = []
        
        ClientRepository.__init__(self, dcFileNames = dcFileNames)
        
        self.onConnLoad = False
        self.dbReq = []
        self.dbResult = []
        
        self.kickCode = -1

        self.url = URLSpec('http://127.0.0.1:4003')
        self._connect()
        
        self.alives = 0
        
    def _connect(self):
        self.connect([self.url],
                        successCallback = self.connectSuccess,
                        failureCallback = self.connectFailure)
        
    def connectFailure(self, statusCode, statusString):
        print "Not connected!",statusCode,statusString
        def _cb(a):
            if a == -1:
                sys.exit()
            self._connect()
            
        while True:
            x = raw_input("failed to conn, try again (y/n):").lower()
            if x in ["y","n"]:
                _cb(1 if x=="y" else -1)
                break
        
    def connectSuccess(self):
        print ":CR: Connected!"
        
        self.acceptOnce('createReady', self.createReady)
        self.accept('testAlive', self.ta)
        
    def ta(self):
        print 'I\'m alive!'
        self.alives += 1
                
    def createReady(self): 
        print ':CR: create ready!'
      
    def setDBUser(self,user,task = None):
        if not self.isConnected():
            if task: return task.again
            taskMgr.doMethodLater(1,self.setDBUser,"setuser",extraArgs = [user])
            return

        datagram = PyDG()
        datagram.addUint16(100)
        datagram.addUint32(self.doIdBase)
        
        datagram.addUint8(DB_REQ_Types['setUser'])
        datagram.addString(user)
        
        self.send(datagram)
        self.dbReq = map(lambda x:DB_RES_Types[x],('badUser','userOk'))
        
        if task: return task.done
        
    def handleDBOpResult(self,di):
        status = di.getUint8()
        #print 'handle db status',status
        if not status in self.dbReq:
            self.notify.warning("DB: Recieved unexpected status: "+str(status))
            return
            
        theStr = di.getString()
        self.dbReq = []
        self.dbResult = [status,theStr]
        
        #btw if it's about setUser, handle HERE
        if status in map(lambda x:DB_RES_Types[x],('badUser','userOk')):
            print 'got user res'
            if status == DB_RES_Types['badUser']:
                print 'OMG ITS BAD!'
                
            self.dbResult = []
     
    @threaded
    def _dbRequest(self,dg):
        self.send(dg)
        
        while not self.dbResult:
            self.readerPollOnce()
            
        return self.__clearDbRes()
            
    def __clearDbRes(self):
        x = self.dbResult[:]
        self.dbResult = []
        self.dbReq = []
        return x

base.cr = MyClientRepository() 

@threaded
def everySecond():
    while True:
        print 'sending request...'
        messenger.send('testAlive')
        time.sleep(5)

#@threaded
def __block(t=None):    
    print globalBlob.all()
    print globalBlob.delToon(0)
    print globalBlob.all()
    
    if t: return t.done

import __builtin__
__builtin__.threaded = threaded
    
from NetworkedBlobWithCR import *
globalBlob = NetworkedBlobWithCR(base.cr,"test")
    
#everySecond()

taskMgr.doMethodLater(2,__block,"block")

#messenger.toggleVerbose()
run()
