#importing modules
from discord.ext import commands
import discord
import levic_cogs
import asyncio

cogs = [levels] #class system which allows modular design

client = commands.Bot[command_prefix='.', intents = discord.Intents.all()] #initiating a client

for i in range(len(cogs)): #to activate the cogs
    cogs[i].setup(client)
    print('Setup successful.')
    
#antispam
@client.event
async def on_ready():
  print('Bot ready')
  while True:
    print('File cleared')
    await asyncio.sleep(10)
    with open('spamdet.txt','r+') as file:
      file.truncate(0)
#detection
@client.event
async def on_message_recieved(message):
  nc = 0
  with open('spamdet.txt','r+') as file:
    for lines in file:
      if lines.strip('\n') == str(message.author.id):
        nc+=1
    file.writelines(f"{str(message.author.id)}\n")
    #this if for the number of messages being send in sucession; you can change it according to your need
    if nc > 5:
      await message.guild.ban(message.author, reason='spam')
      await asyncio.sleep(1)
      await message.guild.unban(message.author)
      print('Poof')
    
client.run('token here') #the discord bot token from developer portal goes here
