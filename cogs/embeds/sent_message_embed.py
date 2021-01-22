from discord import Message, Color

from cogs.embeds.message_embed import MessageEmbed


class SentMessageEmbed(MessageEmbed):
    color = Color.green()
    event = "has sent a new message"

    def __init__(self, message: Message):
        super().__init__(message, event=self.event, color=self.color)
