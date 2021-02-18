class Nation:
    def __init__(self, name, influence, leaderUser,numberOfChannels):
        self.name = name
        self.influence = influence
        self.leaderUser = leaderUser
        self.representatives = []
        self.numberOfChannels = numberOfChannels
        self.citizens = []
        self.armySize = 0
        self.money = 0
        #may not use illigal citizens rn
        self.illegalCitizens=[]
    def addInfluence(self,amount=1):
        self.influence+=amount
    def addRepresentative(self,userName):
        self.representatives.append(userName)
    def removeRepresentative(self,username):
        representativesList = self.representatives
        for i in range(len(representativesList)-1):
            if representativesList[i]==username:
                representativesList.pop(i)
    def UpdateNation(self,name,influence,numberOfChannels):
        self.name=name
        self.influence=influence
        self.numberOfChannels=numberOfChannels

    def removeCitizen(self,name):
        membersList = self.citizens
        for i in range(len(membersList)-1):
            if membersList[i]==name:
                membersList.pop(i)
    def addCitizen(self,name):
        self.citizens.append(name)
    def changeLeader(self,name):
        self.leaderUser=name

def deleteNation(nat):
    del nat


#//Format:
#Nation: name, influence, leaderName, numberOfChannels|

#//Representatives and users are going to go off of roles
#

def readRecovery(file):
    listOfNations = []
    for line in file.split('|'):
        if len(line)>0:
            rest1 = line.split(':')[1]
            name = rest1.split(',')[0]
            influence = int(rest1.split(',')[1])
            leaderName = rest1.split(',')[2]
            numberOfChannels = int(rest1.split(',')[3])
            money = rest1.split(',')[4]
            nation = Nation(name,influence,leaderName,numberOfChannels)
            nation.money=money

            listOfNations.append(nation)
    return listOfNations

def printRecovery(nations):
    final_message = ""
    for nation in nations:
        name = nation.name
        influence = nation.influence
        leader = nation.leaderUser
        channelCount = nation.numberOfChannels

        money = nation.money
        final_message += "{0},{1},{2},{3},{4}|".format(name,influence,leader,channelCount,money)
    return final_message


def debugNationsList(nationsList):
    for nation in nationsList:
        print(nation.name)