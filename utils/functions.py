import io
import random
from datetime import datetime

from claptcha import Claptcha
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from database.punishments import get_moderator


async def create_paste_desc(messages):
    text_to_paste = ""
    messages.reverse()
    for message in messages:
        timestamp = message.created_at.strftime("%H:%M")
        message_content = message.content
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                message_content += f"\n{attachment.url}"
        if message_content == "":
            message_content = "MESSAGE WAS AN EMBED"
        text_to_paste += f"[{timestamp}] {message.author.name} ({message.author.id}): {message_content}\n"
    return text_to_paste


async def get_level_xp(level) -> int:
    """
    Returns te amount of xp needed to go from `level - 1` to `level`
    """
    return 5 * (level ** 2) + (50 * level) + 100


async def get_level_from_xp(xp) -> int:
    """
    Gives level from XP value

    Parameters:
    xp (int): XP to get level from
    """
    remaining_xp = int(xp)
    level = 0
    while remaining_xp >= await get_level_xp(level):
        remaining_xp -= await get_level_xp(level)
        level += 1
    return level


def random_chars(n):
    return "".join(
        random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(n)
    )


def gen_captcha():
    c = Claptcha(random_chars(5), "./data/DroidSansMono.ttf")

    text, im = c.image

    byte_array = io.BytesIO()
    im.save(byte_array, format="png")

    return text, byte_array


async def draw_history(user, history):
    font = ImageFont.truetype(f"./data/Nimbus-Sans-Light.ttf", 24)
    punishment_count = len(history)

    msg = f"{user}'s Punishment History"
    text_width, text_height = font.getsize(msg)
    top_grid = text_height + 20

    grid = draw_grid(punishment_count, top_grid)
    width, _ = grid.size
    draw = ImageDraw.Draw(grid)
    draw.text(((width - text_width) / 2, 10), msg, font=font, fill="black")

    text = [["Moderator", "Type", "Reason", "Date"]]
    for punishment in history:
        date_formatted = datetime.strftime(
            datetime.fromtimestamp(punishment[5]), "%d/%m %H:%M"
        )
        moderator = await get_moderator(punishment[2])
        if moderator is None:
            moderator = str(punishment[2])
        else:
            moderator = moderator[0]
        text.append([moderator, punishment[3], punishment[4], date_formatted])
    grid_written = write_grid(grid, text)

    grid_written.show()
    return grid


def draw_grid(punishment_count, top_grid):
    rows = punishment_count + 1
    height = (50 * (rows if rows <= 11 else 11)) + int(top_grid * 1.5)
    width = 1028
    image = Image.new(mode="L", size=(width, height), color=255)
    draw = ImageDraw.Draw(image)

    for x in range(1, width, 256):
        line = ((x, top_grid), (x, height - int(top_grid / 2)))
        draw.line(line, width=4, fill=128)
    for y in range(top_grid, height, 50):
        line = ((0, y), (width, y))
        draw.line(line, width=5, fill=128)

    return image


def write_grid(grid, text):
    draw = ImageDraw.Draw(grid)
    font = ImageFont.truetype(f"./data/Nimbus-Sans-Light.ttf", 24)
    box_width, box_height = 251, 44
    first_box_x, first_box_y = 4, 89
    displace_x, displace_y = 0, 0

    for row in text:
        for column in row:
            text_width, text_height = font.getsize(column)
            draw.text(
                (
                    (first_box_x + box_width - text_width) / 2 + displace_x,
                    (first_box_y + box_height - text_height) / 2 + displace_y,
                ),
                column,
                font=font,
                fill="black",
            )
            displace_x += 255
        displace_x = 0
        displace_y += 49
    return grid
