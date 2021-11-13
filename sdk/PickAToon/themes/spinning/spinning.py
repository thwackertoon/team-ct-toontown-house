print 'We have %s created toons' % len([x for x in patMgr.heads if x])
       
global ToonButton
class ToonButton(patMgr.gui.DirectButton):
    def __init__(self,name,head,pos):
        patMgr.gui.DirectButton.__init__(self,
                                         relief = None,
                                         pos = pos,
                                         state = patMgr.gui.DGG.NORMAL,
                                         scale = .15,
                                         image = patMgr.loadImage('data/circle.png',True),
                                         )
        self.initialiseoptions(ToonButton)
        self.resetFrameSize()
        
        _size = self.getBounds()
        #print _size;exit()
       
        if head:
            head.reparentTo(self.stateNodePath[0], 20)
            head.instanceTo(self.stateNodePath[1], 20)
            head.instanceTo(self.stateNodePath[2], 20)
            _hsize = patMgr.HeadUtil.getSize(head)
            #print _size,_hsize,_size-_hsize
            #head.setZ((_size-_hsize)/2)
            
        self.resetFrameSize()
        
def getCirclePos(index,total,radius):
    cos = patMgr.modules.math.cos
    sin = patMgr.modules.math.sin
    ang = (360./total*index)*(patMgr.modules.math.pi/180.)
    
    return (radius*cos(ang),0,radius*sin(ang))
    
        
def _makeButton(pos,name,head):
    return ToonButton(name,head,pos)
    
for x in range(6):
    spot = patMgr.spots[x]
    
    pos = getCirclePos(x,6,.8) #(-1,1,.8-x*.3)
        
    if spot.exists: butt = _makeButton(pos,spot.name,patMgr.heads[x])
    else: butt = _makeButton(pos,"Make a Toon",None)
    