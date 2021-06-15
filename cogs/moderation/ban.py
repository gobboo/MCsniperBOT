from discord.ext import commands
import discord

from utils.time import FutureTime
from utils.responses import generate_error, generate_success
from database.punishments import insert_punishment, set_expired
from typing import Union

from datetime import datetime


# Code from Robo Danny
class BannedMember(commands.Converter):
    async def convert(self, ctx, argument):
        if argument.isdigit():
            member_id = int(argument, base=10)
            try:
                return await ctx.guild.fetch_ban(discord.Object(id=member_id))
            except discord.NotFound:
                raise commands.BadArgument('This member has not been banned before.') from None

        ban_list = await ctx.guild.bans()
        entity = discord.utils.find(lambda u: str(u.user) == argument, ban_list)

        if entity is None:
            raise commands.BadArgument('This member has not been banned before.')
        return entity


class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, duration: Union[FutureTime, None, str] = None, *, reason: Union[str, None] = None):

        if member == ctx.author:
            return await generate_error(ctx, "You can't ban yourself, lol.")

        if isinstance(duration, str):
            reason = duration
            duration = None

        reason = reason or "Unspecified"

        seconds_til_unban = f"{round((duration.dt - datetime.utcnow()).seconds)}," if duration is not None else ""

        await insert_punishment(
            user_id=member.id,
            moderator_id=ctx.author.id,
            guild_id=ctx.guild.id,
            punishment_type='ban',
            reason=reason,
            duration=seconds_til_unban,
            permanent=duration is None
        )

        try:
            if not member.dm_channel:
                dm = await member.create_dm()
            if member.dm_channel:
                dm = member.dm_channel

            await dm.send(
                embed=discord.Embed(
                    title=f"You were banned from {ctx.guild.name}",
                    description=f"{member.mention}, you were banned from {ctx.guild.name}\n**Reason: ** {reason}"
                )
            )
        except Exception as e:
            print(e)

        try:
            await ctx.guild.ban(member, reason=reason)
        except (AttributeError, discord.HTTPException) as e:
            print(e)

        await generate_success(ctx, f"Successfully banned {member.mention} for \"{reason}\"")

    @ban.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            return await generate_error(ctx, "You are missing the required permissions to ban members!")

        print(error)

    # Code from Robo Danny
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, member: BannedMember, *, reason: str = None):
        if reason is None:
            reason = "Unspecified"

        await ctx.guild.unban(member.user, reason=reason)

        await set_expired(member.user.id, 'ban')

        return await generate_success(ctx, f"**Successfully unbanned: **{member.user}\n**ID: **{member.user.id}\n**Ban Reason: **{member.reason}")


def setup(client):
    client.add_cog(Ban(client))
