import typing

import discord
from discord.ext import commands

from utils.responses import generate_error


class Purge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["delete", "clear"])
    async def purge(
        self, ctx, next_arg: typing.Union[discord.Member, int] = None, amount=None
    ):
        if next_arg is None:
            return await generate_error(
                ctx=ctx,
                error="You must specify either an amount of messages to delete or a user!",
                example="!purge 5 | !purge @jordan#1284 5",
            )
        author = next_arg if type(next_arg) == discord.Member else None
        if amount is not None:
            try:
                amount = int(amount)
            except ValueError:
                pass
        amount = 50 if amount is None else amount
        messages = []
        message_history = await ctx.channel.history(limit=999).flatten()
        for message in message_history:
            print(message.content, len(messages))
            if len(messages) >= amount:
                break
            if author == message.author or author is None:
                messages.append(message)
            if len(messages) == amount:
                break
        await ctx.channel.delete_messages(messages)


def setup(client):
    client.add_cog(Purge(client))
