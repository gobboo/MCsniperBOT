# import discord
from discord.ext import commands


class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        print(len(payload.message_ids))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        print(message.content)


def setup(client):
    client.add_cog(Messages(client))
