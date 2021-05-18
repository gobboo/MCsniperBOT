import discord

from config import LOGO


async def generate_error(ctx, error, example=None):
    error_embed = discord.Embed(
        title="Error!", colour=int("fb607f", 16), description=error
    )
    if example is not None:
        error_embed.set_footer(text=example, icon_url=LOGO)
    else:
        error_embed.set_footer(text="​", icon_url=LOGO)
    return await ctx.send(embed=error_embed)
