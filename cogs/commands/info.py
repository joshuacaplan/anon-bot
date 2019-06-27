import discord
from discord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['devs', 'credits', 'bot'])
    async def info(self, ctx):
        embed = discord.Embed(title='Anonymous Messaging Bot', color=0x267d28)
        embed.add_field(
            name='Info:', value='A bot which allows users to send anonymous messages to others within a server! Inspired by "Yolo" on Snapchat.', inline=False)
        embed.add_field(
            name='Developers:', value="- Satoshi#1337\n- atom#0001\n- TheStrplum213#6169\n- eli#4591", inline=False)
        embed.add_field(
            name='GitHub', value='https://github.com/LaughingLove/anon-bot\nCreated during Discord Hack Week', inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
