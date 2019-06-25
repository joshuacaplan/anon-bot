import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def _help(self, ctx):
        embed = discord.Embed(title='Showing All Commands:', color=0x267d28)
        # DM Command
        embed.add_field(
            name='dm', value='Sends a direct message to a user', inline=True)
        embed.add_field(
            name='Usage:', value="!dm 'name' 'message'", inline=True)

        # Reply Command
        embed.add_field(
            name='reply', value='Replies a message you received', inline=True)
        embed.add_field(
            name='Usage', value="!reply 'id/username' 'message'", inline=True)

        # Enable Messages Command
        embed.add_field(
            name='enable', value='Allows users to send you anonymous messages', inline=True)
        embed.add_field(
            name='Usage', value="!enable", inline=True)

        # Disable Messages
        embed.add_field(
            name='disable', value='Disables anonymous messaging.', inline=True)
        embed.add_field(
            name='Usage', value="!disable", inline=True)

        # Report Command
        embed.add_field(
            name='report', value='Sends message info to mods', inline=True)
        embed.add_field(
            name='Usage', value="!report 'thread id' '<optional> details'", inline=True)
        # Report Channel Command
        embed.add_field(
            name='reportchannel', value='Sets channel which all reports go to', inline=True)
        embed.add_field(
            name='Usage', value="!reportchannel '#channel'", inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
