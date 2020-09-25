from discord import Color, Embed

from cogs.embeds.base_embed import BaseEmbed


class BaseInfoEmbed(BaseEmbed):
    color = Color.blue()

    def __init__(self):
        super().__init__()

    def build_embed(self, *args, **kwargs):
        self.embed.colour = self.color

