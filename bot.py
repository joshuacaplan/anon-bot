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
bot.remove_command('help')

# bot.command()

def format_cog(cogs_dir='cogs'):
    import os
    found_cogs = []
    for path, dirs, files in os.walk('cogs'):
        for f in files:
            if f.endswith('.py'):
                found_cogs.append(os.path.join(path, f))
    formatted_cogs = [cog.replace('.py', '').replace('\\', '.').replace('/', '.') for cog in found_cogs]
    return formatted_cogs

if __name__ == '__main__':
    import traceback
    for cog in format_cog():
        try:
            bot.load_extension(cog)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {cog}.')
            traceback.print_exc()

bot.run(discord_api)
