import discord
from discord.ext import commands
from discord.ext.commands import CommandInvokeError
from discord.ext.commands import MemberNotFound

from utils.responses import generate_error


class Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage=f"!kick @jordan#1284 [reason]")
    async def kick(self, ctx, member: discord.Member = None, reason=None):
        reason = "Unspecified" if reason is None else reason

        if member is None:
            return await generate_error(
                ctx=ctx,
                error="You must specify a user to kick!",
                example=self.kick.usage,
            )

        await ctx.guild.kick(user=member, reason=reason)

    @kick.error
    async def on_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            return await generate_error(
                ctx=ctx,
                error="You specified an invalid member to kick!",
                example=self.kick.usage,
            )
        if isinstance(error, CommandInvokeError):
            return await generate_error(
                ctx=ctx,
                error="I'm not allowed to kick that user.. "
                "This is likely due to them being above me in the role "
                "hierarchy!",
                example=self.kick.usage,
            )


def setup(client):
    client.add_cog(Kick(client))
