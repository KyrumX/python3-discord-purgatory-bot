#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

import os

import discord
from discord import guild, Message
from discord.ext import commands
from discord.ext.commands import bot

from cogs.embeds.deleted_message_embed import DeleteMessageEmbed
from cogs.embeds.join_embed import JoinEmbed
from cogs.embeds.message_embed import MessageEmbed
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

        join_server_embed = JoinEmbed(member=member)
        join_server_embed.build_embed()

        await self.channel.send(
            embed=join_server_embed.embed
        )

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        # TODO: FIX FILES
        if not message.author.bot:
            message_embed = SentMessageEmbed(message=message)
            message_embed.build_embed()

            await self.channel.send(
                embed=message_embed.embed
            )

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        """"
        Event listener when a message is deleted.
        Only works with the internal cache of the bot, so won't trigger if the bot hasn't cached the message.
        """
        # TODO: FIX FILES
        if not message.author.bot:
            message_embed = DeleteMessageEmbed(message=message)
            message_embed.build_embed()

            await self.channel.send(
                embed=message_embed.embed
            )



def setup(bot):
    bot.add_cog(Logging(bot))
