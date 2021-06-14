from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.postgres_handler import query_sql, execute_sql
from database.punishments import set_expired
from config import MUTE_ROLE, MOD_LOGS_CHANNEL_ID
from utils.logs import log
from datetime import timedelta, datetime
from discord.utils import get


class RemovePunishment(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(
            self.punishment_remove_check, trigger="cron", minute="*"
        )
        self.scheduler.start()

    async def punishment_remove_check(self):
        to_check = query_sql("""
                SELECT user_id, punishment_type, punished_at, duration, guild_id, punishment_id FROM punishments
                WHERE punishment_type='mute' AND permanent=false AND expired=false AND duration IS NOT NULL
                OR punishment_type='ban' AND permanent=false AND expired=false AND duration IS NOT NULL;
                """, one=False)

        for punishment in to_check:
            punishment_id = punishment[5]
            user = punishment[0]
            punishment_type = punishment[1]
            punished_at = punishment[2]
            duration = punishment[3]
            guild = punishment[4]
            print(f"""User: {user}
Type: {punishment_type}
Punished At: {punished_at}
Duration: {duration}
Guild: {guild}""")

            print(datetime.utcnow() >= punished_at + timedelta(seconds=duration))
            if datetime.utcnow() >= punished_at + timedelta(seconds=duration):
                mod_logs = get(get(self.client.guilds, id=guild).channels, id=MOD_LOGS_CHANNEL_ID)
                if punishment_type == "ban":
                    await get(self.client.guilds, id=guild).unban(get(self.client.users, id=user), reason="Ban expired")
                    execute_sql(f"UPDATE punishments SET expired = true WHERE punishment_id = {punishment_id}")
                    await set_expired(user, 'ban')
                elif punishment_type == "mute":
                    guild = get(self.client.guilds, id=guild)
                    muted = get(guild.roles, name=MUTE_ROLE)
                    await get(guild.members, id=user).remove_roles(muted, reason="Mute expired")
                    await set_expired(user, 'mute')
                    await log(
                        self.client,
                        title=f"<@{user}> (ID: {user}) was auto unmuted",
                        description=f"<@{user}> was unmuted\n**Reason: **Mute expired",
                        color=int("CF6C6C", 16),
                        custom_log_channel=mod_logs
                    )


def setup(client):
    client.add_cog(RemovePunishment(client))
