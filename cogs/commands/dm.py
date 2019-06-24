import discord
import sqlite3
from discord.ext import commands

from random import randint


class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dm(self, ctx):
        if type(ctx.channel) != discord.DMChannel:
            await ctx.send(f"Send your message to the bots DMs!")
            await ctx.message.delete()
        else:
            try:
                conn = sqlite3.connect('anon.db')
                c = conn.cursor()
                stuff = ctx.message.content.split(' ')
                user, message = stuff[1], ' '.join(stuff[2:])
                user = discord.utils.get(self.bot.users, name=user)
                anon = ctx.author
                receiver = user.id
                anon_sender = ctx.author.id

                # generates thread_id and checks if it exists
                while True:
                    try:
                        thread_id = ''.join((str(randint(0, 9))
                                             for _ in range(10)))
                        c.execute(
                            f"SELECT receiver FROM anon_messages WHERE thread_id={thread_id}")
                        # if no rows exist, break out of regen loop
                        thread_data = c.fetchone()[0]
                    except TypeError:
                        break

                # insert data
                data = ("NEW_THREAD", thread_id, anon_sender, receiver, message)
                c.execute('INSERT INTO anon_messages VALUES (null,?,?,?,?,?)', data)
                conn.commit()

                await user.send(f'You got an anonymous message! Thread: {thread_id}\nMessage:\n{message}\nUse `!reply {thread_id} <msg>` to respond')
                await anon.send('Sent! :mailbox_with_mail:')
            except AttributeError:
                await ctx.send(f'A user with that name could not be found.')
            conn.close()


def setup(bot):
    bot.add_cog(DM(bot))
