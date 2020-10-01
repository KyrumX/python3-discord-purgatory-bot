from discord import Message, Member, Color
from discord.utils import escape_markdown

from cogs.embeds.event_embed import EventEmbed


class MessageEmbed(EventEmbed):
    def __init__(self, message: Message, event: str, color: Color):
        super().__init__(message.author, event, color)
        self.message = message

    def build_embed(self, *args, **kwargs):
        super().build_embed(*args, **kwargs)

        self.embed.add_field(name="Channel:", value=self.message.channel.name)
        self.embed.add_field(name="Message:", value=escape_markdown(self.message.clean_content), inline=False)