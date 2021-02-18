import discord
def roleInList(roleName, listOfRoles):
    for r in listOfRoles:
        print(r.name)
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

def findNationName(roles,nations):
    for role in roles:
        for nation in nations:
            if role.name==nation.name:
                return nation.name
    return ""
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
def memberInList(name,membersList):
    for member in membersList:
        if name in member.name.split('#')[0]:
            return True
    return False

def memberInNation(member,nationName):
    roles = member.roles
    for role in roles:
        if role.name==nationName:
            return True
    return False

def findNationIndex(name,nationsList):
    for i in range(len(nationsList)):
        if name == nationsList[i].name:
            return i