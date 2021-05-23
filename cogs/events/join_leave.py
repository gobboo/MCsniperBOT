from discord.ext import commands
from discord.utils import get

import discord

from datetime import datetime as dt
import datetime
import io

from utils import captcha
from database.postgres_handler import execute_sql, query_sql


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if dt.utcnow() - member.created_at < datetime.timedelta(days=3):
            await member.add_roles(get(member.guild.roles, name="member"))
        else:
            # The account was brand new (under 3 days old)
            if member.dm_channel is None:
                await member.create_dm()
            try:
                text, captcha_bytes = captcha.gen_captcha()
                embed = discord.Embed(
                    description=f"Hello {member.mention}, your Discord account is less than 3 days old."
                    " Due to this, we require you to solve the below captcha in order to gain access to the rest of the server.\n\n"
                    "Please respond with the exact text shown in the captcha below.",
                    color=int("d8737f", 16)
                )

                embed.set_image(url="attachment://captcha.png")
                await member.dm_channel.send(
                    content=member.mention,
                    embed=embed,
                    file=discord.File(io.BytesIO(captcha_bytes.getvalue()), filename="captcha.png")
                )
                execute_sql(
                    f"""INSERT INTO captcha_users (
                        user_id,
                        captcha,
                        attempts
                    ) VALUES ('{member.id}', '{text}', 1);"""
                )
                print(query_sql("SELECT * FROM captcha_users"))

                # def check(m):
                #     return m.channel == member.dm_channel and m.author == member
                # response = await self.client.wait_for("message", check=check)
                # print(response.content, text)
                # if response.content.lower().strip() == text:
                #     await member.dm_channel.send("successfully answered captcha!")
                #     await member.add_roles(get(member.guild.roles, name="member"))
                # else:
                #     print("failed captcha rippp")
                #     await member.dm_channel.send("failed captcha")
            except Exception as e:
                print(e)
                # handle them not having dms enabled


def setup(client):
    client.add_cog(Welcome(client))
