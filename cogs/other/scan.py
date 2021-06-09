from discord.ext import commands
from config import MEMBER_ROLE

from utils.responses import generate_success
from discord.utils import get


class Scan(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    async def scan(self, ctx):
        member = get(ctx.guild.roles, name=MEMBER_ROLE)
        for user in ctx.guild.members:

            if member not in user.roles:
                print(member)
                await user.add_roles(member, reason="Member was missing role!", atomic=True)

        return await generate_success(ctx, "Successfully added member role to all members of the server!")


def setup(client):
    client.add_cog(Scan(client))
