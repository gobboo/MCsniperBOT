import io
from datetime import datetime

import discord
from discord.ext import commands

from database.punishments import get_history
from utils.functions import draw_history
from utils.responses import generate_error

# import datetime as dt


async def pretty_print_date(date: datetime):
    return date.strftime("%Y-%m-%d %H:%M:%S")


class ModInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        aliases=["history", "hist", "his", "logs"], usage="!modinfo @jordan#1284"
    )
    async def modinfo(self, ctx, member: discord.Member = None):
        # member = ctx.message.author  # For debugging / easier testing
        if member is None:
            return await generate_error(
                ctx=ctx,
                error="Please select a specify a valid user!",
                example=self.modinfo.usage,
            )
        history = await get_history(member.id)
        if history:
            card = await draw_history(str(member), history)
            byte_array = io.BytesIO()
            card.save(byte_array, format="png")
            file = discord.File(
                io.BytesIO(byte_array.getvalue()), filename="history.png"
            )
            await ctx.send(file=file)


def setup(client):
    client.add_cog(ModInfo(client))
