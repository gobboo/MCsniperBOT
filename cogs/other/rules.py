from discord.ext import commands
import discord

from config import RULES


class Rules(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["rules", "rule"])
    async def _rules(self, ctx, *, rules=None):
        embeds = []
        if rules is None or rules == "":
            description = "Please check out the #welcome channel for all of the rules!"
            embeds.append(discord.Embed(
                title="Rules",
                description=description,
                color=0x7CACD4
            ))

        else:
            rules = rules.split(" ")
            rules_not_found = ""
            for rule in rules:
                if rule == "":
                    continue
                rule = rule.strip().replace(".", "")
                description = RULES.get(rule.lower(), f"Rule not found! Please refer to #welcome for rule \"{rule}\"")
                if "Rule not found!" not in description:
                    embeds.append(discord.Embed(
                        title=f"Rule {rule.upper()}",
                        description=description,
                        color=0x7CACD4
                    ))

        for embed in embeds:
            await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(Rules(client))
