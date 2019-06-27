import discord
import sqlite3
from discord.ext import commands


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def report(self, ctx):
        if type(ctx.channel) is discord.DMChannel:
            await ctx.send(f'Send your message in a server!')
        try:
            conn = sqlite3.connect('anon.db')
            c = conn.cursor()
            args = ctx.message.content.split()
            if len(args) > 1:
                thread_id, details = args[1], ' '.join(args[2:]) or 'No details given'
                author = ctx.author
                anon_id = c.execute(f'SELECT anon_sender FROM threads WHERE thread_id={thread_id}').fetchone()[0]
                anon = discord.utils.get(self.bot.users, id=anon_id)
                receiver_id = c.execute(f'SELECT receiver FROM threads WHERE thread_id={thread_id}').fetchone()[0]
                receiver = discord.utils.get(self.bot.users, id=receiver_id)
                report_channel_id = c.execute(f'SELECT report_channel_id FROM guildOptions WHERE guild_id={ctx.guild.id}').fetchone()[0]

                if report_channel_id is not None:
                    report_channel = discord.utils.get(ctx.guild.text_channels, id=report_channel_id)
                else:
                    await ctx.send(f'Report channel has not been set up! Message a server administrator to have one set.')
                    await ctx.message.delete()

                # insert report data
                report_data = (thread_id, anon_id, author.id, details)
                c.execute('INSERT INTO reports VALUES (null,?,?,?,?)', report_data)
                conn.commit()

                embed = discord.Embed(
                    title=f'Report inbound! | Thread ID: {thread_id}', color=0xcc3c3c,
                    description=f'Additional Details: {details}')
                
                embed.add_field(name=f'Reported by', value=f'{author}', inline=True)
                embed.add_field(name=f'Accused', value=f'{anon if author == receiver else receiver}', inline=True)
                embed.add_field(name=f'Thread', value=':arrow_down:', inline=False)

                thread = c.execute(f'SELECT * FROM messages WHERE thread_id={thread_id}').fetchall()
                # iterate through the thread from oldest to newest message
                for message in thread:
                    user = discord.utils.get(self.bot.users, id=message[2])
                    # add a field for each message
                    embed.add_field(name=f'{user}:', value=message[3], inline=False)
                    
                await report_channel.send(embed=embed)
                await ctx.send('Report sent! :mailbox_with_mail:')
            else:
                await ctx.send('You must have at least 1 argument in your command! Refer to !help for more information.')

        except AttributeError:
            await ctx.send(f'Unknown message thread!')
        conn.close()


def setup(bot):
    bot.add_cog(Report(bot))