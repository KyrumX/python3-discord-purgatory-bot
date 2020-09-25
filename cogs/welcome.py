import os

import discord
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):

        # Grab the system channel ('System Messages Channel')
        channel = member.guild.system_channel

        if channel is not None:
            await channel.send('Welcome {0.mention}, to the Kings of Purgatory Discord. \n'
                               'Feel free to join our Steam group: {1}. \n'
                               'We hope you enjoy your stay :) \n'.format(member, os.getenv("STEAM_GROUP_URL")))

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member


def setup(bot):
    bot.add_cog(Welcome(bot))