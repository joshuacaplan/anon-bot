import discord
import sqlite3
from discord.ext import commands
from random import randint


class DisableMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['disable'])
    async def disablemessages(self, ctx):
        conn = sqlite3.connect('anon.db')
        c = conn.cursor()
        user = ctx.author.id

        # check if user exists in db
        # sql does not have boolean datatypes
        # 0 = False, 1 = True
        try:
            user_setting = c.execute(
                f'SELECT allow_anon_messages FROM userOptions WHERE user_id={user}').fetchone()[0]
        except TypeError:
            user_setting = 0

        if user_setting == 1:
            user_setting = 0
            c.execute(
                'UPDATE userOptions SET allow_anon_messages = ? WHERE user_id = ?', (user_setting, user))
            conn.commit()
            await ctx.send('You are no longer allowing anonymous messages.')
        else:
            await ctx.send('Anonymous messages are already disabled!')
        conn.close()


def setup(bot):
    bot.add_cog(DisableMessages(bot))
