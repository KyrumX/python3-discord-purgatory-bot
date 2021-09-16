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

        await self.clear(ctx)

        await ctx.voice_client.disconnect()

        await ctx.send("Disconnected.")

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
            return video_url

    @yt.command(brief='Skip the current song',
                description="Skips the current song and starts the next song")
    async def skip(self, ctx):
        """"
        Stops the current song and goes to the next one, if applicable
        """
        if ctx.voice_client is not None:
            voice = ctx.voice_client
            voice.stop()

            await ctx.send("Skipping...")
            self.play_next(ctx)

    @yt.command(brief='Pause the music playback',
                description="Pauses the current music track")
    async def pause(self, ctx):
        """"
        Pauses playback
        """
        voice = ctx.voice_client

        if not voice.is_paused():
            await ctx.send("Pausing...")
            voice.pause()
        else:
            await ctx.send("Already paused.")

    @yt.command(brief='Resume the music playback',
                description="Resumes the current music track")
    async def resume(self, ctx):
        """"
        Resumes playback
        """
        voice = ctx.voice_client

        if not voice.is_paused():
            await ctx.send("Already playing.")
        else:
            await ctx.send("Resuming the music...")
            voice.resume()

    @yt.command(brief='Purges the queue',
                description="Clears the queue of songs to be played")
    async def clear(self, ctx):
        """"
        Clears the queue
        """
        self.queue.clear()

        await ctx.send("Queue cleared.")

    @play.before_invoke
    @pause.before_invoke
    @skip.before_invoke
    @resume.before_invoke
    @clear.before_invoke
    async def play_back_checks(self, ctx):
        await self.ensure_bot_active_voice(ctx)
        await self.ensure_author_same_voice_bot(ctx)

    async def ensure_bot_active_voice(self, ctx):
        """"
        Ensures the following:
            Bot is active in a voice channel, if not connect it to the author's vc, if applicable
        """
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel!")
                raise commands.CommandError("Author not connected to valid voice channel.")

    async def ensure_author_same_voice_bot(self, ctx):
        """"
        Ensures the following:
            Bot is connected to the same voice channel as the author
        """
        if not ctx.author.voice or ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.send("You are not in the same channel as the bot.")
            raise commands.CommandError("Bot is in a different channel than the author.")


def setup(bot):
    bot.add_cog(YoutubePlayer(bot))