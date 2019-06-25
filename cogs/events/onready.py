import discord
import sqlite3
from discord.ext import commands


class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f'Logged in as {self.bot.user.name}#{self.bot.user.discriminator} (ID: {self.bot.user.id})')
        await self.bot.change_presence(activity=discord.Game('DM me !dm <username> <message>'))

        # setup database connection
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
        conn.commit()
        conn.close()


def setup(bot):
    bot.add_cog(OnReady(bot))
