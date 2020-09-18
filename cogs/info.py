import os

import discord
from discord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["About"], help='Information about this bot')
    async def about(self, ctx):
        """General information about this bot"""
        embed = discord.Embed()
        embed.set_author(name="Alluminator", url="https://github.com/kyrumx")
        embed.colour = discord.Color.red()
        embed.description = "https://github.com/KyrumX/python3-discord-purgatory-bot \n" \
                            "This is the official bot of Kings of Purgatory, written by Alluminator#9301 \n" \
                            "Use '/help' to get started!"
        embed.set_thumbnail(url="https://avatars2.githubusercontent.com/u/8724984?s=460&u"
                                "=38dc9c035803129e3cf0400c2a84e0e4e861cbd4&v=4")
        embed.set_footer(text="Made with Python 3 / discord.py")
        await ctx.send(
            embed=embed
        )