from discord.ext import commands
from discord.utils import get


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.add_roles(get(member.guild.roles, name="Member"))


def setup(client):
    client.add_cog(Welcome(client))
