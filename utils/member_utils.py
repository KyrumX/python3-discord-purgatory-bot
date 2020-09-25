from discord import Member


def build_full_user(member: Member):
    """Returns the full user discord name with discriminator: UserName#2234"""
    return member.name + "#" + member.discriminator