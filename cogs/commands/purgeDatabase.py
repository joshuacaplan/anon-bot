import discord
from discord.ext import commands
from subprocess import Popen
from Globals import bot_owners
import os
import sqlite3


my_user_id = int(os.environ['my_user_id']) or 0

class PurgeDatabase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['purgedb'])
    async def purgedatabase(self, ctx):
        if ctx.author.id in bot_owners:
            try:
                os.remove('anon.db')
                conn = sqlite3.connect('anon.db')
                c = conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS threads
                        (event_id INTEGER PRIMARY KEY AUTOINCREMENT, thread_id INTEGER, anon_sender INTEGER, receiver INTEGER)''')
                c.execute('''CREATE TABLE IF NOT EXISTS messages
                        (thread_id INTEGER, message_id INTEGER, sender INTEGER, message TEXT)''')
                c.execute('''CREATE TABLE IF NOT EXISTS reports
                        (report_id INTEGER PRIMARY KEY AUTOINCREMENT, thread_id INTEGER, anon_sender INTEGER, reporter INTEGER, details TEXT)''')
                c.execute('''CREATE TABLE IF NOT EXISTS guildOptions
                        (event_id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER, report_channel_id INTEGER)''')
                c.execute('''CREATE TABLE IF NOT EXISTS userOptions
                        (event_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, allow_anon_messages BOOLEAN)''')
                c.execute('''CREATE TABLE IF NOT EXISTS guildFilters
                        (words TEXT, server_id INTEGER)''')
                conn.commit()
                conn.close()
                await ctx.send('Database purged!')
            except PermissionError:
                await ctx.send('Unable to purge database. Is another process using it?')
        else:
            await ctx.send(f'You do not have permission to use this command!')


def setup(bot):
    bot.add_cog(PurgeDatabase(bot))