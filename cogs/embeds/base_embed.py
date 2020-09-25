import abc

from discord import Embed

class BaseEmbed(abc.ABC):
    def __init__(self):
        self.embed = Embed()

    def build_embed(self, *args, **kwargs):
        pass