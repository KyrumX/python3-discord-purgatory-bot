import os
import subprocess

from discord.ext import commands
from mcstatus import MinecraftServer


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.ip = os.getenv("MC_SERVER_IP", None)
        self.start_bat = os.getenv("MC_SERVER_BAT", None)

        if not self.ip or not self.start_bat:
            print("No IP or start bat file provided!")
            self.cog_unload()

        self.server = MinecraftServer.lookup(self.ip)

    @commands.command()
    @commands.has_role("Administrator")
    async def startserver(self, ctx):
        # TODO: Add time delay (e.g. command cannot be spammed!)
        try:
            self.server.ping()
            server_online = True
        except:
            server_online = False

        if server_online:
            await ctx.send('Server seems already up and running!')
        else:
            subprocess.Popen([self.start_bat])
            await ctx.send('Starting server, please wait a couple of minutes!')


def setup(bot):
    bot.add_cog(Minecraft(bot))