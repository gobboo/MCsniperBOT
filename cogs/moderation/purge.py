import typing
from datetime import datetime

import discord
from discord.ext import commands

from utils.functions import create_paste_desc
from utils.logs import log
from utils.logs import paste
from utils.responses import generate_error


class Purge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        aliases=["delete", "clear"], usage="!purge 5 | !purge @jordan#1284 5"
    )
    async def purge(
        self, ctx, user_or_amount: typing.Union[discord.Member, int] = None, amount=None
    ):
        if user_or_amount is None:
            return await generate_error(
                ctx=ctx,
                error="You must specify either an amount of messages to delete or a valid user!",
                example=self.purge.usage,
            )
        author = user_or_amount if type(user_or_amount) == discord.Member else None
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
            amount = user_or_amount if type(user_or_amount) == int else 50
        messages = []
        message_history = await ctx.channel.history(limit=999).flatten()
        for message in message_history:
            if len(messages) >= amount:
                break
            if author == message.author or author is None:
                messages.append(message)

        messages.reverse()

        failed_to_purge = False

        try:
            await ctx.channel.delete_messages(messages)
        except Exception as e:
            if isinstance(e, discord.errors.HTTPException):
                failed_to_purge = True
                await generate_error(
                    ctx=ctx,
                    error=str(e),
                )

        text_to_paste = ""
        for message in messages:
            timestamp = message.created_at.strftime("%H:%M")
            message_content = message.content
            if len(message.attachments) > 0:
                for attachment in message.attachments:
                    message_content += f"\n{attachment.url}"
            if message_content == "":
                message_content = "MESSAGE WAS AN EMBED"
            text_to_paste += f"[{timestamp}] {message.author.name} ({message.author.id}): {message_content}\n"
        text_to_paste = await create_paste_desc(messages)
        paste_url = await paste(
            name=f"{datetime.now().strftime('%d|%m - %H:%M')} Purged Messages",
            description=f"{len(messages)} messages deleted from #{ctx.channel.name} by {ctx.message.author}",
            to_paste=text_to_paste,
        )

        description = (
            f"{ctx.author} has purged `{len(messages)}` messages in #{ctx.channel}"
        )

        if paste_url is not None:
            description += f"\n\n[Purge Log]({paste_url})"

        await log(
            client=self.client,
            title="Moderator Command Executed!",
            description=description,
        )

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
