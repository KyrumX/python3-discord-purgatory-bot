from discord import Message, Color
from discord.utils import escape_markdown

from cogs.embeds.event_embed import EventEmbed


class UpdatedMessageEmbed(EventEmbed):
    color = Color.orange()
    event = "has updated a message"

    def __init__(self, original_message: Message, updated_message: Message, original_message_has_content=True):
        super().__init__(original_message.author, self.event, self.color)
        self.original_message = original_message
        self.updated_message = updated_message
        self.original_message_has_content = original_message_has_content

    def build_embed(self, *args, **kwargs):
        super().build_embed(*args, **kwargs)

        self.embed.add_field(name="Channel:", value=self.original_message.channel.name)
        if self.original_message_has_content:
            original_content = self.original_message.clean_content
        else:
            original_content = "<Original message had no content!>"
        self.embed.add_field(name="Initial message:", value=escape_markdown(original_content), inline=False)
        self.embed.add_field(name="Updated message:", value=escape_markdown(self.updated_message.clean_content),
                             inline=False)

