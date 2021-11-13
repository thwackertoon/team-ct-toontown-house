#AI Chat Bot
#Coded by FerverExtreme (Junior) - 02/12/14

import BotEN as lang #Load default language

class Bot:
    def __init__(self,alreadyCome=False):
        self.dataAwsner = lang.data
        if not alreadyCome: print(lang.helpEnt)
        else: print(lang.yourQuest)
        self.awsner = raw_input()
        da = self.dataAwsner
        if da[0] in self.awsner:
            print(lang.registerManutence)
            print(lang.otherQuest)
            yon = raw_input()
            if "yes" in yon: self.__init__(True)
            else:
              print(lang.bye)
              return
        elif da[1] in self.awsner:
            print(lang.cantLogin)
            print(lang.otherQuest)
            yon = raw_input()
            if "yes" in yon: self.__init__(True)
            else:
              print(lang.bye)
              return
        elif da[2] in self.awsner:
            print(lang.cantDownPlay)
            print(lang.otherQuest)
            yon = raw_input()
            if "yes" in yon: self.__init__(True)
            else:
              print(lang.bye)
              return
        elif da[3] in self.awsner:
            print(lang.cantDownPlay)
            print(lang.otherQuest)
            yon = raw_input()
            if "yes" in yon: self.__init__(True)
            else:
              print(lang.bye)
              return
        elif da[4] in self.awsner:
            print(lang.noReleaseDate)
            print(lang.otherQuest)
            yon = raw_input()
            if "yes" in yon: self.__init__(True)
            else:
              print(lang.bye)
              return
        elif da[5] in self.awsner:
            print(lang.noReleaseDate)
            print(lang.otherQuest)
            yon = raw_input()
            if "yes" in yon: self.__init__(True)
            else:
              print(lang.bye)
              return

        else:
            print(lang.sorryICU)
            self.__init__(True)


        return






Bot(False)
