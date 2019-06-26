import discord
from discord.ext import commands
from Globals import *

import os

my_user_id = int(os.environ['my_user_id']) or 0


class Exit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='exit', aliases=['quit', 'shutdown'])
    async def _exit(self, ctx):
        if ctx.author.id in bot_owners:
            print('Requested to exit')
            await self.bot.change_presence(activity=discord.Game('Exiting...'))
            await ctx.send('Shutting down...')
            await self.bot.logout()


def setup(bot):
    bot.add_cog(Exit(bot))
