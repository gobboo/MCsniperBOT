from datetime import datetime
from random import randint

import discord
from discord.ext import commands
from discord.utils import get

from config import LOGS_CHANNEL_ID
from database.users import get_captcha_data
from database.users import get_xp
from database.users import increment_attempts
from database.users import increment_messages
from database.users import increment_xp
from database.users import require_captcha
from utils.functions import create_paste_desc
from utils.functions import get_level_from_xp
from utils.logs import log
from utils.logs import paste
from database.postgres_handler import execute_sql


from config import MEMBER_ROLE


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
        # Levels
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

        # Verify
        # TODO: allow users to retry
        if isinstance(
            message.channel, discord.channel.DMChannel
        ) and await require_captcha(message.author.id) and message.author != self.client.user:
            user_id_from_db, captcha, attempts = await get_captcha_data(
                message.author.id
            )
            print(message.author.id)
            print(user_id_from_db, captcha, attempts)
            if user_id_from_db is not None:
                if attempts < 5:
                    if message.content.strip().lower() == captcha:
                        await message.channel.send(
                            embed=discord.Embed(
                                title="Success!",
                                description=f"{message.author.mention}, you are now verified!",
                            )
                        )
                        logs_channel = await self.client.fetch_channel(
                            int(LOGS_CHANNEL_ID)
                        )
                        # TODO: send logs for attempts / success
                        await get(
                            logs_channel.guild.members, id=message.author.id
                        ).add_roles(
                            get(logs_channel.guild.roles, name=MEMBER_ROLE)
                        )
                        await log(
                            self.client,
                            "Verified!",
                            f"{message.author.mention} successfully verified with account age {datetime.utcnow() - message.author.created_at}"
                        )
                        execute_sql(f"DELETE FROM captcha_users WHERE user_id={message.author.id};")
                    else:
                        await message.channel.send(
                            embed=discord.Embed(
                                title="Fail!",
                                description=":x: Incorrect captcha answer!",
                            )
                        )
                        await increment_attempts(message.author.id)
                        await log(self.client, "Failed verification", f"{message.author.mention} failed authentication\n`Tries`: {attempts}")
                else:
                    await message.channel.send(
                        embed=discord.Embed(
                            title="Too many attempts!",
                            description="Please contact a moderator to be verified.",
                        )
                    )

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
