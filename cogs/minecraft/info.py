from discord.ext import commands
import discord

from utils.responses import generate_error
import aiohttp
import pycountry

from datetime import datetime

VALID_COUNTRIES_FOR_FLAGS = flags = [
    "af",
    "ax",
    "al",
    "dz",
    "as",
    "ad",
    "ao",
    "ai",
    "aq",
    "ag",
    "ar",
    "am",
    "aw",
    "au",
    "at",
    "az",
    "bs",
    "bh",
    "bd",
    "bb",
    "by",
    "be",
    "bz",
    "bj",
    "bm",
    "bt",
    "bo",
    "ba",
    "bw",
    "br",
    "io",
    "vg",
    "bn",
    "bg",
    "bf",
    "bi",
    "kh",
    "cm",
    "ca",
    "ic",
    "cv",
    "bq",
    "ky",
    "cf",
    "td",
    "cl",
    "cn",
    "cx",
    "cc",
    "co",
    "km",
    "cg",
    "cd",
    "ck",
    "cr",
    "ci",
    "cx",
    "cc",
    "co",
    "km",
    "cg",
    "cd",
    "ck",
    "cr",
    "ci",
    "hr",
    "cu",
    "cw",
    "cy",
    "cz",
    "dk",
    "dj",
    "dm",
    "do",
    "ec",
    "eg",
    "sv",
    "gq",
    "er",
    "ee",
    "et",
    "eu",
    "fk",
    "fo",
    "fj",
    "fi",
    "fr",
    "gf",
    "pf",
    "tf",
    "ga",
    "gm",
    "ge",
    "de",
    "gh",
    "gi",
    "gr",
    "gl",
    "gd",
    "gp",
    "gu",
    "gt",
    "gg",
    "gn",
    "gw",
    "gy",
    "ht",
    "hn",
    "hk",
    "hu",
    "is",
    "in",
    "id",
    "ir",
    "iq",
    "ie",
    "im",
    "il",
    "it",
    "jm",
    "jp",
    "je",
    "jo",
    "kz",
    "ke",
    "ki",
    "xk",
    "kw",
    "kg",
    "la",
    "lv",
    "lb",
    "ls",
    "lr",
    "ly",
    "li",
    "kw",
    "kg",
    "la",
    "lv",
    "lb",
    "ls",
    "lr",
    "ly",
    "li",
    "lt",
    "lu",
    "mo",
    "mk",
    "mg",
    "mw",
    "my",
    "mv",
    "ml",
    "mt",
    "mh",
    "mq",
    "mr",
    "mu",
    "yt",
    "mx",
    "fm",
    "md",
    "mc",
    "mn",
    "me",
    "ms",
    "ma",
    "mz",
    "mm",
    "na",
    "nr",
    "np",
    "nl",
    "nc",
    "nz",
    "ni",
    "ne",
    "ng",
    "nu",
    "nf",
    "kp",
    "mp",
    "no",
    "om",
    "pk",
    "pw",
    "ps",
    "pa",
    "pg",
    "py",
    "pe",
    "ph",
    "pn",
    "pl",
    "pt",
    "pr",
    "qa",
    "re",
    "ro",
    "ru",
    "rw",
    "ws",
    "sm",
    "st",
    "sa",
    "sn",
    "rs",
    "sc",
    "sl",
    "sg",
    "sx",
    "sk",
    "si",
    "gs",
    "sb",
    "so",
    "sc",
    "sl",
    "sg",
    "sx",
    "sk",
    "si",
    "gs",
    "sb",
    "so",
    "za",
    "kr",
    "ss",
    "es",
    "lk",
    "bl",
    "sh",
    "kn",
    "lc",
    "pm",
    "vc",
    "sd",
    "sr",
    "sz",
    "se",
    "ch",
    "sy",
    "tw",
    "tj",
    "tz",
    "th",
    "tl",
    "tg",
    "tk",
    "to",
    "tt",
    "tn",
    "tr",
    "tm",
    "tc",
    "vi",
    "tv",
    "ug",
    "ua",
    "ae",
    "gb",
    "england",
    "scotland",
    "wales",
    "us",
    "uy",
    "uz",
    "vu",
    "va",
    "ve",
    "vn",
    "wf",
    "eh",
    "ye",
    "zm",
    "zw",
    "ac",
    "bv",
    "cp",
    "ea",
    "dg",
    "hm",
    "mf",
    "sj",
    "ta",
    "um",
]


async def get_user_info(user: str) -> dict:
    async with aiohttp.ClientSession() as s:
        async with s.get(f"https://api.kqzz.me/api/mojang/user/{user}?namemc=true") as r:
            if r.status > 300:
                print(r.status)
                return None

            rj = await r.json()
            return rj


async def get_body_url(uuid: str):
    return f"https://www.mc-heads.net/body/{uuid}/right"


async def get_desc(user_data: dict) -> str:
    pass


async def get_pretty_socials(socials_list: dict) -> str:
    social_emojis = {
        "discord": "<:discord:822910137857212497>",
        "facebook": "<:youtube:822910143788089394>",
        "github": "<:github:822910137618137180>",
        "instagram": "<:instagram:822910138473119846>",
        "reddit": "<:reddit:822910164357087302>",
        "snapchat": "<:snapchat:822910145532395580>",
        "soundcloud": "<:soundcloud:822910162276450365>",
        "steam": "<:steam:822910144555122700>",
        "telegram": "<:telegram:822910144458915871>",
        "twitch": "<:twitch:822910143640502293>",
        "twitter": "<:twitter:822910145100120118>",
        "youtube": "<:youtube:822910143788089394>",
    }
    pretty_socials = ""
    for social in socials_list.keys():
        if social != 'discord':
            pretty_socials += f"[{social_emojis.get(social)}]({socials_list[social]}) "
        else:
            pretty_socials += f"{social_emojis.get(social)} "

    return pretty_socials


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx, user: str = None):
        if user is None:
            return await generate_error(ctx, "Please input a valid name")

        user_info = await get_user_info(user)

        if user_info is None:
            return await generate_error(ctx, "Failed to grab data on user!")

        embed = discord.Embed()

        embed.set_author(
            name=f"{user_info['username']} Info",
            icon_url=f"https://crafatar.com/avatars/{user_info['uuid']}",
            url=user_info["namemc"]["link"]
        )

        mc_profile = f"""__UUID__: `{user_info['uuid']}`
__Link__: {user_info['namemc']['link']}
__Views__: {user_info['namemc']['views']} / month"""

        embed.add_field(
            name="Minecraft Profile",
            value=mc_profile,
            inline=False
        )

        name_hist = ""
        for name in reversed(user_info["username_history"]):
            if name.get('changedToAt', None) is not None:
                name_hist += f"{name['name']} @ {datetime.utcfromtimestamp(name['changedToAt'] / 1000)}\n"
            else:
                name_hist += f"{name['name']} (original name)\n"

        embed.add_field(
            name="Name History",
            value="```" + name_hist + "```",
        )

        pretty_socials = await get_pretty_socials(user_info["namemc"]["accounts"])

        location = ""
        if user_info["namemc"]["location"] != "" and user_info["namemc"]["location"] is not None and "Badlion" not in user_info["namemc"]["location"]:
            # overengineered code 😐
            country_code = pycountry.countries.get(name=user_info["namemc"]["location"]).alpha_2.lower()
            if country_code in VALID_COUNTRIES_FOR_FLAGS:
                country_flag = f":flag_{country_code}:"
                if user_info["namemc"]["location"] in ("england", "scotland", "wales"):
                    country_flag = country_code
                location = f"__Location__: {country_flag} {user_info['namemc']['location']}\n"
            else:
                location = f"__Location__: {user_info['namemc']['location']}\n"

        if pretty_socials != "" or location != "":
            embed.add_field(
                name="Information",
                value=f"{location}__Accounts__: {pretty_socials}",
                inline=False
            )

        body_url = await get_body_url(user_info["uuid"])

        embed.set_thumbnail(url=body_url)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Info(client))
