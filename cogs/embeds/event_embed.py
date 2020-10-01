import abc
import datetime

from discord import Color, Embed, Member

from cogs.embeds.base_embed import BaseEmbed
from utils.member_utils import build_full_user


class EventEmbed(BaseEmbed):
    def __init__(self,
                 member: Member,
                 event: str,
                 color: Color):
        super().__init__(color)
        self.member = member
        self.event = event
        self.user_with_discriminator = build_full_user(member)

    def _set_footer(self):
        self.embed.set_footer(text="User ID: " + self.member.id.__str__())
        self.embed.timestamp = datetime.datetime.now()

    def _set_author(self):
        self.embed.set_author(name=self.user_with_discriminator)

    def build_embed(self, *args, **kwargs):
        self._set_author()
        self._set_footer()

        self.embed.title = self.member.display_name + " " + self.event
