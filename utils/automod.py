from config import MOD_RULES
import discord


async def automod(message):
    for rule in MOD_RULES:
        if rule["l"](message.content):
            await message.delete()
            await message.author.send(embed=discord.Embed(
                title="Message flagged",
                description=f"Your message was flagged and deleted due to this reason:\n\n```{rule['m']}```",
                color=0xcf6c6c
            ))
            if rule.get('severity', 0) > 0:
                pass
