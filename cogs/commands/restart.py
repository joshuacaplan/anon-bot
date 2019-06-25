import discord
from discord.ext import commands
from subprocess import Popen
import os

try:
    my_user_id = 0
except KeyError:
    my_user_id = int(os.environ['my_user_id'])

class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def restart(self, ctx):
        if ctx.author.id == my_user_id:
            print('Restarting')
            await self.bot.change_presence(activity=discord.Game('Restarting...'))
            Popen('python bot.py')
            await self.bot.logout()

def setup(bot):
    bot.add_cog(Restart(bot))