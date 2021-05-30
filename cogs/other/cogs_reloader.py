from discord.ext import commands
import os


class CogsReloader(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def _reload_cogs(self, directory: str):
        for file in os.listdir(directory):
            if file.endswith(".py"):
                self.client.reload_extension(f"{directory[2:].replace('/', '.')}.{file[:-3]}")
                print(f"=> {file[:-3]} Reloaded")
            elif not (file in ["__pycache__"] or file.endswith(("pyc", "txt"))):
                print(f"\n[{file}]")
                await self._reload_cogs(f"{directory}/{file}")

    @commands.command(usage="!reload_cogs", aliases=["r", "reload"])
    async def reload_cogs(self, ctx, directory="./cogs"):
        await self._reload_cogs(directory)
        await ctx.send("Successfully reloaded cogs")


def setup(client):
    client.add_cog(CogsReloader(client))
