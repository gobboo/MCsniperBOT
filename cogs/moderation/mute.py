from discord.ext import commands
import discord
from discord.utils import get

from utils.time import FutureTime
from utils.responses import generate_error, generate_success
from database.punishments import insert_punishment
from typing import Union

import time
from config import MUTE_ROLE


class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def mute(self, ctx, member: discord.Member, duration: Union[FutureTime, None, str] = None, *, reason: Union[str, None] = None):

        muted = get(ctx.guild.roles, name=MUTE_ROLE)

        if member == ctx.author:
            return await generate_error(ctx, "You can't mute yourself, lol.")

        if isinstance(duration, str):
            reason = duration
            duration = None

        reason = reason or "Unspecified"

        seconds_til_unmute = f"{round(duration.dt.timestamp() - time.time())}," if duration is not None else ""

        print(duration, reason)

        await insert_punishment(
            user_id=member.id,
            moderator_id=ctx.author.id,
            guild_id=ctx.guild.id,
            punishment_type='mute',
            reason=reason,
            duration=seconds_til_unmute,
            permanent=duration is None
        )

        try:
            # await ctx.guild.ban(member, reason=reason)
            await member.add_roles(muted, reason=reason)
            pass
        except (AttributeError, discord.HTTPException) as e:
            print(e)

        await generate_success(ctx, f"Successfully muted {member.mention} for \"{reason}\"")

    @mute.error
    async def handle_error(error):
        print(error)

    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def unmute(self, ctx, member: discord.Member, duration: Union[FutureTime, None, str] = None, *, reason: Union[str, None] = None):
        pass


def setup(client):
    client.add_cog(Mute(client))
