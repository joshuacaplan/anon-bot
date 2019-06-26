import discord
import sqlite3
from discord.ext import commands


class Badwords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def badwords(self, ctx):
        if type(ctx.channel) is discord.DMChannel:
            await ctx.send(f'Send your message in a server!')
        else:
            conn = sqlite3.connect('anon.db')
            c = conn.cursor()
            server_id = ctx.guild.id
            args = ctx.message.content.split(' ')
            word = args[1]

            # insert data
            word_data = (word, server_id)
            c.execute(
                'INSERT INTO guildFilters VALUES(?,?)', word_data)
            conn.commit()
            await ctx.send("Word added to filter list!")
            conn.close()


def setup(bot):
    bot.add_cog(Badwords(bot))
