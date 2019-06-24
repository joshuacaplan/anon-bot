import discord
from discord.ext import commands

import os

try:
    my_user_id = 0
except KeyError:
    my_user_id = int(os.environ['my_user_id'])

class Exit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='exit', aliases=['quit'])
    async def _exit(self, ctx):
        if ctx.author.id == my_user_id:
            await self.bot.change_presence(activity=discord.Game('Exiting...'))
            await self.bot.logout()

def setup(bot):
    bot.add_cog(Exit(bot))