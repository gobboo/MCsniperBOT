from discord.ext import commands
import discord
from discord.utils import get

from utils.time import FutureTime
from utils.responses import generate_error, generate_success
from utils.logs import log
from database.punishments import insert_punishment, set_expired
from typing import Union

from config import MUTE_ROLE, MOD_LOGS_CHANNEL_ID
from datetime import datetime, timedelta


class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def mute(self, ctx, member: discord.Member, duration: Union[FutureTime, None, str] = None, *, reason: Union[str, None] = None):

        if member == ctx.author:
            return await generate_error(ctx, "You can't mute yourself, lol.")

        if isinstance(duration, str):
            reason = duration
            duration = None

        muted = get(ctx.guild.roles, name=MUTE_ROLE)
        mod_logs = get(ctx.guild.channels, id=MOD_LOGS_CHANNEL_ID)

        if muted in member.roles:
            return await generate_error(ctx, f"{member.mention} is already muted!")

        reason = reason or "Unspecified"

        seconds_til_unmute = f"{round((duration.dt - datetime.utcnow()).seconds)}," if duration is not None else ""

        await insert_punishment(
            user_id=member.id,
            moderator_id=ctx.author.id,
            guild_id=ctx.guild.id,
            punishment_type='mute',
            reason=reason,
            duration=seconds_til_unmute,
            permanent=duration == '',
        )

        try:
            print("Sending dm")
            if not member.dm_channel:
                dm = await member.create_dm()
            if member.dm_channel:
                dm = member.dm_channel

            await dm.send(
                embed=discord.Embed(
                    title=f"You were muted in {ctx.guild.name}",
                    description=f"""{member.mention}, you were muted in {ctx.guild.name}
**Reason: ** {reason}
**Duration: **{'permanent' if seconds_til_unmute == '' else timedelta(seconds=int(seconds_til_unmute[0]))}"""
                )
            )
        except Exception as e:
            print(e)

        try:
            await member.add_roles(muted, reason=reason)
        except (AttributeError, discord.HTTPException) as e:
            print(e)

        await generate_success(ctx, f"Successfully muted {member.mention} for \"{reason}\"")
        await log(
            self.client,
            title=f"{member.name} was muted",
            description=f"{member.mention} ({member.id}) was muted\n**Reason: **{reason}\n**Muted Until: **{duration.dt if duration is not None else 'NIL'}",
            color=int("CF6C6C", 16),
            custom_log_channel=mod_logs
        )

    @mute.error
    async def handle_error(error):
        print(error)

    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def unmute(self, ctx, member: discord.Member, *, reason: Union[str, None] = None):
        muted = get(ctx.guild.roles, name=MUTE_ROLE)
        mod_logs = get(ctx.guild.channels, id=MOD_LOGS_CHANNEL_ID)
        reason = reason or "Unspecified"

        if muted not in member.roles:
            return await generate_error(ctx, f"{member.mention} is not muted!")

        await set_expired(member.id, 'mute')

        try:
            await member.remove_roles(muted, reason=reason)
        except (AttributeError, discord.HTTPException) as e:
            print(e)

        await generate_success(ctx, f"Successfully unmuted {member.mention} for \"{reason}\"")
        await log(
            self.client,
            title=f"{member.name} was unmuted",
            description=f"{member.mention} ({member.id}) was unmuted\n**Reason: **{reason}",
            color=int("ECB54D", 16),
            custom_log_channel=mod_logs
        )


def setup(client):
    client.add_cog(Mute(client))
