from discord import Color, Member, GroupChannel

from cogs.embeds.event_embed import EventEmbed


class ConnectEmbed(EventEmbed):
    color = Color.dark_green()
    event = "has connected to a channel"

    def __init__(self, member: Member, channel: GroupChannel):
        super().__init__(member=member, event=self.event, color=self.color)
        self.channel = channel

    def build_embed(self, *args, **kwargs):
        super().build_embed(*args, **kwargs)

        self.embed.add_field(name="Channel:", value=self.channel.name)
