from datetime import datetime

import discord
import aiohttp

from config import LOGO
from config import LOGS_CHANNEL
from config import PASTE_API_KEY


async def log(client, title, description):
    c = await client.fetch_channel(int(LOGS_CHANNEL))
    emb = discord.Embed(
        title=title,
        colour=int("19C7FC", 16),
        description=description,
        timestamp=datetime.utcnow(),
    )
    emb.set_footer(text="​", icon_url=LOGO)
    return await c.send(embed=emb)


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
            async with s.post("https://api.paste.gg/v1/pastes", headers=headers, json=data) as post_paste:
                if post_paste.status == 201:
                    post_paste_json = await post_paste.json()
                    paste_id = post_paste_json["result"]["id"]
                    print("Hey")
                    return f"https://paste.gg/{paste_id}"
        return None
    return None
