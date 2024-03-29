import logging
import os

from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
from dotenv import load_dotenv
import discord

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
bot = commands.Bot(command_prefix="/", intents=intents)

initial_extensions = ['cogs.welcome',
                      'cogs.info',
                      'cogs.minecraft',
                      'cogs.youtubeplayer']


@bot.command(name='iloveyou', help='If you need some love <3')
async def iloveyou(ctx):
    msg = "I love you too, {}".format(ctx.message.author.mention)
    await ctx.send(msg)


@bot.command(name='whatdowehate', help='I, the bot of truth, will tell you what we really hate!')
async def whatdowehate(ctx):
    id = '<@374550002208342026>'
    msg = "When {} rushes mid, we all die a little inside...".format(id)
    await ctx.send(msg)


@bot.command(name='list', help='[ADMIN ONLY] Responds with a list of users/userids')
@has_permissions(administrator=True)
async def list(ctx):
    members = ctx.guild.members

    msg = ""

    for member in members:
        msg += member.display_name + " - " + member.id.__str__() + " \n"

    await ctx.send(msg)


@list.error
async def list_error(ctx, error):
    if isinstance(error, CheckFailure):
        msg = "You do not have permission for this command, {}".format(ctx.message.author.mention)
        await ctx.send(msg)

# Logging
log = logging.getLogger('LOG')
log.setLevel(logging.INFO)

# Load .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Load cogs
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion discord.py: {discord.__version__}\n')

    bot.load_extension('cogs.logging')

bot.run(TOKEN)
