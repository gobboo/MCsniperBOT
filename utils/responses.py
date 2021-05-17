import discord


async def generate_error(ctx, error, example=None):
    error_embed = discord.Embed(
        title="Error!", colour=int("FF0000", 16), description=error
    )
    if example is not None:
        error_embed.set_footer(text=example)
    error_embed.set_thumbnail(url="https://imgur.com/8qwtdtA")
    return await ctx.send(embed=error_embed)
