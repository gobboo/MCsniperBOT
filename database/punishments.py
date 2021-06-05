from database.postgres_handler import query_sql


async def get_history(user_id: int):
    return query_sql(
        f"SELECT * FROM punishments WHERE user_id={user_id} ORDER BY punished_at ASC",
        False,
    )


async def get_moderator(moderator_id: int):
    return query_sql(f"SELECT username FROM users WHERE user_id={moderator_id}")
