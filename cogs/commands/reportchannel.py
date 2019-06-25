import discord
import sqlite3
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure


class ReportChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permissions(manage_channels=True)
    async def reportchannel(self, ctx):
        try:
            conn = sqlite3.connect('anon.db')
            c = conn.cursor()
            args = ctx.message.content.split(' ')
            channel = args[1].replace('<', '').replace(
                '#', '').replace('>', '')

            data = (ctx.guild.id, channel)
            c.execute(
                'INSERT INTO guildOptions VALUES (null,?,?)', data)
            conn.commit()
            await ctx.send(f'Reports will be sent to <#{channel}>')
        except AttributeError:
            await ctx.send(f'Unknown message thread!')
        conn.close()


def setup(bot):
    bot.add_cog(ReportChannel(bot))
