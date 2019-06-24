import discord
import sqlite3
from discord.ext import commands

from random import randint


class Reply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reply(self, ctx):
        if type(ctx.channel) != discord.DMChannel:
            await ctx.send(f"Send your message to the bots DMs!")
            await ctx.message.delete()
        else:
            try:
                conn = sqlite3.connect('anon.db')
                c = conn.cursor()
                stuff = ctx.message.content.split(' ')
                thread_id, message = stuff[1], ' '.join(stuff[2:])
                user = ctx.author
                receiver = user.id
                anon_id = c.execute(
                    f"SELECT anon_sender FROM anon_messages WHERE thread_id={thread_id}").fetchone()[0]
                anon = discord.utils.get(self.bot.users, id=anon_id)

                # insert data
                # storing replies isn't necessary, but its there if needed
                data = ("REPLY", thread_id, anon_id, receiver, message)
                c.execute(
                    'INSERT INTO anon_messages VALUES (null,?,?,?,?,?)', data)
                conn.commit()

                embed = discord.Embed(
                    title="Your message was replied to!", color=0x267d28,
                    description=f'Use `!reply {thread_id} <msg>` to respond')
                embed.add_field(
                    name='Thread ID:', value=thread_id, inline=True)
                embed.add_field(
                    name='Message:', value=message, inline=True)
                await ctx.send(embed=embed)
                await user.send('Sent! :mailbox_with_mail:')
            except AttributeError:
                await ctx.send(f'Unknown message thread!')
            conn.close()


def setup(bot):
    bot.add_cog(Reply(bot))
