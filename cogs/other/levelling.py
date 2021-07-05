import io

import discord
from discord.ext import commands
from database.users import get_lb

from utils.rank_card import generate_rank_card
from utils.functions import get_level_from_xp


class Levelling(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.command()
    async def rank(self, ctx, user: discord.Member = None):
        # Need to add a rank_error func in case invalid user
        user = ctx.message.author if user is None else user
        card = await generate_rank_card(user)
        byte_array = io.BytesIO()
        card.save(byte_array, format="png")
        file = discord.File(io.BytesIO(byte_array.getvalue()), filename="rank.png")
        await ctx.send(file=file)

    @commands.command(aliases=["lb", "leaderboard"])
    async def _lb(self, ctx):
        lb = await get_lb()
        print(lb)

        user_strs = []
        rank = 0
        for person in lb:
            mention = f"<@{person[0]}>"
            level = await get_level_from_xp(person[1])
            rank += 1
            user_strs.append(f"{rank}. {mention} - lvl. {level}")

        embed = discord.Embed(
            title="🏆 Levels Leaderboard",
            description="\n".join(user_strs),
            color=0x7cacd4
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Levelling(client))
