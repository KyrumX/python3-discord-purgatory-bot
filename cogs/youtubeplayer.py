from discord import FFmpegPCMAudio
from discord.ext import commands
from youtube_dl import YoutubeDL


class YoutubePlayer(commands.Cog):
    YDL_OPTIONS = {'format': 'bestaudio/best',
                   'noplaylist': 'True'}

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}

    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @commands.group(pass_context=True, brief="Global command, use /help yt", description="Global command, use /help yt")
    async def yt(self, ctx):
        """The global group command of this cog, /yt (sub command) (parameters)"""
        pass

    @yt.command()
    @commands.has_role("False King")
    async def join(self, ctx):
        """Stops and disconnects the bot from voice"""

        channel = ctx.message.author.voice.channel

        if channel:
            await channel.connect()

    @yt.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        self.queue.clear()

        await ctx.voice_client.disconnect()

    @yt.command(brief='Plays the audio of a youtube video, direct link or search query',
                description="Plays the audio of a youtube video, will accept direct link or search query")
    async def play(self, ctx, *args):
        """"
        Command: yt <url: string>
        Since the search query can contain spaces use *args
        """

        video_url = self.search(args)

        voice = ctx.voice_client

        if not voice.is_playing():
            await ctx.send("Playing!")
            self.queue.append(video_url)
            self.play_next(ctx)
        else:
            await ctx.send("Already playing song, adding to queue")
            self.queue.append(video_url)

    def play_next(self, ctx):
        """"
        Actual play functionality, uses a queue
        """
        if len(self.queue) >= 1:
            voice = ctx.voice_client
            song_url_ffmpeg = self.queue.pop(0)
            voice.play(FFmpegPCMAudio(song_url_ffmpeg, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx) if len(self.queue) >= 1 else None)

        else:
            return

    def search(self, search_query):
        """"
        Searches for the youtube video using the user input (search query)
        Will use the first found youtube video by the search query,
            or if the user has simply provided the direct url it will play that
        """
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                video_url = ydl.extract_info(f"ytsearch:{search_query}", download=False)['entries'][0]['formats'][0]['url']
            except:
                raise commands.CommandError("Invalid input provided for search.")
            print(video_url)
            return video_url

    @yt.command(brief='Skip the current song',
                description="Skips the current song and starts the next song")
    def pause(self, ctx):
        pass

    @play.before_invoke
    async def ensure_author_voice(self, ctx):
        """"
        Ensures that the author is actually in a voice channel
        """
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel!")
                raise commands.CommandError("Author not connected to valid voice channel.")


def setup(bot):
    bot.add_cog(YoutubePlayer(bot))