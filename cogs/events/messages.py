from datetime import datetime
from random import randint

import discord
from discord.ext import commands

from database.users import get_xp
from database.users import increment_messages
from database.users import increment_xp
from utils.functions import create_paste_desc
from utils.functions import get_level_from_xp
from utils.logs import log
from utils.logs import paste


class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._cd = commands.CooldownMapping.from_cooldown(
            1, 60, commands.BucketType.member
        )

    def get_cooldown(self, message: discord.Message):
        """Returns the cooldown left"""
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    @commands.Cog.listener()
    async def on_message(self, message):
        cooldown = self.get_cooldown(message)
        level_up = False
        await increment_messages(message.author.id)
        if cooldown is None:
            xp_gained = randint(15, 25)
            xp = await get_xp(message.author.id)
            current_level = await get_level_from_xp(xp)
            new_level = await get_level_from_xp(xp + xp_gained)
            if new_level > current_level:
                level_up = True
            await increment_xp(message.author.id, xp_gained)
            if level_up:
                print("Levelled up")

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        amount = len(messages)
        channels = []
        user_count = {}
        list_count = ""
        for message in messages:
            if message.channel not in channels:
                channels.append(message.channel)
            if message.author.id in user_count:
                user_count[message.author.id] = user_count[message.author.id] + 1
            else:
                user_count[message.author.id] = 1
        for user_id, message_count in user_count.items():
            list_count += f"<@!{user_id}> - {message_count}\n"

        channel = (
            f"{len(channels)} channels" if len(channels) > 1 else f"<#{channels[0].id}>"
        )
        description = (
            f"`{amount}` cached messages bulk deleted from {channel}\n\n{list_count}"
        )

        text_to_paste = await create_paste_desc(messages)
        paste_url = await paste(
            name=f"{datetime.now().strftime('%d|%m - %H:%M')} Purged Messages",
            description=f"{len(messages)} messages deleted from {channel}",
            to_paste=text_to_paste,
        )
        if paste_url is not None:
            description += f"\n[Purge Log]({paste_url})"

        await log(
            client=self.client,
            title="Messages Deleted!",
            description=description,
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        message_content = message.content
        message_content += "\n" if message_content != "" else ""
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                message_content += f"{attachment.url}\n"
        await log(
            client=self.client,
            title="Message Deleted!",
            description=f"Message by {message.author} deleted from <#{message.channel.id}>\n\n"
            f"**Content**:\n"
            f"{message_content}",
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content and not before.author.bot:
            await log(
                client=self.client,
                title="Message Deleted!",
                description=f"Message by {before.author} edited in <#{before.channel.id}>\n\n"
                f"**Before**:\n"
                f"{before.content}\n\n"
                f"**After**:\n"
                f"{after.content}",
            )


def setup(client):
    client.add_cog(Messages(client))
