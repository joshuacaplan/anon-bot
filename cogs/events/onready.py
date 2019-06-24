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
        await self.bot.change_presence(activity=discord.Game('!dm to use'))

        # setup database connection
        conn = sqlite3.connect('anon.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS anon_messages
                (event_id INTEGER PRIMARY KEY AUTOINCREMENT, messageType TEXT, sender INTEGER, receiver INTEGER, message TEXT)''')
        conn.commit()
        conn.close()


def setup(bot):
    bot.add_cog(OnReady(bot))
