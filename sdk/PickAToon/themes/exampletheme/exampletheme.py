#this one is messed
print 'We have %s created toons' % len([x for x in patMgr.heads if x])
       
global ToonButton
class ToonButton(patMgr.gui.DirectButton):
    def __init__(self,name,head,pos):
        patMgr.gui.DirectButton.__init__(self,
                                         relief = None,
                                         pos = pos,
                                         state = patMgr.gui.DGG.NORMAL,
                                         text = (name.decode('latin-1'),),
                                         text_pos = (1,0,0),
                                         scale = .15,
                                         text_scale = .8,
                                         )
        self.initialiseoptions(ToonButton)
        self.resetFrameSize()
        
        _size = patMgr.HeadUtil.getSize(self)
       
        if head:
            print 'HEAD!'
            head.reparentTo(self.stateNodePath[0], 20)
            head.instanceTo(self.stateNodePath[1], 20)
            head.instanceTo(self.stateNodePath[2], 20)
            
            _hsize = patMgr.HeadUtil.getSize(head)
            print _size,_hsize,_size-_hsize
            #head.setZ((_size-_hsize)/2)
            
        self.resetFrameSize()
        
def _makeButton(pos,name,head):
    print 'mk'
    return ToonButton(name,head,pos)

aspect2d = _makeButton((-10,-10,-10),"",None).getParent()
    
for x in range(6):
    spot = patMgr.spots[x]
    
    pos = (-1,1,.8-x*.3)
        
    if spot.exists: butt = _makeButton(pos,spot.name,patMgr.heads[x])
    else: butt = _makeButton(pos,"Make a Toon",None)
    