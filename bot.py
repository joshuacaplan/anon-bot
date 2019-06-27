from subprocess import Popen
import discord
from discord.ext import commands
import logging
import os
from random import randint
from Globals import prefix

try:
    discord_api = os.environ['discord']
    my_user_id = 0
except KeyError:
    from environs import Env
    env = Env()  # reads from .env file
    env.read_env()
    my_user_id = int(os.environ['my_user_id'])
    discord_api = os.environ['discord']

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')

def format_cogs(cogs_dir='cogs'):
    from glob import glob
    found_cogs = glob(f'{cogs_dir}/**/*.py', recursive=True)
    formatted_cogs = [cog.replace('.py', '').replace('\\', '.').replace('/', '.') for cog in found_cogs]
    return formatted_cogs


if __name__ == '__main__':
    import traceback
    for cog in format_cogs():
        try:
            bot.load_extension(cog)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {cog}')
            traceback.print_exc()

bot.run(discord_api)