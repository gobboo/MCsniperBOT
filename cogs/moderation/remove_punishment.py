from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.postgres_handler import query_sql, execute_sql
from datetime import timedelta, datetime
from discord.utils import get


class Ban(commands.Cog):
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
                WHERE punishment_type='mute' OR punishment_type='ban' AND permanent=false AND expired=false;
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
Time: {punished_at}
Duration: {duration}
Guild: {guild}""")

            if datetime.utcnow() >= punished_at + timedelta(seconds=duration):
                if punishment_type == "ban":
                    await get(self.client.guilds, id=guild).unban(get(self.client.users, id=user), reason="Ban expired")
                    execute_sql(f"UPDATE punishments SET expired = true WHERE punishment_id = {punishment_id}")
            else:
                print("HAHAHA NO UNBAN / UNMUTE FOR U")


def setup(client):
    client.add_cog(Ban(client))
