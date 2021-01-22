import os

import discord
from discord.ext import commands
from discord.utils import get


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """"
        Event listener when a member joins the discord server
        Sends a welcome message in the system channel, if applicable
        Give them a default rank, if applicable
        """

        # Grab the system channel ('System Messages Channel')
        channel = member.guild.system_channel

        if channel is not None:
            await channel.send('Welcome {0.mention}, to the Kings of Purgatory Discord. \n'
                               'Feel free to join our Steam group: {1}. \n'
                               'We hope you enjoy your stay :) \n'.format(member, os.getenv("STEAM_GROUP_URL")))

        # Grab the default role
        default_role = get(member.guild.roles, name=os.getenv("DISCORD_DEFAULT_ROLE"))

        if default_role:
            await member.add_roles(default_role, reason="Giving default role!")

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