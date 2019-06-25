import discord
import sqlite3
from discord.ext import commands

from random import randint


class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dm(self, ctx):
        if type(ctx.channel) is not discord.DMChannel:
            await ctx.send(f"Send your message to the bots DMs!")
            await ctx.message.delete()
        else:
            try:
                conn = sqlite3.connect('anon.db')
                c = conn.cursor()
                args = ctx.message.content.split(' ')
                user, message = args[1], ' '.join(args[2:])
                user = discord.utils.get(self.bot.users, name=user)
                anon = ctx.author
                receiver = user.id
                anon_sender = ctx.author.id
                message_id = 1

                # generates thread_id and checks if it exists
                while True:
                    try:
                        thread_id = ''.join((str(randint(0, 9))
                                             for _ in range(10)))
                        c.execute(
                            f"SELECT receiver FROM threads WHERE thread_id={thread_id}")
                        # if no rows exist, break out of regen loop
                        thread_data = c.fetchone()[0]
                    except TypeError:
                        break

                # insert data
                thread_data = (thread_id, anon_sender, receiver)
                message_data = (thread_id, message_id, anon_sender, message)
                c.execute(
                    'INSERT INTO threads VALUES (null,?,?,?)', thread_data)
                c.execute(
                    'INSERT INTO messages VALUES (?,?,?,?)', message_data)
                conn.commit()

                embed = discord.Embed(
                    title="Anonymous message inbound!", color=0x267d28,
                    description=f'Use `!reply {thread_id} <msg>` to respond')
                embed.add_field(
                    name='Thread ID:', value=thread_id, inline=True)
                embed.add_field(
                    name='Message:', value=message, inline=True)
                await user.send(embed=embed)
                await anon.send('Sent! :mailbox_with_mail:')
            except AttributeError:
                await ctx.send(f'A user with that name could not be found. Names are case specific.')
            conn.close()


def setup(bot):
    bot.add_cog(DM(bot))
