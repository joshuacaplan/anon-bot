import discord
from discord.ext import commands

from random import randint

class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def dm(self, ctx):
        try:
            stuff = ctx.message.content.split(' ')
            user, message = stuff[1], ' '.join(stuff[2:])
            user = discord.utils.get(self.bot.users, name=user)
            anon = ctx.author
            # check if receiver is in db for a random number
            # if not found, create a random_number for user and add it to database
            sender_id = ''.join((str(randint(0, 9)) for _ in range(10)))
            # add receiver id to db
            await user.send(
                f'You got an anonymous message from {sender_id}:\n{message}\nUse `.reply {sender_id} <msg>` to reply')
        except AttributeError:
            await ctx.send(f'A user with that name could not be found.')

        # add sender to db
        # add receiver to db
        # create a random number for the sender and receiver so
        # Start new DM thread if none exists

        def check(m):
            content = m.content
            if content.startswith('.reply') and type(m.channel) == discord.DMChannel:
                user_id = content.split()[1]
                if user_id == sender_id or discord.utils.get(self.bot.users, name=user_id):
                    return True
            return False
            # in DMChannel, user is receiver or sender
            #

        while True:
            msg = await self.bot.wait_for('message', check=check)
            reply_content = ' '.join(msg.content.split()[2:])
            if msg.author == user:
                await anon.send(f'{user} said:\n{reply_content}\nUse `.reply {user} <msg>` to reply`')
            else:
                await user.send(f'{sender_id} said:\n{reply_content}\n Use `.reply {sender_id} <msg>` to reply')

def setup(bot):
    bot.add_cog(DM(bot))