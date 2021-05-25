import datetime
import io
from datetime import datetime as dt

import discord
from discord import Forbidden
from discord.ext import commands
from discord.utils import get

from config import MEMBER_ROLE
from database.users import set_captcha
from utils.functions import gen_captcha

# from database.postgres_handler import query_sql


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if dt.utcnow() - member.created_at < datetime.timedelta(days=3):
            await member.add_roles(get(member.guild.roles, name=MEMBER_ROLE))
        else:
            # The account was brand new (under 3 days old)
            try:
                captcha, captcha_bytes = gen_captcha()
                embed = discord.Embed(
                    description=f"Hello {member.mention}, your Discord account is less than 3 days old. "
                    f"Due to this, we require you to solve the below captcha in order to gain access to "
                    f"the rest of the server.\n\n"
                    f"Please respond with the exact text shown in the captcha below.",
                    color=int("d8737f", 16),
                )

                embed.set_image(url="attachment://captcha.png")
                await member.send(
                    content=member.mention,
                    embed=embed,
                    file=discord.File(
                        io.BytesIO(captcha_bytes.getvalue()), filename="captcha.png"
                    ),
                )
                await set_captcha(member.id, captcha)
            except Forbidden:
                # TODO: Figure out how we want to approach this as it is 100% necessary
                print(
                    "Here we will tag them in the one channel they can see, telling them to enable server DMs then "
                    "running !verify"
                )

            # TODO: Figure if this will ever occur, and get rid of it
            except Exception as e:
                print(e)


def setup(client):
    client.add_cog(Welcome(client))
