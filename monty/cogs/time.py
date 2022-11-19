from datetime import datetime

import discord
import humanize
import pytz
from discord.ext import commands
from sqlmodel import Session, select

from monty.bot import MontyBot
from monty.db_models import *
from monty.util.context import BotContext
from monty.util.db import engine


class TimeCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot: MontyBot = bot

    @commands.command(aliases=["tzsetup"])
    async def timesetup(self, ctx: BotContext, tz: str):
        """Set up the timezone for a user."""
        if tz not in pytz.all_timezones:
            await ctx.send("**Error**: Not a valid timezone.")
        else:
            zone = pytz.timezone(tz)
            now = datetime.now()
            local_now = now.astimezone(zone)
            # fmt = "%Y-%m-%d %H:%M:%S %z"
            fmt = "%Y-%m-%d %I:%M %p"

            with Session(engine) as session:
                stmt = select(User).where(User.id == ctx.author.id)
                result = session.exec(stmt)

                user = result.one_or_none()

                if user == None:
                    new_user = User(id=ctx.author.id, timezone=tz)
                    session.add(new_user)
                    session.commit()
                    await ctx.send(
                        f"Added your timezone! Your current time is `{local_now.strftime(fmt)}`."
                    )
                else:
                    user.timezone = tz
                    session.add(user)
                    session.commit()
                    await ctx.send(
                        f"Added your timezone! Your current time is `{local_now.strftime(fmt)}`."
                    )

    @commands.command(aliases=["tf", "time"])
    async def timefor(self, ctx: BotContext, user: discord.User | None = None):
        """Gets the current time for a given user or the author."""
        if user == None:
            with Session(engine) as session:
                stmt = select(User).where(User.id == ctx.author.id)
                result = session.exec(stmt)

                db_user = result.one_or_none()
                if db_user == None:
                    await ctx.send("You do not have a timezone set.")
                else:
                    tz = db_user.timezone
                    fmt = "%Y-%m-%d %I:%M %p"
                    zone = pytz.timezone(tz)
                    local_now = datetime.now().astimezone(zone)
                    await ctx.send(f"Your current time is `{local_now.strftime(fmt)}`.")
        else:
            with Session(engine) as session:
                stmt = select(User).where(User.id == user.id)
                result = session.exec(stmt)

                db_user = result.one_or_none()
                if db_user == None or db_user.timezone == None:
                    await ctx.send("They do not have a timezone set.")
                elif db_user.pronouns == None:
                    tz = db_user.timezone
                    fmt = "%Y-%m-%d %I:%M %p"
                    zone = pytz.timezone(tz)
                    local_now = datetime.now().astimezone(zone)
                    await ctx.send(
                        f"Their current time is `{local_now.strftime(fmt)}`."
                    )
                else:
                    tz = db_user.timezone
                    fmt = "%Y-%m-%d %I:%M %p"
                    zone = pytz.timezone(tz)
                    local_now = datetime.now().astimezone(zone)
                    pro = db_user.pronouns.posDet
                    await ctx.send(
                        f"{str(pro).capitalize()} current time is `{local_now.strftime(fmt)}`."
                    )


def setup(bot: MontyBot):
    bot.add_cog(TimeCog(bot))
