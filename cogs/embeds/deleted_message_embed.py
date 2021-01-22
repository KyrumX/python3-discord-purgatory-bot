from discord import Message, Color

from cogs.embeds.message_embed import MessageEmbed


class DeleteMessageEmbed(MessageEmbed):
    color = Color.red()
    event = "has deleted a message"

    def __init__(self, message: Message):
        super().__init__(message, event=self.event, color=self.color)
