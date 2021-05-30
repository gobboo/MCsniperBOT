import io
import random

from claptcha import Claptcha


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
    while (remaining_xp >= await get_level_xp(level)):
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
