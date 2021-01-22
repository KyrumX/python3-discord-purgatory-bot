from discord.ext import commands


class MinecraftCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role("Administrator")
    async def startserver(self, ctx, argument):
        pass


def setup(bot):
    bot.add_cog(MinecraftCog(bot))