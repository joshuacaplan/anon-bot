import discord
import sqlite3
from discord.ext import commands
from random import randint


class EnableMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['enable'])
    async def enablemessages(self, ctx):
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
            user_setting = 2
            # 2 is the value when data needs to be CREATED, not UPDATED.

        if user_setting == 2:
            user_data = (user, 1)
            c.execute('INSERT INTO userOptions VALUES (null,?,?)', user_data)
            conn.commit()
            await ctx.send('You are now allowing anonymous messages.')
        elif user_setting == 0:
            user_data = (1, user)
            c.execute(
                'UPDATE userOptions SET allow_anon_messages = ? WHERE user_id = ?', user_data)
            conn.commit()
            await ctx.send('You are now allowing anonymous messages.')
        else:
            await ctx.send('Anonymous messages are already enabled!')
        conn.close()


def setup(bot):
    bot.add_cog(EnableMessages(bot))
