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
        else:
            self.server = MinecraftServer.lookup(self.ip)

    @commands.group(pass_context=True, brief="Global command, use /help mc", description="Global command, use /help mc")
    async def mc(self, ctx):
        """The global group command of this cog, /mc (other commands)"""
        pass

    @mc.command(brief='[ADMIN ONLY] Start the Minecraft server', description="Admin only command to start the "
                                                                             "Minecraft server, can only be used once "
                                                                             "ever 10 minutes")
    @commands.has_role("Administrator")
    @commands.cooldown(per=600, rate=1, type=commands.BucketType.default)
    async def start(self, ctx):
        """"
        Command to start the Minecraft server, can only be used globally once every 10 minutes to prevent
        spam during startup phase

        Furthermore, this command can only be used by administrators\

        Command: mc start
        """
        try:
            self.server.ping()
            server_online = True
        except:
            server_online = False

        if server_online:
            await ctx.send('Server seems already up and running!')
        else:
            subprocess.Popen([self.start_bat], creationflags=subprocess.CREATE_NEW_CONSOLE)
            await ctx.send('Starting server, please wait a couple of minutes!')


def setup(bot):
    bot.add_cog(Minecraft(bot))