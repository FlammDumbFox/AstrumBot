import discord
import json
import os
from discord.ext import commands

class EmojiAnalytics(commands.Cog):

    # Initializing the Cog
    def __init__(self, bot):

        # Allows the Cog itself to work
        self.bot = bot
    
    # This listener is required for commands:
    @commands.Cog.listener()
    async def on_ready(self):
        setup(self.bot)
        print("[cogs/analytics] Emoji Analytics module loaded.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        for e in self.bot.emojis:
            if f"<:{e.name}:{e.id}>" in message.content:
            #    await message.channel.send(f"Eu vejo um <:{e.name}:{e.id}>!")
                sortAndUpdateJsonDump(updateEmojiCount(readJsonDump(), e.name, e.id))

    @commands.command(name = "emojilist")
    async def printEmojiList(self, ctx):
        await ctx.send(getSortedEmojiList())

def readJsonDump():
    jsonPath = "./data/EmojiAnalytics.json"
    try:
        jsonFile = open(jsonPath, 'r')
    except IOError:
        jsonFile = open(jsonPath, 'w+')
    d = json.loads(jsonFile.read())
    jsonFile.close()
    return d

def updateEmojiCount(jsonDict, emojiName, emojiId):
    em = f"<:{emojiName}:{emojiId}>" 
    if em in jsonDict:
        jsonDict[em] += 1
    else:
        jsonDict[em] = 1
    return jsonDict

def sortAndUpdateJsonDump(jsonDict: dict):
    jsonDict = sorted(jsonDict.items(), key = lambda item: item[1])
    with open("./data/EmojiAnalytics.json", 'w+') as f:
        f.write(json.dumps(dict(jsonDict)))

def getSortedEmojiList():
    jsonPath = "./data/EmojiAnalytics.json"
    buf = ''
    finalString = ''
    with open(jsonPath) as f:
        buf = json.loads(f.read())
    for emoji in buf:
        finalString += f"{emoji}: {buf[emoji]}\n"
    return finalString

def setup(bot):
    bot.add_cog(EmojiAnalytics(bot))
