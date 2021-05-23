from database.postgres_handler import execute_sql
from database.postgres_handler import query_sql


async def user_exists(user_id: int) -> bool:
    if query_sql(f"SELECT * FROM users WHERE user_id={user_id}") is None:
        return False
    return True


async def create_user(user_id: int):
    execute_sql(f"INSERT INTO users VALUES({user_id}, 0, 0)")


async def get_xp(user_id: int) -> int:
    if not await user_exists(user_id):
        await create_user(user_id)
    return query_sql(f"SELECT experience FROM users WHERE user_id={user_id}", True)[0]


async def increment_xp(user_id: int, xp_gained: int):
    execute_sql(
        f"UPDATE users SET experience=experience + {xp_gained} WHERE user_id={user_id}"
    )


async def increment_messages(user_id: int):
    execute_sql(f"UPDATE users SET messages=messages + 1 WHERE user_id={user_id}")
