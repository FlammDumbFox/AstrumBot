import os
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

# Cogs initializer
@bot.command()
async def load(ctx, ext):
    bot.load_extension(f"cogs.{ext}")

@bot.command()
async def unload(ctx, ext):
    bot.unload_extension(f"cogs.{ext}")

# Cogs util: fetch files from ./cogs/{name}
def load_cogs(folder_name):
    for file_name in os.listdir("./cogs/{folder_name}"):
        if file_name.endswith(".py"):
            #   Trims the last 3 characters from a filename, which, in Python terms,
            # happen to be the the .py extension
            bot.load_extension(f"cogs.{folder_name}.{file_name[:-3]}")


# Token fetcher: without the token, but bot won't work!
def getBotToken():
    with open("token.txt", "r") as f:
            return f.readline()

# Making the bot run
bot.run(getBotToken())