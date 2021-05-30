import discord
from discord.ext import commands
from discord.ext.commands import CommandInvokeError
from discord.ext.commands import MemberNotFound

from utils.responses import generate_error


class Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage="!kick @jordan#1284 [reason]")
    async def kick(self, ctx, member: discord.Member = None, reason=None):
        """
        TODO: Need to log punishments and store in table
            : Could make a function in logs.py "log_punishment", which then stores within the same function
            : Can't really test logging and storing without successfully kicking account so up to Kqzz
            : await log_punishment(moderator, offender, reason, duration)
        """

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
                error="I'm not allowed to kick that user. "
                "This is likely due to them being above me in the role "
                "hierarchy!",
                example=self.kick.usage,
            )


def setup(client):
    client.add_cog(Kick(client))
