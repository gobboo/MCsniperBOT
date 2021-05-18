# import discord
from discord.ext import commands

from utils.logs import log


class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        amount = len(payload.message_ids)
        cached_messages = payload.cached_messages
        user_count = {}
        list_count = ""
        for message in cached_messages:
            if message.author.id in user_count:
                user_count[message.author.id] = user_count[message.author.id] + 1
            else:
                user_count[message.author.id] = 1
        for user_id, message_count in user_count.items():
            list_count += f"<@!{user_id}> - {message_count}\n"
        await log(
            client=self.client,
            title="Messages Deleted!",
            description=f"`{amount}` messages bulk deleted from <#{payload.channel_id}>\n\n{list_count}",
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        print(message.content)


def setup(client):
    client.add_cog(Messages(client))
