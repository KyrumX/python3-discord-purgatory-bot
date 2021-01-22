import abc

from discord import Embed, Color


class BaseEmbed(abc.ABC):
    def __init__(self, color: Color):
        self.embed = Embed()
        self.embed.colour = color

    @abc.abstractmethod
    def build_embed(self, *args, **kwargs):
        pass