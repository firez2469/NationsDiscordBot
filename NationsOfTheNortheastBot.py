# bot.py
import os
import random
from discord.ext import commands
import asyncio
import random
import DiscordNations as n

bot = commands.Bot(command_prefix='!')
counter = {}

#TOKEN = os.getenv('DISCORD_TOKEN')

#main bot idea is to have multiple different states which are part


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
    #await channel.send('**THE NUKES WILL SOON BE DROPPED**')
    print(bot.guilds)




@bot.command
async def commandName(ctx):
    print('do something')



    
#bot.loop.create_task(search_submissions())

bot.run('NjY2MzE5OTgyMDk0NzEyODcz.Xhyc1w.loZGlLtxTyTi7OjD061i_qf3abw')
#bot.run(TOKEN)


