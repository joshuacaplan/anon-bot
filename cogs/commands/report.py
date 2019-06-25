import discord
import sqlite3
from discord.ext import commands


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def report(self, ctx):
        if type(ctx.channel) is discord.DMChannel:
            await ctx.send(f"Send your message in a server!")
        try:
            conn = sqlite3.connect('anon.db')
            c = conn.cursor()
            args = ctx.message.content.split(' ')
            thread_id, details = args[1], ' '.join(
                args[2:]) or 'No details given'
            author = ctx.author
            reporter = author.id
            anon_id = c.execute(
                f"SELECT anon_sender FROM threads WHERE thread_id={thread_id}").fetchone()[0]
            anon = discord.utils.get(self.bot.users, id=anon_id)
            report_channel_id = c.execute(
                f"SELECT report_channel_id FROM guildOptions WHERE guild_id={ctx.guild.id}").fetchone()[0]

            if report_channel_id is not None:
                report_channel = discord.utils.get(
                    ctx.guild.text_channels, id=report_channel_id)
            else:
                await ctx.send(f'Report channel has not been set up! Message a server administrator to have one set.')
                await ctx.message.delete()

            # insert report data
            report_data = (thread_id, anon_id, reporter, details)
            c.execute(
                'INSERT INTO reports VALUES (null,?,?,?,?)', report_data)
            conn.commit()

            embed = discord.Embed(
                title=f"Report inbound! | Thread ID: {thread_id}", color=0xcc3c3c,
                description=f'Additional Details: {details}')

            thread_length = len(c.execute(
                f"SELECT message_id FROM messages WHERE thread_id={thread_id}").fetchall())

            # iterate through all thread messages in order oldest -> newest
            for x in range(thread_length):
                message_content = c.execute(
                    f"SELECT message FROM messages WHERE thread_id={thread_id} AND message_id = {x + 1}").fetchone()[0]
                user_id = c.execute(
                    f"SELECT sender FROM messages WHERE thread_id={thread_id} AND message_id = {x + 1}").fetchone()[0]
                user = discord.utils.get(self.bot.users, id=user_id)

                # add a field for each message
                embed.add_field(
                    name=f'@{user.name}#{user.discriminator}:', value=message_content, inline=False)
            await report_channel.send(embed=embed)
            await ctx.send('Report sent! :mailbox_with_mail:')

        except AttributeError:
            await ctx.send(f'Unknown message thread!')
        conn.close()


def setup(bot):
    bot.add_cog(Report(bot))
