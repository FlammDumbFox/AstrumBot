import discord

from discord.ext import commands

# Bot aliases
PREFIX_LIST = ["a!", "astrum ", "Astrum "]

# initializing the bot itself
bot = commands.Bot(command_prefix = PREFIX_LIST)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    # Other tasks

    # Cogs

# Token fetcher: without the token, but bot won't work!
def getBotToken():
    with open("token.txt", "r") as f:
            return f.readline()

# Making the bot run
bot.run(getBotToken())