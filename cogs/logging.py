#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

import os

import discord
from discord import guild, Message
from discord.ext import commands
from discord.ext.commands import bot

from cogs.embeds.join_embed import JoinEmbed
from cogs.embeds.sent_message_embed import SentMessageEmbed


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # We only care about our own guild, this bot will not be deployed on other guilds ('discord servers')
        guild = self.bot.guilds[0]
        self.channel = discord.utils.get(guild.text_channels, name=os.getenv("LOGGING_CHANNEL"))

        if self.channel is None:
            print("Logging channel not found!")
            self.cog_unload()
        print("Discord logging loaded successfully!")

    @commands.Cog.listener()
    async def on_member_join(self, member):

        event = "has joined the server"

        embed = JoinEmbed.build_embed(member, event)

        await self.channel.send(
            embed=embed
        )

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if not message.author.bot:
            event = "has sent a new message"

            embed = SentMessageEmbed().build_embed(message, event)

            await self.channel.send(
                embed=embed
            )


def setup(bot):
    bot.add_cog(Logging(bot))