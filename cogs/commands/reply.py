import discord
import sqlite3
from discord.ext import commands

from random import randint


class Reply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reply(self, ctx):
        if type(ctx.channel) is not discord.DMChannel:
            await ctx.send(f'Send your message to the bots DMs!')
            await ctx.message.delete()
        else:
            try:
                conn = sqlite3.connect('anon.db')
                c = conn.cursor()
                args = ctx.message.content.split(' ')
                thread_id, message = args[1], ' '.join(args[2:])
                user = ctx.author
                receiver_id = c.execute(
                    f'SELECT receiver FROM threads WHERE thread_id={thread_id}').fetchone()[0]
                if receiver_id == user.id:
                    receiver_id = c.execute(
                        f'SELECT anon_sender FROM threads WHERE thread_id={thread_id}').fetchone()[0]
                receiver = discord.utils.get(self.bot.users, id=receiver_id)
                message_id = c.execute(
                    f'SELECT max(message_id) FROM messages WHERE thread_id={thread_id}').fetchone()[0]

                # insert data
                # storing replies isn't necessary, but its there if needed
                message_data = (thread_id, message_id + 1, user.id, message)
                c.execute(
                    'INSERT INTO messages VALUES (?,?,?,?)', message_data)
                conn.commit()

                embed_title = f'{user} replied to your message!' if receiver_id == user.id else 'You got another message'
                embed = discord.Embed(
                    title=embed_title, color=0x267d28,
                    description=f'Use `!reply {thread_id} <msg>` to respond')
                embed.add_field(
                    name='Thread ID:', value=thread_id, inline=True)
                embed.add_field(
                    name='Message:', value=message, inline=True)
                await receiver.send(embed=embed)
                await ctx.send('Reply sent! :mailbox_with_mail:')
            except AttributeError:
                await ctx.send(f'Unknown message thread!')
            conn.close()


def setup(bot):
    bot.add_cog(Reply(bot))
