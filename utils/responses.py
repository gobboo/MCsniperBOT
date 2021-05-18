import discord

logo = "https://cdn.discordapp.com/attachments/819654216548483083/844153348470734858/logo.png"


async def generate_error(ctx, error, example=None):
    error_embed = discord.Embed(
        title="Error!", colour=int("FF0000", 16), description=error
    )
    if example is not None:
        error_embed.set_footer(text=example)
    error_embed.set_thumbnail(url=logo)
    return await ctx.send(embed=error_embed)
