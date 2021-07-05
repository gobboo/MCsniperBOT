  
from datetime import datetime

import discord
from discord.ext import commands


class MCsniperBOTHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        ctx = self.context
        await ctx.send("Help command here!")

    @staticmethod
    async def command_help(ctx, command):
        emb = discord.Embed(
            title=f"Help for {command.qualified_name.capitalize()}"
        )
        emb.add_field(name="Help", value=command.help)
        emb.add_field(name="Usage", value=command.usage, inline=False)
        emb.add_field(
            name="Aliases",
            value=" ".join(command.aliases) if command.aliases else "None",
        )
        emb.set_footer(text=f"Requested by {ctx.message.author}")
        emb.timestamp = datetime.utcnow()
        await ctx.send(embed=emb, file=file)

    async def send_command_help(self, command):
        await self.command_help(self.context, command)

    async def send_group_help(self, group):
        await self.command_help(self.context, group)


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client._original_help_command = client.help_command
        client.help_command = MCsniperBOTHelp()
        client.help_command.cog = self


def setup(client):
    client.add_cog(Help(client))
