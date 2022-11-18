from datetime import datetime

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

    @commands.command()
    async def timesetup(self, ctx: BotContext, tz: str):
        """Set up the timezone for a user."""
        if tz not in pytz.all_timezones:
            await ctx.send("**Error**: Not a valid timezone.")
        else:
            zone = pytz.timezone(tz)
            now = datetime.now()
            local_now = now.astimezone(zone)
            fmt = "%Y-%m-%d %H:%M:%S %z"

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


def setup(bot: MontyBot):
    bot.add_cog(TimeCog(bot))
