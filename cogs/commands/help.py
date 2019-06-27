import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def _help(self, ctx):
        embed = discord.Embed(title="Showing All Commands:", color=0x267d28)
        # DM Command
        embed.add_field(
            name="dm", value="Sends anonymous message to a user\n***Usage***: !dm 'username#0000' 'message'", inline=False)
        # Reply Command
        embed.add_field(
            name="reply", value="Replies a message you received\n***Usage***: !reply 'thread id' 'message'", inline=False)
        # Enable Messages Command
        embed.add_field(
            name="enable", value="Enables anonymous messaging\n***Usage***: !enable", inline=False)
        # Disable Messages
        embed.add_field(
            name="disable", value="Disables anonymous messaging\n***Usage***: !disable", inline=False)
        # Checks the status of anon messaging
        embed.add_field(
            name="status", value="Checks the status of anonymous messaging\n***Usage***: !status", inline=False)
        # Report Command
        embed.add_field(
            name="report", value="Sends message info to server moderators\n***Usage***: !report 'thread id' '<optional> details", inline=False)
        # Report Channel Command
        embed.add_field(
            name="reportchannel", value="Sets channel which all reports are sent (for server moderators)\n***Usage***: !reportchannel '#channel'", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))