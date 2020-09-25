from discord import Embed, Member, Message

from cogs.embeds.base_info_embed import BaseInfoEmbed
from utils.member_utils import build_full_user


class SentMessageEmbed(BaseInfoEmbed):
    def __init__(self):
        super().__init__()

    def build_embed(self, message: Message, event: str) -> Embed:
        super().build_embed()

        self.embed.set_author(name=build_full_user(message.author))
        self.embed.title = message.author.display_name + " " + event

        self.embed.add_field(name="Channel", value=message.channel.name)

        self.embed.set_footer(text="User ID: " + message.author.id.__str__())

        return self.embed