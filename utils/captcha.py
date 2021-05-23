import random
from claptcha import Claptcha

import io


def random_chars(n):
    return "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(n))


def gen_captcha():
    c = Claptcha(random_chars(5), "./data/DroidSansMono.ttf")

    text, im = c.image

    byte_array = io.BytesIO()
    im.save(byte_array, format="png")

    return text, byte_array
