from discord import FFmpegPCMAudio
from discord.ext import commands
from youtube_dl import YoutubeDL


class YoutubePlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, brief="Global command, use /help yt", description="Global command, use /help yt")
    async def yt(self, ctx):
        """The global group command of this cog, /yt (other commands)"""
        pass

    @yt.command()
    async def join(self, ctx):
        """Stops and disconnects the bot from voice"""

        #TODO: Check if already connected
        channel = ctx.message.author.voice.channel

        if channel:
            await channel.connect()

    @yt.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @yt.command(brief='Plays the audio of a youtube video', description="Plays the audio of the provided youtube link")
    async def play(self, ctx, url):
        """"
        Command: yt <url: string>
        """

        voice = ctx.voice_client

        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}

        if not voice.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            ffmpeg_url = info['formats'][0]['url']
            voice.play(FFmpegPCMAudio(ffmpeg_url, **FFMPEG_OPTIONS))
            voice.is_playing()
        else:
            await ctx.send("Already playing song")
            return

def setup(bot):
    bot.add_cog(YoutubePlayer(bot))