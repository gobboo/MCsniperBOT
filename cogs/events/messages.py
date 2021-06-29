from datetime import datetime
from random import randint

import discord
from discord.ext import commands
from discord.utils import get

from config import LOGS_CHANNEL_ID
from config import MEMBER_ROLE
from config import VERIFY_HERE_ID
from database.users import captcha_completed
from database.users import get_captcha_data
from database.users import get_xp
from database.users import increment_column
from database.users import require_captcha
from utils.functions import create_paste_desc
from utils.functions import get_level_from_xp
from utils.logs import log
from utils.logs import paste
from utils.responses import generate_success


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

    async def captcha_check(self, message):
        if message.content.lower().replace("!", "") in ("retry", "refresh", "regenerate"):
            return
        user_id_from_db, captcha, attempts = await get_captcha_data(message.author.id)
        logs_channel = await self.client.fetch_channel(int(LOGS_CHANNEL_ID))
        member = logs_channel.guild.get_member(message.author.id)
        if user_id_from_db is not None:
            if attempts < 5:
                if (
                    message.content.strip().lower() == captcha
                ):  # If user answer matches captcha

                    await generate_success(
                        message.channel,
                        f"{message.author.mention}, you are now verified!",
                    )
                    await member.add_roles(
                        get(logs_channel.guild.roles, name=MEMBER_ROLE)
                    )
                    await log(
                        self.client,
                        "Verified!",
                        f"{message.author.mention} successfully verified with account age "
                        f"{datetime.utcnow() - message.author.created_at}",
                    )
                    await captcha_completed(message.author.id)

                else:
                    await message.channel.send(
                        embed=discord.Embed(
                            title="Fail!",
                            description=":x: Incorrect captcha answer!\n\nYou can run !regenerate to get a new captcha or try this one again.",
                            colour=int("a12118", 16),
                        )
                    )
                    await increment_column(
                        table="captcha_users",
                        column="attempts",
                        amount=1,
                        condition=f"WHERE user_id={message.author.id}",
                    )
                    await log(
                        self.client,
                        "Captcha Fail",
                        f"{message.author.mention} failed authentication\n"
                        f"`Attempts`: {attempts}",
                    )
            else:
                await message.channel.send(
                    embed=discord.Embed(
                        title="Too many attempts!",
                        description="Too many attempts! Please contact a moderator to be verified.",
                        colour=int("a12118", 16),
                    )
                )

    async def grant_xp(
        self, message
    ) -> (bool, int):  # returns if leveled up or not and level
        level_up = False
        xp_gained = randint(15, 25)
        xp = await get_xp(message.author.id, message.author.name)
        current_level = await get_level_from_xp(xp)
        new_level = await get_level_from_xp(xp + xp_gained)
        if new_level > current_level:
            level_up = True

        await increment_column(
            table="users",
            column="experience",
            amount=xp_gained,
            condition=f"WHERE user_id={message.author.id}",
        )
        await increment_column(
            table="users",
            column="messages",
            amount=1,
            condition=f"WHERE user_id={message.author.id}",
        )
        if level_up:
            return True, new_level
        return False, 0

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.client.user:
            return

        if (
            isinstance(message.channel, discord.channel.DMChannel)
            or message.channel.id == VERIFY_HERE_ID
        ) and await require_captcha(message.author.id):
            return await self.captcha_check(message)

        await increment_column(
            table="users",
            column="raw_messages",
            amount=1,
            condition=f"WHERE user_id={message.author.id}",
        )

        if self.get_cooldown(message) is None:
            leveled_up, level = await self.grant_xp(message)
            if leveled_up:
                await message.channel.send(
                    f"{message.author.mention}, you levelled up to level {level}!"
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
            color=int("cc5151", 16),
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
            description=f"Message by {message.author.mention} ({message.author}) deleted from <#{message.channel.id}>\n\n"
            f"**Content**:\n"
            f"{message_content}",
            color=int("cc5151", 16),
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content and not before.author.bot:
            await log(
                client=self.client,
                title="Message Edited!",
                description=f"Message by {before.author.mention} ({before.author}) edited in <#{before.channel.id}>\n\n"
                f"**Before**:\n"
                f"{before.content}\n\n"
                f"**After**:\n"
                f"{after.content}",
            )


def setup(client):
    client.add_cog(Messages(client))
