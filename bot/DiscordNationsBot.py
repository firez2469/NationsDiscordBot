# bot.py
import os
import random
from discord.ext import commands
from discord.utils import get
import discord
import asyncio
import random
import DiscordNations as n
import SearchFunctions as s
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.',intents=intents)
TOKEN = os.getenv('DISCORD_TOKEN')

counter = {}
nations = []
serversNations = {}
import time

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    # await channel.send('**THE NUKES WILL SOON BE DROPPED**')
    print(bot.guilds)

@commands.has_role('Independent Corporations')
@bot.command()
async def FullSetUp(ctx):
    serversNations[ctx.message.guild.name]=[]
    print("Added '{0}' server to the collection of servers".format(ctx.message.guild))
    server = ctx.message.guild
    roles = server.roles
    rolesForServer = ["Citizen","National Leader","National Representative","Independant Contractors","World Congress Host"]
    for role in rolesForServer:
        await server.create_role(name=role)
@commands.has_role('Independent Corporations')
@bot.command()
async def PartialSetup(ctx):
    serversNations[ctx.message.guild.name] = [n.Nation("nonetype1",0,"nuuuuuul",0)]
    print(serversNations)
    print("Added '{0}' server to the collection of servers".format(ctx.message.guild))
    await ctx.send("Server Is Set Up")
#MASSIVE BUG serversNation works until createNation where it needs to add nation ot serversNations, where it bugs out and returns null
@bot.command()
async def createNation(ctx,*,name):
    user = ctx.author

    if not s.roleInList("Citizen",user.roles):
        server = ctx.message.guild
        new_nation = n.Nation(name,1,ctx.author.name,1)
        new_nation.citizens=[user.name]
        new_nation.money=0

        nationslist = serversNations[server.name]
        nationslist.append(new_nation)
        serversNations[server.name] = nationslist
        #serversNations[server.name] = nationslist.append(newNation)
        await ctx.send("The Nation of **{0}** has been founded by {1}!!!".format(name,ctx.author.name))
        role = get(server.roles, name="National Leader")
        role2 =get(server.roles,name="Citizen")
        try:
            await ctx.author.add_roles(role)
            await ctx.author.add_roles(role2)
            await server.create_role(name="{0}".format(name),colour=discord.Colour(0x00c7ff))

        except:
            await ctx.send("Also... Bot has insuffient permissions to change roles")
        try:
            newRole = get(server.roles, name=name)
            await ctx.author.add_roles(newRole)
        except:
            print('not enough perms')
        countryRole = get(server.roles,name=name)
        await server.create_category(name)
        category = discord.utils.get(server.categories, name=name)
        await server.create_text_channel("{0} general".format(name),category=category)
        await category.set_permissions(countryRole, read_messages=True, send_messages=True,read_message_history=True)
        await category.set_permissions(get(server.roles,name="@everyone"),read_messages = False)
        await category.set_permissions(get(server.roles,name="National Leader"),manage_channels=True,manage_permissions=True,manage_messages=True)
        await countryRole.edit(hoist=True)

    else:
        await ctx.send("You are already a member of a Nation, leave or dissolve the nation to found a new one.")


# doesn not remove "citizen"and "representtive" role from all other citizen
@bot.command()
async def dissolveNation(ctx):
    print('{0} requested to dissolve nation'.format(ctx.author.name))
    user = ctx.message.author
    server = user.guild
    roles = user.roles
    print("Nations:",serversNations[server.name])
    if s.isPartOfCountry(roles,serversNations[server.name]):
        role = s.findNationName(roles,serversNations[server.name])
        if not (role == "World Congress Host" or role == "Independant Contractors" or role=="National Leader" or role=="National Representative"
        or role == "Citizen" or role=="@everyone"):
            try:
                await get(user.roles,name=role).delete()
            except discord.Forbidden:
                await ctx.send('I do not have permission to manage and delete roels')
        if s.roleInList("National Leader",user.roles):
            r = get(user.roles, name="National Leader")
            if r.name == "National Leader":
                await user.remove_roles(r)
        if s.roleInList("National Representative",user.roles):
            r = get(user.roles,name="National Representative")
            await user.remove_roles(r)
        r = get(user.roles,name="Citizen")
        await user.remove_roles(r)
        category = discord.utils.get(server.categories, name=role)
        for channel in category.channels:
            await channel.delete()
        await category.delete()
        index = s.findNationIndex(role,serversNations[server.name])
        atWarWithList = serversNations[server.name][index].atWarWith
        for nationName in atWarWithList:
            index = s.findNationIndex(nationName,serversNations[server.name])
            serversNations[server.name][index].atWarWith.remove(role)

        serversNations[server.name].pop(index)



@bot.command()
async def renameNation(ctx,*,name):
    user = ctx.message.author
    server = user.guild
    roles = user.roles
    if s.isPartOfCountry(roles, serversNations[server.name]):
        nationName = s.findNationName(roles,serversNations[server.name])
        for i in range(len(serversNations[server.name])):
            if serversNations[server.name][i].name==nationName:
                nation1 =serversNations[server.name][i]
                serversNations[server.name][i]=n.Nation(name,nation1.influence,nation1.leaderUser,nation1.numberOfChannels)
        role = get(user.roles, name=nationName)
        await role.edit(name=name)
        await ctx.send("The Nation of {0} has been renamed to {1}".format(nationName,name))
        category = discord.utils.get(server.categories, name=nationName)
        index=1
        for channel in category.channels:
            await channel.edit(name="{0} channel {1}".format(name,index))
            index+=1
        await category.edit(name=name)
        n.debugNationsList(serversNations[server.name])
    print('{0} changed name of nation they were part of to {1}'.format(nationName,name))

#wishlist
@bot.command()
async def changeLeader(ctx,member1:discord.Member):
    user = ctx.author
    server = ctx.author.guild
    roles =user.roles
    print("{0} requested to change the leader of his nation with {1}".format(user.name,member1.name))
    if s.isPartOfCountry(user.roles, serversNations[server.name]):
        members = server.members
        if s.memberInList(member1.name,members):
            nationName = s.findNationName(member1.roles, serversNations[server.name])
            print("Found nation: {0}".format(nationName))
            role = get(server.roles, name="National Leader")
            #m = s.findMemberInMembersList(member1.name,members)
            if s.memberInNation(member1,nationName):
                await user.remove_roles(role)
                await member1.add_roles(role)
                nat = s.findNationByName(nationName,serversNations[server.name])
                newNation = n.Nation(nat.name,nat.influence, ctx.author.name, nat.numberOfChannels)
                for i in range(len(serversNations[server.name])):
                    if serversNations[server.name][i]==nat.name:
                        serversNations[server.name][i]=newNation
            else:
                await ctx.send("Member is not part of your nation")
        else:
            await ctx.send("Member is not found")
    #print('changing leader. This role is only for people with leader role')


@bot.command()
async def joinNation(ctx,*,name):
    user = ctx.author
    server=user.guild
    print("{0} joined {1}".format(user.name,name))
    try:
        role = get(server.roles, name=name)
        role2 = get(server.roles, name="Citizen")
        await ctx.author.add_roles(role)
        await ctx.author.add_roles(role2)
    except:
        await ctx.send("Failed to join {0}".format(name))
        
    index1 = s.findNationIndex(name, serversNations[server.name])
    serversNations[server.name][index1].influence += 1
    

    print('Sucessfully joined')

@bot.command()
async def leaveNation(ctx):
    print('{0} requested to leave their nation'.format(ctx.author.name))
    user = ctx.author
    server = user.guild

    try:
        if s.isPartOfCountry(user.roles,serversNations[server.name]):
            nationName = s.findNationName(user.roles,serversNations[server.name])
            role = get(server.roles, name=nationName)
            roleCitizen = get(server.roles,name="Citizen")
            if s.roleInList("National Leader", user.roles):
                #r = get(user.roles, name="National Leader")
                #if r.name == "National Leader":
                    #await user.remove_roles(r)
                await ctx.send('You are the leader of this nation, you must either dissolve your nation, or change leadership before leaving')
            else:
                await user.remove_roles(role)
                await user.remove_roles(roleCitizen)
                index1 = s.findNationIndex(nationName,serversNations[server.name])
                serversNations[serversNations][index1].influence-= 1
        else:
            await bot.run("You are not part of a nation")
    except:
        await bot.run('Insufficient permissions for bot')

#will eventually need a better alternative to store all nations data off of discord itself
@commands.has_role('Independent Corporations')
@bot.command()
async def recover(ctx,*,recovery=""):
    server = ctx.message.guild
    channels = server.channels
    channelFound = False

    if len(recovery)>0:
        servers1 = recovery.split('}')
        if len(servers1)>0:
            for servers2 in servers1:
                if len(servers2)>0:
                    serverName = servers2.split('{')[0]
                    nationsList = servers2.split('{')[1]
                    print(nationsList)
                    list1=nationsList
                    serversNations[serverName]=[]
                    for n1 in list1.split('|'):
                        if len(n1)>0:
                            components = n1.split(',')
                            serversNations[server.name].append(n.Nation(components[0],components[1],components[2],components[3]))
                print("sucessfully recovered nations")
    await ctx.send("Successfully recovered nations data")

@commands.has_role('Independent Corporations')
@bot.command()
async def saveRecovery(ctx):
    print("{0} requested recovery data".format(ctx.author.name))
    finalText = ""
    for server in serversNations:
        text = n.printRecovery(serversNations[server])
        finalText+= server+"{"+text+"}"
    await ctx.send(finalText)
    #await ctx.send(n.printRecovery(serversNations[ctx.author.guild.name]))

@commands.has_role('Independent Corporations')
@bot.command()
async def testRole(ctx,*,name):
    countryRole = get(ctx.guild.roles,name=name)
    await countryRole.edit(hoist=True)
@commands.has_role('National Leader')
@bot.command()
async def addRepresentative(ctx,*,member1:discord.Member):
    #if(s.has_role(member1,s.findNationName(ctx.author.roles,serversNations[ctx.guild.name]))):
    repRole = get(ctx.guild.roles,name="National Representative")
    await member1.add_roles(repRole)
    await ctx.send("New Role assigned")
    print("{0} requested representative role for {1}".format(ctx.author.name,member1.name))
   # else:
        #print("{0} failed to add representative".format(ctx.author.name))
        #await ctx.send("The member you selected is not a Citizen of your nation")

@commands.has_role('National Leader')
@bot.command()
async def removeRepresentative(ctx,*,member1:discord.Member):
    if s.has_role(member1,"National Representative"):
        repRole = get(ctx.guild.roles,name="National Representative")
        await member1.remove_roles(repRole)
        await ctx.send("Representative role removed from {0}".format(member1.name))
        print("Representative role removed from {0}".format(member1.name))
    else:
        print("{0} failed to remove representative role from {1}".format(ctx.author.name,member1.name))
        await ctx.send("Failed to remove representation role from {1}".format(member1.name))

@commands.has_role('Citizen')
@bot.command()
async def stats(ctx,*,nationName):
    for nation in serversNations[ctx.guild.name]:
        if nation.name==nationName:
            message = "**{0} stats**\n " \
                      "Influence {1}\n " \
                      "Leader {2}\n Army {3}\n" \
                      " At War with: {4}".format(nation.name,nation.influence,nation.leaderUser,nation.armySize,n.formatNationsAtWarWith(nation.atWarWith))
            await ctx.send(message)
    print("Nation stats requested by {0} for {1}".format(ctx.author.name,nationName))

#@commands.has_role('National Leader')
#@bot.command()
#async def resetChannelPerms(ctx,category:discord.CategoryChannel):
#    for channel in category.channels:
#        leaderRole = get(ctx.guild.roles,name="National Leader")
#        await category.set_permissions(read_messages=True, send_messages=True,read_message_history=True,mange_channel=True,manage_permissions=True)
#    print("Channel reset requested by {0}".format(ctx.author.name))




@bot.command()
async def nations(ctx):
    message ="**List of Nations:**\n"
    for nation in serversNations[ctx.guild.name]:
        if not nation.name == "nonetype1":
            message+= "{0}\n".format(nation.name)
    await ctx.send(message)
    print("List of nations requested by {0}".format(ctx.author.name))
#@commands.has_role('National Leader')
#@bot.command()
#async def buildArmy(ctx):
#    server = ctx.guild
#    nationName = s.findNationName(ctx.author.roles,serversNations[server.name])
#    index1 = s.findNationIndex(nationName,serversNations[server.name])
#    strength = (random.random()*0.6)+.8
#    serversNations[server.name][index1].armySize += strength
#    serversNations[server.name][index1].influence -=1
#    await ctx.send("The army of {0} has been added the strength of {1}!".format(nationName,strength))
#    print("{0} built their army for {1} with strength of {2}".format(ctx.author.name,nationName,strength))

#@commands.has_role('Naitonal Leader')
#@bot.command()
#async def DeclareWar(ctx,nation:discord.Role):
#    print('{0} declared war on {1}'.format(ctx.author.name,nation.name))
#    server = ctx.guild
#    thisNationName = s.findNationName(ctx.author.roles,serversNations[server.name])
#    thisNation = s.findNationByName(thisNationName,serversNations[server.name])
#    thatNation = s.findNationByName(nation.name,serversNations[server.name])
#    if thisNationName==thatNation.name:
#        await ctx.send("You can't declare war on yourself")
#    else:
#        await ctx.send("**{0} has declared war on {1}!!!**".format(thisNationName,thatNation.name))
#        thisIndex = s.findNationIndex(thisNationName,serversNations[server.name])
#        thatIndex = s.findNationIndex(thatNation.naem,serversNations[server.name])
#        serversNations[server.name][thisIndex].atWarWith.append(nation.name)
#        serversNations[server.name][thatIndex].atWarWith.append(thisNationName)

bot.run(TOKEN)


