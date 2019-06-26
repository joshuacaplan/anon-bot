import discord
import sqlite3
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure


class ReportChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @has_permissions(manage_channels=True)  # bot does not need to create, edit, or delete channels
    async def reportchannel(self, ctx):
        try:
            conn = sqlite3.connect('anon.db')
            c = conn.cursor()
            args = ctx.message.content.split(' ')
            if len(args) > 1:

                channel = args[1].replace('<', '').replace('#', '').replace('>', '')

                # check if report_channel_id is None, insert data as needed.
                try:
                    report_channel = c.execute(
                        f'SELECT report_channel_id FROM guildOptions WHERE guild_id={ctx.guild.id}').fetchone()[0]

                    c.execute(
                        'UPDATE guildOptions SET report_channel_id = ? WHERE guild_id = ?', (channel, ctx.guild.id))
                except TypeError:
                    data = (ctx.guild.id, channel)
                    c.execute('INSERT INTO guildOptions VALUES (null,?,?)', data)

                conn.commit()
                await ctx.send(f'Reports will be sent to <#{channel}>')
            else:
                await ctx.send('You must have at least 1 argument in your command! Refer to !help for more information.')
        except AttributeError:
            await ctx.send(f'Unknown channel.')
        conn.close()


def setup(bot):
    bot.add_cog(ReportChannel(bot))
