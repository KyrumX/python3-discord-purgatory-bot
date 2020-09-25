import datetime

from discord import Embed, Color, Member

from cogs.embeds.base_info_embed import BaseInfoEmbed
from utils.member_utils import build_full_user


class JoinEmbed(BaseInfoEmbed):
    def __init__(self):
        super().__init__()

    def build_embed(self, member: Member, event: str) -> Embed:
        embed = Embed()
        embed.set_author(name=build_full_user(member))
        embed.title = member.display_name + " " + event

        embed.set_footer(text="User ID: " + member.id.__str__())

        return embed