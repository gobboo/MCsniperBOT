import io

import discord
from discord.ext import commands

from utils.rank_card import generate_rank_card


class Levelling(commands.Cog):
    def __init__(self, client):
        self.client = client

    #@commands.command()
    async def rank(self, ctx, user: discord.Member = None):
        # Need to add a rank_error func in case invalid user
        user = ctx.message.author if user is None else user
        card = await generate_rank_card(user)
        byte_array = io.BytesIO()
        card.save(byte_array, format="png")
        file = discord.File(io.BytesIO(byte_array.getvalue()), filename="rank.png")
        await ctx.send(file=file)


def setup(client):
    client.add_cog(Levelling(client))
