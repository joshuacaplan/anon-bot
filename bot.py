from subprocess import Popen

import discord
from discord.ext import commands
from environs import Env
import logging
import os
from random import randint

try:
    discord_api = os.environ['discord']
    my_user_id = 0
except KeyError:
    env = Env()  # reads from .env file
    env.read_env()
    my_user_id = int(os.environ['my_user_id'])
    discord_api = os.environ['discord']

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
bot = commands.Bot(command_prefix='!')
bot.remove_command("help")

# bot.command()


@bot.event
async def on_ready():
    print('Logged In')
    await bot.change_presence(activity=discord.Game('!dm to use'))


@bot.command()
async def dm(ctx):
    try:
        stuff = ctx.message.content.split(' ')
        user, message = stuff[1], ' '.join(stuff[2:])
        user = discord.utils.get(bot.users, name=user)
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
            if user_id == sender_id or discord.utils.get(bot.users, name=user_id):
                return True
        return False
        # in DMChannel, user is receiver or sender
        #

    while True:
        msg = await bot.wait_for('message', check=check)
        reply_content = ' '.join(msg.content.split()[2:])
        if msg.author == user:
            await anon.send(f'{user} said:\n{reply_content}\nUse `.reply {user} <msg>` to reply`')
        else:
            await user.send(f'{sender_id} said:\n{reply_content}\n Use `.reply {sender_id} <msg>` to reply')


@bot.command()
async def ping(ctx):
    ctx.send('pong')


@bot.command()
async def restart(ctx):
    if ctx.author.id == my_user_id:
        print('Restarting')
        await bot.change_presence(activity=discord.Game('Restarting...'))
        Popen('python bot.py')
        await bot.logout()


@bot.command(name='exit', aliases=['quit'])
async def _exit(ctx):
    if ctx.author.id == my_user_id:
        await bot.change_presence(activity=discord.Game('Exiting...'))
        await bot.logout()

@bot.command(name='help')
async def _help(ctx):
    embed = discord.Embed(title="Showing All Commands:", color=0x267d28)
    embed.add_field(name='dm', value='Sends a direct message to a user', inline = True)
    embed.add_field(name='Usage:', value ="!dm 'name' 'message'", inline = True)
    embed.add_field(name='reply', value='Replies a message you received', inline = True)
    embed.add_field(name='Usage', value=".reply'id' 'message'", inline = True)
    await ctx.send(embed=embed)


bot.run(discord_api)
