from HoodUtil import makeDoor
from CogMaker import CogMaker

cogPoints = (
                    (251,106,-68.4),
                    (170,81,-68.4),
                    (107,39,-68.4),
                    (24,78,-68.4),
                    (-55,103,-68.4),
                    (-32,17,-68.4),
                    (41,-9,-68.4),
                    (135,6,-68.4),
                    (222,44,-68.4),
                    (-10,-26,-68.4),
                    (-16,-76,-68.4),
                    (23,-122,-68.4),
                    (-26,-163,-68.4),
                    (20,-180,-68.4),
                    (75,-151,-68.4),
                    (74,-83,-68.4),
                    (148,-82,-68.4),
                    (206,-67,-68.4),
                    (257,-14,-68.4),
                    (232,24,-68.4),
                    (155,-8,-68.4),
                    (96,-39,-68.4),
                    (29,-37,-68.4),
                    (188,-100,-68.4),
                    (207,-173,-68.4),
                    (137,-243,-68.4),
                    (87,-179,-68.4),
                    (115,-101,-68.4),
                    (71,-180,-68.4),
                    (22,-197,-68.4),
                    (-11,-219,-68.4),
                    (13,-262,-68.4),
                    (-16,-306,-68.4),
                    (-30,-345,-68.4),
                    (-56,-378,-68.4),
                    (-68,-435,-68.4),
                    (-21,-474,-68.4),
                    (15,-448,-68.4),
                    (23,-371,-68.4),
                    (41,-280,-68.4),
                    (61,-219,-68.4),
                    (172,-247,-68.4),
                    (241,-315,-68.4),
                    (264,-398,-68.4),
                    (222,-452,-68.4),
                    (159,-362,-68.4),
                    (88,-314,-68.4),
                    (85,-247,-68.4),
                    (150,-258,-68.4)
                )
     
cogWalkDur = 465

class LawbotHQManager:
    def __init__(self,distMgr):
        self.distMgr = distMgr
        self.door_DALobby = makeDoor(base.air,distMgr.get(9000),"door_0")
        
        self.cogMaker = CogMaker(self,distMgr.get(9000),(0,1,0,0),30,(8,10))
        self.cogMaker.setPoints(cogPoints)
        self.cogMaker.time = cogWalkDur