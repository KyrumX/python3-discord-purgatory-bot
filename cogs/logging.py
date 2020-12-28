#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

import os

import discord
from discord import Message, VoiceState, Member
from discord.ext import commands

from cogs.embeds.UpdatedMessageEmbed import UpdatedMessageEmbed
from cogs.embeds.connect_embed import ConnectEmbed
from cogs.embeds.deleted_message_embed import DeleteMessageEmbed
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

        join_server_embed = JoinEmbed(member=member)
        join_server_embed.build_embed()

        await self.channel.send(
            embed=join_server_embed.embed
        )

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """"
        Event listener when a message is deleted.
        Only works with the internal cache of the bot, so won't trigger if the bot hasn't cached the message.
        """

        # Check for message.content, in case it is only a attachment
        if not message.author.bot and message.content:
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

        # Check for message.content, in case it is only a attachment
        if not message.author.bot and message.content:
            message_embed = DeleteMessageEmbed(message=message)
            message_embed.build_embed()

            await self.channel.send(
                embed=message_embed.embed
            )

    @commands.Cog.listener()
    async def on_message_edit(self, original_message: Message, updated_message: Message):
        """"
        Event listener when a message is updated.
        Only works with the internal cache of the bot, so won't trigger if the bot hasn't cached the message.
        """

        # Check for message.content, in case it is only a attachment
        if not original_message.author.bot:
            original_message_has_content = True if original_message.content else False
            message_embed = UpdatedMessageEmbed(original_message=original_message, updated_message=updated_message,
                                                original_message_has_content=original_message_has_content)
            message_embed.build_embed()

            await self.channel.send(
                embed=message_embed.embed
            )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, voice_before: VoiceState, voice_after: VoiceState):
        """"
        Event listener when a user updates their voice states.
        Events: Join, Leave, AFK, etc.
        """

        if (voice_before.channel is None and voice_after is not None) or (voice_before.channel != voice_after.channel):
            connect_channel_embed = ConnectEmbed(member, channel=voice_after.channel)
            connect_channel_embed.build_embed()

            await self.channel.send(
                embed=connect_channel_embed.embed
            )



def setup(bot):
    bot.add_cog(Logging(bot))
