import typing

import discord
from discord.ext import commands

from utils.responses import generate_error


class Purge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        aliases=["delete", "clear"], usage="!purge 5 | !purge @jordan#1284 5"
    )
    async def purge(
        self, ctx, next_arg: typing.Union[discord.Member, int] = None, amount=None
    ):
        if next_arg is None:
            return await generate_error(
                ctx=ctx,
                error="You must specify either an amount of messages to delete or a valid user!",
                example=self.purge.usage,
            )
        author = next_arg if type(next_arg) == discord.Member else None
        if amount is not None:
            try:
                amount = int(amount)
            except ValueError:
                return await generate_error(
                    ctx=ctx,
                    error="You must specify a valid amount!",
                    example=self.purge.usage,
                )
        else:
            amount = next_arg if type(next_arg) == int else 50
        messages = []
        message_history = await ctx.channel.history(limit=999).flatten()
        for message in message_history:
            if len(messages) >= amount:
                break
            if author == message.author or author is None:
                messages.append(message)
        await ctx.channel.delete_messages(messages)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.BadUnionArgument):
            return await generate_error(
                ctx=ctx,
                error="You must specify a valid user or amount!",
                example=self.purge.usage,
            )


def setup(client):
    client.add_cog(Purge(client))
