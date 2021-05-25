from datetime import datetime

import discord

from config import LOGO


async def generate_error(ctx, error, example=None):
    error_embed = discord.Embed(
        title="Error!",
        colour=int("a12118", 16),
        description=error,
        timestamp=datetime.utcnow(),
    )
    if example is not None:
        error_embed.set_footer(text=example, icon_url=LOGO)
    else:
        error_embed.set_footer(text="​", icon_url=LOGO)

    return await ctx.send(embed=error_embed)


async def generate_success(ctx, success_message):
    success_embed = discord.Embed(
        title="Success!",
        colour=int("2a8c3a", 16),
        description=success_message,
        timestamp=datetime.utcnow(),
    )
    success_embed.set_footer(text="​", icon_url=LOGO)
    return await ctx.send(embed=success_embed)
