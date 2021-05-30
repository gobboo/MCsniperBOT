import io

import aiohttp
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from database.users import get_user_rank
from database.users import get_xp
from utils.functions import get_level_from_xp
from utils.functions import get_level_xp


async def generate_rank_card(user):
    xp = await get_xp(user.id)

    rank, total_count = await get_user_rank(user.id)

    current_level = await get_level_from_xp(xp)

    xp_required = await get_level_xp(
        current_level + 1
    )  # XP required to go from current lvl to next lvl

    xp_required_current = sum(
        [await get_level_xp(level) for level in range(current_level)]
    )
    level_xp = xp - xp_required_current

    progress = level_xp / await get_level_xp(current_level + 1)

    print(
        "-----------------------------\n"
        f"Current Level: {current_level}\n"
        f"Current XP: {xp}\n"
        f"XP Required: {xp_required}\n"
        f"You are currently {round(progress * 100)}% of the way to level {current_level + 1}\n"
        f"Rank #{rank} of {total_count}\n"
        "-----------------------------"
    )

    background = draw_rounded_rect((819, 256), 50, "#8EAAD3", outline=10)

    basefont = await get_font(17 * 2)  # Base font for text

    cropped_avatar = await get_cropped_avatar(user)
    avatar_with_border = await outline_avatar(cropped_avatar)
    background.paste(avatar_with_border, (35, 25), avatar_with_border)
    background = await gen_text(
        background, (256, 52), f"Level {current_level}", basefont, "#373737"
    )
    background = await gen_text(background, (256, 175), str(user), basefont, "#373737")
    background = await gen_text(background, (500, 52), f"Rank #{rank} / {total_count}", basefont, "#373737")
    bar = await get_bar(progress)
    background.paste(bar, (256, 110), bar)
    return background


async def get_bar(percent):
    bg = await gen_bar_background()
    overlay = await gen_bar_overlay(percent)
    if percent >= 0.05:
        bg.paste(overlay, (5, 5), overlay)
    if percent >= 0.15:
        bg = await gen_text(bg, (26, 11), f"{round(percent * 100)}%", await get_font(28), "#C4C4C4")
    return bg


async def gen_bar_overlay(percent):
    if percent > 1:
        raise OverflowError
    w, h = int(500 * percent), 30
    return draw_rounded_rect((w, h), 30, "#4D76AA", outline=None)


async def gen_bar_background():
    w, h = 500, 40
    return draw_rounded_rect((w, h), 38, "#C4C4C4", outline=None)


async def get_font(size: int):
    font_filename = "Nimbus-Sans-Light.ttf"
    font_dir = "data"
    font = ImageFont.truetype(f"./{font_dir}/{font_filename}", size)
    return font


async def gen_text(baseimage, coordinates, text, font, color):
    draw = ImageDraw.Draw(baseimage)
    draw.text(coordinates, text, font=font, fill=color)
    return baseimage


async def get_cropped_avatar(user):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            str(user.avatar_url_as(format="webp", size=1024))
        ) as resp:
            img = Image.open(io.BytesIO(await resp.read()))
    cropped_avatar = crop_avatar_numpy(img)
    return cropped_avatar


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


async def outline_avatar(image):
    to_return = Image.new(
        mode="RGBA", size=(image.width + 10, image.height + 10), color=(0, 0, 0, 0)
    )
    draw = ImageDraw.Draw(to_return)
    thickness = 8
    draw.ellipse(
        (0, 0, image.width + thickness, image.height + thickness),
        fill="#373737",
        outline="#373737",
    )
    to_return.paste(image, (int(thickness / 2), int(thickness / 2)), mask=image)
    return to_return


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


def draw_rounded_rect(dimensions, r, color, outline=None):
    background = Image.new("RGBA", dimensions, (0, 0, 0, 0))
    draw = ImageDraw.Draw(background)
    x = 0
    y = 0

    w, h = dimensions

    if outline is not None:
        draw.ellipse((x, y, x + r, y + r), fill="#373737")
        draw.ellipse((x + w - r, y, x + w, y + r), fill="#373737")
        draw.ellipse((x, y + h - r, x + r, y + h), fill="#373737")
        draw.ellipse((x + w - r, y + h - r, x + w, y + h), fill="#373737")

        draw.rectangle((x + r / 2, y, x + w - (r / 2), y + h), fill="#373737")
        draw.rectangle((x, y + r / 2, x + w, y + h - (r / 2)), fill="#373737")

        x = 5
        y = 5
        w -= outline
        h -= outline
        r -= outline

    draw.ellipse((x, y, x + r, y + r), fill=color)
    draw.ellipse((x + w - r, y, x + w, y + r), fill=color)
    draw.ellipse((x, y + h - r, x + r, y + h), fill=color)
    draw.ellipse((x + w - r, y + h - r, x + w, y + h), fill=color)

    draw.rectangle((x + r / 2, y, x + w - (r / 2), y + h), fill=color)
    draw.rectangle((x, y + r / 2, x + w, y + h - (r / 2)), fill=color)

    return background
