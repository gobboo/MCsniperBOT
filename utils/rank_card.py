import io

import aiohttp
import numpy as np
from PIL import Image
from PIL import ImageDraw

from database.users import get_xp
from utils.functions import get_level_from_xp
from utils.functions import get_level_xp


async def generate_rank_card(user):
    xp = await get_xp(user.id)
    current_level = await get_level_from_xp(xp)
    xp_required = await get_level_xp(current_level + 1)

    background = get_background()
    async with aiohttp.ClientSession() as session:
        async with session.get(str(user.avatar_url)) as resp:
            img = Image.open(io.BytesIO(await resp.read()))

    cropped_avatar = crop_avatar_numpy(img)
    background.paste(cropped_avatar, (100, 28), cropped_avatar)
    print(
        f"Current Level: {current_level}\n"
        f"Current XP: {xp}\n"
        f"XP Required: {xp_required}"
    )
    return background


def crop_avatar(avatar):
    width, height = avatar.size
    x = (width - height) // 2
    avatar_cropped = avatar.crop((x, 0, x + height, height))

    mask = Image.new("L", avatar_cropped.size)
    mask_draw = ImageDraw.Draw(mask)
    width, height = avatar_cropped.size
    mask_draw.ellipse((0, 0, width, height), fill=255)
    avatar_cropped.putalpha(mask)

    avatar_cropped.thumbnail((203, 203), Image.ANTIALIAS)

    return avatar_cropped


def crop_avatar_numpy(img):
    np_image = np.array(img)
    h, w = img.size
    alpha = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)
    np_alpha = np.array(alpha)
    np_image = np.dstack((np_image, np_alpha))

    avatar_cropped = Image.fromarray(np_image)
    avatar_cropped.thumbnail((199, 199), Image.ANTIALIAS)
    return avatar_cropped


def get_background():
    template = Image.open("data/rankcard.jpg")
    radius = 100
    circle = Image.new("L", (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
    alpha = Image.new("L", template.size, 255)
    w, h = template.size
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(
        circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius)
    )
    template.putalpha(alpha)
    draw = ImageDraw.Draw(template)
    draw.ellipse((98, 26, 301, 22), fill="black", outline="black")

    return template


def draw_rounded_rect():
    background = Image.new("RGBA", (1024, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(background)

    x = 0
    y = 0
    r = 200
    w = 1024
    h = 256
    color = "black"

    draw.ellipse((x, y, x + r, y + r), fill=color)
    draw.ellipse((x + w - r, y, x + w, y + r), fill=color)
    draw.ellipse((x, y + h - r, x + r, y + h), fill=color)
    draw.ellipse((x + w - r, y + h - r, x + w, y + h), fill=color)

    draw.rectangle((x + r / 2, y, x + w - (r / 2), y + h), fill=color)
    draw.rectangle((x, y + r / 2, x + w, y + h - (r / 2)), fill=color)

    return background
