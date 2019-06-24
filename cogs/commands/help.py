import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='help')
    async def _help(self, ctx):
        embed = discord.Embed(title="Showing All Commands:", color=0x267d28)
        embed.add_field(name='dm', value='Sends a direct message to a user', inline = True)
        embed.add_field(name='Usage:', value ="!dm 'name' 'message'", inline = True)
        embed.add_field(name='reply', value='Replies a message you received', inline = True)
        embed.add_field(name='Usage', value=".reply'id' 'message'", inline = True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))