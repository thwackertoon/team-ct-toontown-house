class DistributedFishing(DistributedObject):
 
    def __init__(self):
        self.accept('left', self.reelLeft)
        self.accept('right', self.reelRight)
        self.accept('control', self.castLine)
 
        #self.fishingPanel
        #self.fishingJellybeanJar
        #self.fishingBucket
        #self.fishingExit
 
        self.ttc_fish = [{'Balloon Fish': 'Balloon Fish', 'Hot Air Balloon', 'Red Balloon Fish', 'Weather Balloon Fish'}, 
                     {'Clown Fish': 'Sad Clown Fish', 'Circus Clown Fish'},
                     {'Star Fish': 'Star Fish', 'Five Star Fish', 'Shining Star Fish'},
                     {'Peanut Butter & Jellyfish': 'Peanut Butter & Jellyfish', 'Grape PB&J Fish'},
                     {'Cat Fish': 'Cat Fish'},
                     {'King Crab': 'King Crab'},
                     {'Nurse Shark': 'Nurse Shark'},
                     {'Cutthroat Trout': 'Cutthroat Trout'},
                     'Old Boot']
 
        ddk_fish = [] #Not added yet
 
    def catchFish(self):
        self.jbWorth == 0
        if Hood.zoneId == 1000:
            message = 'you caught a'+random.choice(self.ttc_fish)+'!'
            self.jbWorth += int(random.randint(1,5))
        elif Hood.zoneId == 2000:
            message = 'you caught a'+random.choice(self.ddk_fish)+'!'
            self.jbWorth += int(random.randint(5,10))
 
        self.bucketInt += 1
 
        reelGui.removeNode()
 
        self.tug.finish()
 
    def castLine(self):
        if not hasattr(self, "reel"):
            self.pole = "twig"
 
        self.crank = loader.loadModel('phase_4/models/gui/fishing_crank.bam')
 
        self.progressMeter = DirectWaitBar(text="Distance",value=15,pos=(0,-.7,.90))
        self.fishingCrank = DirectFrame(frameSize=None, pos=(0,-.4,.90), image=self.crank)
 
        self.jellybeanInt -= 1
 
        self.reel = "Left"
 
    def fishPowers(self):
        self.tug = Sequence(Wait(0.5), self.progressMeter['value']-=int(random.randint(3,7)))
        self.tug.loop()
 
    def reelLeft(self):
        if self.reel == "Left":
            self.fishingCrank.hprInterval(0.1, (0,0,360))
            if self.pole == "twig":
                self.progressMeter['value'] += 3
            elif self.pole == "hardwood":
                self.progressMeter['value'] += 5
            elif self.pole == "steel":
                self.progressMeter['value'] += 7
            elif self.pole == "gold":
                self.progressMeter['value'] += 10
 
            if self.progressMeter['value'] <= 100:
                self.catchFish()
 
            self.reel = "Right"
        else: pass
 
    def reelRight(self):
        if self.reel == "Right":
            self.fishingCrank.hprInterval(0.1, (0,0,-360))
            if self.pole == "twig":
                self.progressMeter['value'] += 3
            elif self.pole == "hardwood":
                self.progressMeter['value'] += 5
            elif self.pole == "steel":
                self.progressMeter['value'] += 7
            elif self.pole == "gold":
                self.progressMeter['value'] += 10
 
            if self.progressMeter['value'] <= 100:
                self.catchFish()
 
            self.reel = "Left"
        else: pass