from discord.ext import commands

from utils.rank_card import generate_rank_card


class Levelling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rank(self, ctx):
        await generate_rank_card(ctx.message.author)


def setup(client):
    client.add_cog(Levelling(client))
