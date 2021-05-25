import io

import discord
from discord.ext import commands

from database.users import require_captcha
from database.users import set_captcha
from utils.functions import gen_captcha
from utils.responses import generate_error


class Regenerate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["retry", "refresh"])
    async def regenerate(self, ctx):
        if not await require_captcha(ctx.author.id):
            return await generate_error(
                ctx.author,
                f"You are already verified... You do not need to complete a captcha",
            )
        captcha, captcha_bytes = gen_captcha()
        embed = discord.Embed(
            description=f"You have regenerated your captcha, see the new one below.",
            color=int("19C7FC", 16),
        )

        embed.set_image(url="attachment://captcha.png")
        await ctx.author.send(
            content=ctx.author.mention,
            embed=embed,
            file=discord.File(
                io.BytesIO(captcha_bytes.getvalue()), filename="captcha.png"
            ),
        )
        await set_captcha(ctx.author.id, captcha)


def setup(client):
    client.add_cog(Regenerate(client))
