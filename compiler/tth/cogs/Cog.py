from panda3d.core import *

from direct.actor.Actor import Actor
from direct.gui.DirectGui import *

from tth.book.DisguisePage import getCogName, suitDeptFullnames
from CogAvatarPanel import CogAvatarPanel
from CogDNA import CogDNA
import CogHead, CogGlobals

SCALE = .8

CogFont = None
def getCogFont():
    global CogFont
    if not CogFont:
        CogFont = loader.loadFont('phase_3/models/fonts/vtRemingtonPortable.ttf')
        
    return CogFont

class Cog(Actor):
    
    always4 = ["slip-forward","slip-backward","tug-o-war","flailing"]

    def __init__(self,dna = None):
        Actor.__init__(self)
        
        self.cnp = NodePath('dummy')
        self.inited = False
        self.healthBar = None
        self.healthCondition = 0
        
        self.curHp = 0
        self.maxHp = 200
        
        self.dtPanel = None
        
        self.dna = CogDNA()
        if dna: self.reload(dna)
        
    def reload(self,dna):
        self.dna.makeFrom(dna)
        
        self.__destroy()
        
        self.inited = True
        self.maxHp = CogGlobals.getHpByLevel(self.dna.level)
        
        oldHead = self.find('**/cogHead*')
        if oldHead: oldHead.removeNode()
        self.cnp.removeNode()
        
        dept, index = self.dna.dept, self.dna.leader
        
        #load body
        self.bodyType = CogGlobals.getBodyType(dept, index)
        _model,_phase = CogGlobals.ModelDict[self.bodyType][0]+'mod',3.5
        
        if self.dna.isSkel: _model,_phase = "/models/char/cog"+self.bodyType.upper()+"_robot-zero",5
        
        self.bodyModel = "phase_{0}{1}".format(_phase,_model)
        anims = self.__getAnims(dept, index, self.bodyType)
        
        self.loadModel(self.bodyModel)
        self.loadAnims(anims)

        self.makeHead(dept, index, CogGlobals.getHeadColor(dept, index))
        
        #loop neutral
        self.loop('neutral')
        
        self.setWaiter(self.dna.isWaiter)
        self.dialog = self.__loadDialog(self.dna.isSkel)
        
        self.scale,self.height = CogGlobals.ScalesAndHeights[dept][index]
        
        self.getGeomNode().setScale(self.scale * SCALE)
        self.setHeight(self.height * SCALE) #actually scale already sets height
        
        self.leftHand = self.find('**/joint_Lhold')
        self.rightHand = self.find('**/joint_Rhold')
        self.shadowJoint = self.find('**/joint_shadow')
        self.nametagJoint = self.find('**/joint_nameTag')
        
        self.makeNameTag()
        self.makeColl()
        self.makeTie()
        self.makeMedallion()
        
    def setHeight(self,newH):      
        points = map(lambda x: x[2],self.getTightBounds())
        curH = points[0]-points[1]
        
        curH = max(curH,-curH)
        
        self.getGeomNode().setSz(self.getGeomNode().getSz()*newH/curH)
        
    def makeNameTag(self):
        font = getCogFont()
        
        l10nPrefix = ""
        if self.dna.lives > 1: l10nPrefix = "_VER"

        name = getCogName(self.dna.dept*8+self.dna.leader)
        if self.dna.isSkel: name = L10N('COG_SKEL')
        
        deptName = suitDeptFullnames[('c','l','m','s')[self.dna.dept]]
        args = (name,deptName,self.dna.level)
        
        if self.dna.lives > 1: args += (self.dna.lives,)
        
        text = L10N('COG_TAG'+l10nPrefix).replace("\\n","\n") % args
        
        self.nameTag = OnscreenText(decal=True,text=text,scale=.4,font=font,fg=(0,0,0,1),bg=(1,1,1,.3))
        self.nameTag.reparentTo(self.exposeJoint(None,"modelRoot","joint_head"))
        self.nameTag.setBillboardAxis()
        self.nameTag.setWordwrap(3.2/.4)
        
        x = 3.5 #self.nameTag.node().getNumLines() * 3

        if not self.dna.isSkel:
            points = map(lambda x: x[2],self.find('**/cogHead*').getTightBounds())
            h2 = points[0]-points[1]
            h2 = max(h2,-h2)
            
        else: h2 = .5

        self.nameTag.setZ(h2+x/1.75)
 
    def __getAnims(self, dept, index, bodyType):
        ba = self.__formatBasicAnims(CogGlobals.BasicAnims,bodyType)
        
        return self.__formatAnims(tuple(ba)+CogGlobals.SpecificAnims[dept][index], bodyType)
        
    def __formatAnims(self,anims,bodyType):
        a = {}
        for model,phase in anims: a[model] = 'phase_'+str(phase)+'/models/char/suit'+bodyType.upper()+'-'+model
        return a
        
    def __formatBasicAnims(self,anims,bodyType):
        a = []
        for anim in anims:
            p = (4,3.5)[bodyType == "c" and anim not in self.always4]
            if anim not in ["walk","neutral","flailing","lose","pie-small","squirt-small"]+self.always4: p = 5
            a.append((anim,p))
            
        return a
        
    def setCogClothes(self, dept = None, handColor = None):
        if self.dna.isSkel: return
    
        int2str = ['c','l','m','s','waiter_m']
        
        if not dept:
            dept = self.dna.dept
            
        if type(dept) is int:
            try: dept = int2str[dept]
            except: raise ToontownHouseError("Cog 0x000: BAD DEPT, UNABLE TO TEXTURE!")
        
        assert dept in int2str

        t = {"sleeve":"arms","blazer":"torso","leg":"legs"}
        for i in t.keys():
            _tex = loader.loadTexture("phase_3.5/maps/{0}_{1}.jpg".format(dept,i))
            _tex.setMinfilter(Texture.FTLinearMipmapLinear)
            _tex.setMagfilter(Texture.FTLinear)
            self.find("**/"+t[i]).setTexture(_tex,1)

        if handColor: self.find('**/hands').setColor(handColor)
        
    def setWaiter(self,flag = False):
        if flag: self.setCogClothes('waiter_m')
        else: self.setCogClothes(handColor = CogGlobals.getHandColor(self.dna.dept,self.dna.leader))
        
    def makeHead(self,dept,index,color = None):
        _head = CogHead.CogHead(dept, index)
        
        if not self.dna.isSkel:
            self.instance(_head, 'modelRoot', 'joint_head')
            if color:
                _head.setColor(color,1)
            
        _head.removeNode()
                
    def __loadDialog(self,skel=False):
        SuitDialogArray = []
        loadPath = 'phase_3.5/audio/dial/COG_VO_'
        if skel: loadPath = 'phase_5/audio/sfx/Skel_COG_VO_'
        SuitDialogFiles = ['grunt','murmur','statement','question']
        for file in SuitDialogFiles:
            SuitDialogArray.append(base.loadSfx(loadPath + file + '.mp3'))
            
        return SuitDialogArray
    
    def __destroy(self):
        if not self.inited: return
        self.nameTag.removeNode()  
        self.removePart("modelRoot")
        
        if self.dtPanel: self.dtPanel.cleanup()

    def makeColl(self):        
        bounds = map(lambda x:max(x,-x),map(lambda x:x[0]-x[1],zip(*self.getTightBounds())))
        
        cs = CollisionSphere(0,0,0,.9)
        cn = CollisionNode(self.getName()+'_cnode')
        cn.addSolid(cs)
        cn.setCollideMask(17)
        
        self.cnp = self.attachNewNode(cn)
        self.cnp.setScale(*bounds)
        
        #self.cnp.show()      
        gamebase.clickDict[self.cnp] = self.__click

    def __click(self,entry):
        self.dtPanel = CogAvatarPanel(self)
        
    def makeTie(self):
        dept = self.dna.dept
        tie = self.find('**/tie')
        if tie.isEmpty():
            #print 'Cog 0x001 (WARNING): skelecog has no tie!'
            return
            
        n = ('boss','legal','money','sales')[dept]
        tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_'+n+'.jpg')
        tieTex.setMinfilter(Texture.FTLinearMipmapLinear)
        tieTex.setMagfilter(Texture.FTLinear)
        tie.setTexture(tieTex, 1)

    def makeMedallion(self):
        icons = loader.loadModel('phase_3/models/gui/cog_icons')
        dept = self.dna.dept
        chestNull = self.find('**/joint_attachMeter')
        
        n = ('CorpIcon','LegalIcon','MoneyIcon','SalesIcon')[dept]
        
        self.corpMedallion = icons.find('**/'+n).copyTo(chestNull)
        self.corpMedallion.setPosHprScale(0.02, 0.05, 0.04, 180.0, 0.0, 0.0, 0.51, 0.51, 0.51)
        self.corpMedallion.setColor(CogGlobals.getMedallionColor(dept,self.dna.leader))
        icons.removeNode()
