#importing modules
import discord
from discord.ext import commands
from pymongo import MongoClient
import asyncio
import youtube_dl
 
bot_channel = #put the channel ID here. You can get the channel ID by heading over to the channel > right click > copy channel ID
talk_channels = [] #ID's of every channel wherein you want the bot to allot xp to a user

# you can have as many levels as you like
level = ["Level 1", "Level 2", "Level 3"] #you'll have to create roles (aka the levels) and put them here. So if my roles were Level 1, Level 2, and Level 3, then I'll use this
levelnum = [10,20,30]
 
cluster = MongoClient("") #put the string of text that you copied in "" from MongoDB's website and replace the password with your cluster's password
 
collection_name = cluster["database_name"]["collection_name"] #replace the database_name and the collection_name from MongoDB here.
 
#initiation
class levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client
 
    @commands.Cog.listener()
    async def on_ready(self):
        print("Online!")

#gaining exp. It gains 1 exp but you can change it accordingly.
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channels: #to check if it's in the right channel
            stats = collection_name.find_one({"id":message.author.id}) #replace collection_name with your collection's name
            if not message.author.bot: #to check that it isn't levelling the bot up.
                if stats is None: #to check if they're registered
                    newuser = {"id" : message.author.id, "xp" : 0}
                    collection_name.insert_one(newuser) #replace collection_name with you collection's name; this is to insert the details into the database
                else: #means that they're registered
                    xp = stats["xp"] + 1 #increases xp by 1
                    collection_name.update_one({"id":message.author.id}, {"$set":{"xp":xp}}) #replace collection_name with your collection's name; is being ussed to update the databse
                    #to find what level the user's at
                    lvl = 0
                    while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    if xp == 0:
                        await message.channel.send(f"Congrats! {message.author.mention}! You leveled up to **level: {lvl}**!") #sending an alert when the user levels up
                        #to check if they got a new role or not
                        for i in range(len(level)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                                embed = discord.Embed(description=f"{message.author.mention}. New role: **{level[i]}**!!!")
                                embed.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.send(embed=embed)
 
#to get rank
    @commands.command()
    async def rank(self, ctx):
        if ctx.channel.id == bot_channel: #to check if they're sending it in the right channel
            stats = collection_name.find_one({"id" : ctx.author.id}) #replace collection_name with your collection's name
            if stats is None: #checks if the user has send messages or not. If not then it send the message mentioned below
                embed = discord.Embed(description="You need to send messages to obtain a rank!")
                await ctx.channel.send(embed=embed)
            else: #if the user has send messages to the right channel(s)
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                boxes = int((xp/(200*((1/2) * lvl)))*20) #shows boxes (for visual effect)
                rankings = collection_name.find().sort("xp",-1) #replace collection_name with your collection's name
                for x in rankings: #to show what rank they are
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                #using this to send all the info
                embed = discord.Embed(title="{}'s level stats".format(ctx.author.name))
                embed.add_field(name="Name", value=ctx.author.mention, inline=True)
                embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
                embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                embed.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
#Leaderboard
    @commands.command()
    async def leaderboard(self, ctx):
        if (ctx.channel.id == bot_channel):
            rankings = collection_name.find().sort("xp",-1) #replace collection_name with your collection's name
            i = 1
            embed = discord.Embed(title="Rankings:")
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    embed.add_field(name=f"{i}: {temp.name}", value=f"Total XP: {tempxp}", inline=False)
                    i += 1
                except:
                    pass
                if i == 11:
                    break
            await ctx.channel.send(embed=embed)

#music commands
#you'll need a youtube link for music commands. Queuing music will be added soon! :')
class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Please join a voice channel.")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()


    @commands.command()
    async def play(self, ctx, url):
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio'}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send('Paused.')

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send('Resumed.')
            
#setting up cogs
def setup(client):
    client.add_cog(levels(client))
