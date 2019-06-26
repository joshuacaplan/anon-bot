import discord
import sqlite3
from discord.ext import commands
from random import randint


class AllowMessaging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # SQL does not have boolean datatypes
    # 0 indicates that the user has anonymous messaging disabled
    # 1 indicates that the user has anonymous messaging enabled

    @commands.command(aliases=['enable'])
    async def enablemessages(self, ctx):
        conn = sqlite3.connect('anon.db')
        c = conn.cursor()
        user = ctx.author.id

        try:
            user_setting = c.execute(f'SELECT allow_anon_messages FROM userOptions WHERE user_id={user}').fetchone()[0]
            if not user_setting:
                user_data = (1, user)
                c.execute('UPDATE userOptions SET allow_anon_messages = ? WHERE user_id = ?', user_data)
                conn.commit()
                await ctx.send('Anonymous messaging is **ENABLED**')
            else:
                await ctx.send('Anonymous messaging is already **ENABLED**')
        except TypeError:  # if user does not exist, insert 1 to indicate enabled
            user_data = (user, 1)
            c.execute('INSERT INTO userOptions VALUES (null,?,?)', user_data)
            conn.commit()
            await ctx.send('Anonymous messaging is already **ENABLED**')         
        conn.close()

    @commands.command(aliases=['disable'])
    async def disablemessages(self, ctx):
        conn = sqlite3.connect('anon.db')
        c = conn.cursor()
        user = ctx.author.id

        # check if user exists in db
        try:
            user_setting = c.execute(f'SELECT allow_anon_messages FROM userOptions WHERE user_id={user}').fetchone()[0]
            if user_setting:
                user_data = (0, user)
                c.execute('UPDATE userOptions SET allow_anon_messages = ? WHERE user_id = ?', user_data)
                conn.commit()
                await ctx.send('Anonymous messaging is **DISABLED**')
            else: await ctx.send('Anonymous messaging is already **DISABLED**')
        except TypeError:  # if user does not exist, insert 0 to disable anonymous messaging
            user_data = (user, 0)
            c.execute('INSERT INTO userOptions VALUES (null,?,?)', user_data)
            conn.commit()
            await ctx.send('Anonymous messaging is **DISABLED**')        
        conn.close()
    
    @commands.command(aliases=['status'])
    async def anonstatus(self, ctx):
        conn = sqlite3.connect('anon.db')
        c = conn.cursor()
        user = ctx.author.id

        try: user_setting = c.execute(f'SELECT allow_anon_messages FROM userOptions WHERE user_id={user}').fetchone()[0]
        except TypeError:
            user_data = (user, 1)
            c.execute('INSERT INTO userOptions VALUES (null,?,?)', user_data)
            conn.commit()
            user_setting = 1
        
        if user_setting: await ctx.send('Anonymous messaging: **ENABLED**')
        else: await ctx.send('Anonymous messaging: **DISABLED**')
            

def setup(bot):
    bot.add_cog(AllowMessaging(bot))
