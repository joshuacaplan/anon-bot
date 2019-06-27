import discord
from discord.ext import commands
from subprocess import Popen
from Globas import bot_owners
import os


my_user_id = int(os.environ['my_user_id']) or 0

class PurgeDatabase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['purgedb'])
    async def purgedatabase(self, ctx):
        if ctx.author.id == my_user_id or ctx.author.id in bot_owners:
            try:
                os.remove('anon.db')
                await ctx.send('Database removed! Restarting now..')
            except PermissionError:
                await ctx.send('Unable to purge database. Is another process using it?')
            await self.bot.change_presence(activity=discord.Game('Restarting...'))
            Popen('python bot.py')
            await self.bot.logout()
        else:
            await ctx.send(f'You do not have permission to use this command!')


def setup(bot):
    bot.add_cog(PurgeDatabase(bot))