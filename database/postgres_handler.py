import logging

import psycopg2

from config import DATABASE
from config import HOST
from config import PASSWORD
from config import USER


def create_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            f"dbname={DATABASE} user={USER} password={PASSWORD} host={HOST}"
        )
    except (Exception, psycopg2.DatabaseError) as error:
        return logging.critical(f"Postgres has produced an error (startup) ~ {error}")
    return conn


def execute_sql(command):
    conn = create_connection()

    cur = conn.cursor()
    try:
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        return logging.critical(f"Postgres has produced an error ({command}) ~ {error}")
    cur.close()
    conn.commit()


def query_sql(command, one=True):
    conn = create_connection()

    cur = conn.cursor()
    try:
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        return logging.critical(f"Postgres has produced an error ({command}) ~ {error}")
    if one:
        data = cur.fetchone()
    else:
        data = cur.fetchall()
    cur.close()
    return data


async def setup_tables():
    commands = (
        """
            CREATE TYPE punishment_types AS ENUM ('mute', 'warn', 'kick', 'ban')
        """,
        """
            CREATE TABLE IF NOT EXISTS punishments (
                punishment_id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                moderator_id BIGINT NOT NULL,
                punishment_type punishment_types NOT NULL,
                reason TEXT NOT NULL,
                punished_at TIMESTAMP NOT NULL,
                duration BIGINT NULL,
                permanent BOOL DEFAULT FALSE,
                expired BOOL DEFAULT FALSE
            )
        """,
    )
    for command in commands:
        execute_sql(command)
