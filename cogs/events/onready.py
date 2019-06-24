import discord
from discord.ext import commands

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged In')
        await self.bot.change_presence(activity=discord.Game('!dm to use'))

def setup(bot):
    bot.add_cog(OnReady(bot))