from datetime import datetime

import aiohttp
import discord

from config import LOGO
from config import LOGS_CHANNEL_ID
from config import PASTE_API_KEY


async def log(client, title, description, color=None, custom_log_channel=None):
    logs_channel = custom_log_channel or await client.fetch_channel(int(LOGS_CHANNEL_ID))
    emb = discord.Embed(
        title=title,
        colour=color if color is not None else int("19C7FC", 16),
        description=description,
        timestamp=datetime.utcnow(),
    )
    emb.set_footer(text="​", icon_url=LOGO)
    return await logs_channel.send(embed=emb)


async def paste(name=None, description=None, to_paste=None):
    if PASTE_API_KEY != "":
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Key {PASTE_API_KEY}",
        }
        data = {
            "name": name,
            "description": description,
            "visibility": "unlisted",
            "files": [
                {"name": "paste.txt", "content": {"format": "text", "value": to_paste}}
            ],
        }
        async with aiohttp.ClientSession() as s:
            async with s.post(
                "https://api.paste.gg/v1/pastes", headers=headers, json=data
            ) as post_paste:
                if post_paste.status == 201:
                    post_paste_json = await post_paste.json()
                    paste_id = post_paste_json["result"]["id"]
                    return f"https://paste.gg/{paste_id}"
        return None
    return None
