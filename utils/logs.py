from datetime import datetime

import discord
import requests

from config import LOGO
from config import LOGS
from config import PASTE_API


async def log(client, title, description):
    c = await client.fetch_channel(int(LOGS))
    emb = discord.Embed(
        title=title,
        colour=int("19C7FC", 16),
        description=description,
        timestamp=datetime.utcnow(),
    )
    emb.set_footer(text="​", icon_url=LOGO)
    return await c.send(embed=emb)


async def paste(name=None, description=None, to_paste=None):
    if PASTE_API != "":
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Key {PASTE_API}",
        }
        data = {
            "name": name,
            "description": description,
            "visibility": "unlisted",
            "files": [
                {"name": "paste.txt", "content": {"format": "text", "value": to_paste}}
            ],
        }
        post_paste = requests.post(
            "https://api.paste.gg/v1/pastes", headers=headers, json=data
        )
        if int(post_paste.status_code) == 201:
            paste_id = post_paste.json()["result"]["id"]
            return f"https://paste.gg/{paste_id}"
        return None
    return None
