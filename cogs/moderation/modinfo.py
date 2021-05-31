from discord.ext import commands
import discord

from database.postgres_handler import query_sql
from utils.responses import generate_error

from datetime import datetime
# import datetime as dt


async def pretty_print_date(date: datetime):
    return date.strftime("%Y-%m-%d %H:%M:%S")


class ModInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def modinfo(self, ctx, member: discord.Member = None):
        if member is None:
            return await generate_error(
                ctx,
                "Please select a valid user!",
                "‏‏‎‎"
            )

        data = query_sql(
            f"""SELECT (
                moderator_id,
                punishment_type,
                reason,
                punished_at,
                duration,
                permanent,
                expired
            ) FROM punishments WHERE user_id='{member.id}' ORDER BY punished_at ASC"""
        )

        if data is not None:
            await ctx.send(data)


def setup(client):
    client.add_cog(ModInfo(client))
