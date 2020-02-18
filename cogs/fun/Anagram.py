import discord
import random
from discord.ext import commands

# Creates a Cog
class Anagram(commands.Cog):
    
    # Initializes a Cog
    def __init__(self, bot):

        # Allows the Cog itself to work
        self.bot = bot

    # This listener is required for commands
    @commands.Cog.listener()
    async def on_ready(self):
        setup(self.bot)
        print("[cogs/fun] Anagram module loaded.")

    # The command itself
    @commands.command(name = "anagram")
    async def anagram(self, ctx, w):
        pass

def setup(bot):
    bot.add_cog(Anagram(bot))

def generate_anagram(w):
    w = list(w)
    random.shuffle(w)
    return ''.join(w)