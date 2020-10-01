from discord import Embed, Color, Member

from cogs.embeds.event_embed import EventEmbed


class JoinEmbed(EventEmbed):
    color = Color.blue()
    event = "has joined the server"

    def __init__(self, member: Member):
        super().__init__(member=member, event=self.event, color=self.color)

    def build_embed(self, *args, **kwargs):
        super().build_embed(*args, **kwargs)
