from discord.ext import commands
import discord

from database.punishments import warn_user, warn_count, insert_punishment
from utils.responses import generate_success, generate_error

from config import MUTE_ROLE, MOD_LOGS_CHANNEL_ID
from discord.utils import get

from utils.logs import log


class Warn(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def warn(self, ctx, user: discord.Member, *, reason: str = "Unspecified"):
        await warn_user(user.id, ctx.author.id, ctx.guild.id, reason)

        warnings = await warn_count(user.id)

        if warnings >= 3:
            await generate_success(ctx, f"Warned {user.mention} for {reason}")
            muted = get(ctx.guild.roles, name=MUTE_ROLE)
            mod_logs = get(ctx.guild.channels, id=MOD_LOGS_CHANNEL_ID)

            if muted in user.roles:
                return await generate_error(ctx, f"Failed to mute | {user.mention} is already muted!")

            reason = "Reached Max Warnings!"

            seconds_til_unmute = ""

            await insert_punishment(
                user_id=user.id,
                moderator_id=ctx.author.id,
                guild_id=ctx.guild.id,
                punishment_type='mute',
                reason=reason,
                duration=seconds_til_unmute,
                permanent=True,
            )

            try:
                await user.add_roles(muted, reason=reason)
            except (AttributeError, discord.HTTPException) as e:
                print(e)

            await log(
                self.client,
                title=f"{user.name} was muted",
                description=f"{user.mention} ({user.id}) was muted\n**Reason: **{reason}\n**Muted Until: **NIL",
                color=int("CF6C6C", 16),
                custom_log_channel=mod_logs
            )
            await generate_success(ctx, f"Muted {user.mention} due to them having 3 or more warnings!")
        else:
            await generate_success(ctx, f"Warned {user.mention} for {reason} ({3 - warnings} warnings left until mute)")


def setup(client):
    client.add_cog(Warn(client))
