from database.postgres_handler import query_sql, execute_sql


async def get_history(user_id: int):
    return query_sql(
        f"SELECT * FROM punishments WHERE user_id={user_id} ORDER BY punished_at ASC",
        one=False
    )


async def get_moderator(moderator_id: int):
    return query_sql(f"SELECT username FROM users WHERE user_id={moderator_id}")


async def insert_punishment(user_id, moderator_id, guild_id, punishment_type, reason, duration, permanent):
    execute_sql(
        f"""
            INSERT INTO punishments (
                user_id,
                moderator_id,
                guild_id,
                punishment_type,
                reason,
                punished_at,
                {'duration,' if duration != '' else ''}
                permanent) VALUES (
                {user_id},
                {moderator_id},
                {guild_id},
                '{punishment_type}',
                '{reason}',
                'now',
                {duration}
                {'true' if duration == '' else 'false'});"""
    )


async def set_expired(user_id, punishment_type):
    execute_sql(f"""
    UPDATE punishments
    SET expired = true
    WHERE user_id = {user_id} and punishment_type = '{punishment_type}'
    """)
