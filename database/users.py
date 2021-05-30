from database.postgres_handler import execute_sql
from database.postgres_handler import query_sql

from ast import literal_eval as make_tuple

"""
Generic / Reusable Queries
"""


async def increment_column(
    table: str, column: str, amount: int, condition: str
) -> None:
    execute_sql(f"UPDATE {table} SET {column}={column} + {amount} {condition}")


"""
Levelling System Queries
"""


async def user_exists(user_id: int) -> bool:
    if query_sql(f"SELECT * FROM users WHERE user_id={user_id}") is None:
        return False
    return True


async def create_user(user_id: int):
    execute_sql(f"INSERT INTO users VALUES({user_id}, 0, 0)")


async def get_xp(user_id: int) -> int:
    if not await user_exists(user_id):
        await create_user(user_id)
    return query_sql(f"SELECT experience FROM users WHERE user_id={user_id};")[0]


async def get_user_count() -> int:
    """
    Get number of users in database
    """
    return query_sql("SELECT COUNT (*) FROM USERS")[0]


class ThisShouldntHappen(Exception):
    pass


async def get_user_rank(user_id: int) -> (int, int):
    """
    Get user rank in db

    e.g. 100 would be they have the 100th highest xp in the db
    """

    if not await user_exists(user_id):
        await create_user(user_id)

    total_count = await get_user_count()

    all_users_experience = sorted(query_sql("SELECT (experience, user_id) FROM users;", one=False), key=lambda u: u[0]).reverse()
    i = 1
    print(all_users_experience)
    for u in all_users_experience:
        if make_tuple(u[0])[1] == user_id:
            return i, total_count
        i += 1

    raise ThisShouldntHappen

"""
Captcha Queries
"""


async def get_captcha_data(user_id: int) -> list:
    return query_sql(
        f"SELECT user_id, captcha, attempts FROM captcha_users WHERE user_id={user_id}"
    )


async def require_captcha(user_id: int) -> bool:
    if query_sql(f"SELECT * FROM captcha_users WHERE user_id={user_id}") is None:
        return False
    return True


async def set_captcha(user_id: int, captcha: str) -> None:
    if await get_captcha_data(user_id) is not None:
        return execute_sql(
            f"UPDATE captcha_users SET captcha='{captcha}', attempts=0 WHERE user_id={user_id}"
        )
    return execute_sql(
        f"INSERT INTO captcha_users (user_id, captcha, attempts) VALUES ({user_id}, '{captcha}', 0)"
    )


async def captcha_completed(user_id: int) -> None:
    execute_sql(f"DELETE FROM captcha_users WHERE user_id={user_id}")
