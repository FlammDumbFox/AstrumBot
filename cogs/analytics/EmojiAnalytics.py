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
            if f"<:{e.name}:{e.id}>" in message.content or f"<a:{e.name}:{e.id}>" in message.content:
            #    await message.channel.send(f"Eu vejo um <:{e.name}:{e.id}>!")
                sortAndUpdateJsonDump(updateEmojiCount(readJsonDump(), e))

## Emoji List
    @commands.command(name = "emojilist")
    async def printEmojiList(self, ctx):
        emojiMessageList = getSortedEmojiList()
        for message in emojiMessageList:
            await ctx.send(message)
            
    
## Generate list of emojis
    @commands.command(name = "generatelist")
    async def generateEmojiList(self, ctx):
        await ctx.send("Dando fetch em todos os emojis...")
        for e in self.bot.emojis:
            sortAndUpdateJsonDump(purgeNonExistentEmojis(initializeEmojiCount(readJsonDump(), e), self.bot.emojis))
        await ctx.send("Fetch terminado.")

## Read the current list of emojis
def readJsonDump():
    jsonPath = "./data/EmojiAnalytics.json"
    try:
        jsonFile = open(jsonPath, 'r')
    except IOError:
        jsonFile = open(jsonPath, 'w+')

    # Dumps the .json file into a string
    d = json.loads(jsonFile.read())
    jsonFile.close()

    # and returns it
    return d

def updateEmojiCount(jsonDict, emoji):

    if emoji.animated:
        em = f"<a:{emoji.name}:{emoji.id}>"
    else:
        em = f"<:{emoji.name}:{emoji.id}>"

    if em in jsonDict:
        jsonDict[em] += 1
    else:
        jsonDict[em] = 1

    return jsonDict

    
def initializeEmojiCount(jsonDict, emoji):

    if emoji.animated:
        em = f"<a:{emoji.name}:{emoji.id}>"
    else:
        em = f"<:{emoji.name}:{emoji.id}>"

    if em not in jsonDict:
        jsonDict[em] = 0
    return jsonDict

## Deletes obsolete emojis
def purgeNonExistentEmojis(jsonDict, emojiList):

    # Generate two "buffer" lists as a copy
    jsonDictCopy = jsonDict.copy()
    emojiListCopy = []

    # If an emoji exists in the current list, add it to the buffer list
    for e in emojiList:
        if e.animated:
            emojiListCopy.append(f"<a:{e.name}:{e.id}>")
        else:
            emojiListCopy.append(f"<:{e.name}:{e.id}>")

    # If an emoji exists in file but not in the buffer list, delete it
    for e in jsonDictCopy:
        if not e in emojiListCopy:
            jsonDict.pop(e)
            
    # Then, return the updated list            
    return jsonDict

def sortAndUpdateJsonDump(jsonDict: dict):
    # Sorts the dictionary
    jsonDict = sorted(jsonDict.items(), key = lambda item: item[1])
    with open("./data/EmojiAnalytics.json", 'w+') as f:
        f.write(json.dumps(dict(jsonDict)))

# Gets the list of strings to be output
def getSortedEmojiList():
    jsonPath = "./data/EmojiAnalytics.json"
    buf = ''
    finalStringList = []
    finalString = ''
    i = 0
    clipMessage = 0

    with open(jsonPath) as f:
        buf = json.loads(f.read())

    # Creates a list of formatted strings
    for emoji in buf:
        if i >= 5:
            finalString += "\n"
            clipMessage += 1
            i = 0
        if clipMessage >= 8:
            finalStringList.append(finalString)
            finalString = ''
            clipMessage = 0
        finalString += f"\|   {emoji} - {buf[emoji]}   \|"
        i += 1
    finalStringList.append(finalString)
    return finalStringList

def setup(bot):
    bot.add_cog(EmojiAnalytics(bot))
