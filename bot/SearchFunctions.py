import discord
def roleInList(roleName, listOfRoles):
    for r in listOfRoles:
        if roleName==r.name:
            return True
    return False

def roleInDict(roleName,dict):
    for role in dict:
        if role==roleName:
            return True
    return False


def isPartOfCountry(roles,nations):
    for role in roles:
        for nation in nations:
            if role.name == nation.name:
                return True
    return False

#used to find the nation name a person is a part of
def findNationName(roles,nations):
    for role in roles:
        for nation in nations:
            if role.name==nation.name:
                return nation.name
    return ""
#used to find the nation object
def findNationByName(name,nations):
    for nation in nations:
        if nation.name==name:
            return nation

def convertToChannelName(nationName):
    newString =""
    for i in range(len(nationName)):
        if nationName[i]==' ':
            newString+='-'
        else:
            newString+=nationName[i].lower()
    return newString

def findMemberInMembersList(name,membersList):
    for member in membersList:
        if name == member.name:
            return member

# used to see if member is in alist
def memberInList(name,membersList):
    for member in membersList:
        if name in member.name.split('#')[0]:
            return True
    return False
#used to see if member is in the designated nation
def memberInNation(member,nationName):
    roles = member.roles
    for role in roles:
        if role.name==nationName:
            return True
    return False

def userNation(member,nationName,nationsList):
    if(memberInNation(member,nationName)):
        for nation in nationsList:
            if nation.name==nationName:
                return nation
    
            

def findNationIndex(name,nationsList):
    for i in range(len(nationsList)):
        if name == nationsList[i].name:
            return i
def has_role(member,roleName):
    for mRole in member.roles:
        if roleName==mRole:
            return True
    return False
