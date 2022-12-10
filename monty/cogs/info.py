import json as jason
import os
import time
from typing import Optional

import discord
import httpx
import psutil
from discord.ext import commands
from loguru import logger

from monty import __version__
from monty.bot import MontyBot
from monty.util.context import BotContext
from monty.util.date import date
from monty.util.embed import CustomEmbed
from monty.util.traceback import log_traceback_maker, traceback_maker


class Info(commands.Cog):
    def __init__(self, bot: MontyBot) -> None:
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self, ctx: BotContext):
        """Pong!"""
        before = time.monotonic()
        message = await ctx.send("Pong...")

        ping = (time.monotonic() - before) * 1000

        await message.edit(content=f"Pong! `{int(ping)}ms`")

    @commands.command()
    async def info(self, ctx: BotContext):
        """Info about the bot."""
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)

        embed = CustomEmbed(ctx)  # type: ignore
        embed.set_thumbnail(url=ctx.bot.user.avatar)  # type: ignore
        embed.add_field(name="Last boot", value=date(self.bot.uptime, ago=True))
        embed.add_field(name="Version", value=__version__)
        embed.add_field(
            name=f"Developer{'' if len(self.bot.config['bot']['owners']) == 1 else 's'}",
            value=", ".join(
                [str(self.bot.get_user(x)) for x in self.bot.config["bot"]["owners"]]
            ),
        )
        embed.add_field(name="Library", value=f"pycord {discord.__version__}")
        embed.add_field(
            name="Servers",
            value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers:,.2f} users/server )",
        )
        embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]))  # type: ignore
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB")

        await ctx.send(content=f"ℹ About **{ctx.bot.user}**", embed=embed)

    @commands.command(aliases=["curr"])
    async def currency(self, ctx, amount: float | int | None, source: str, target: str):
        """Converts currency from a given currency to another.

        Parameters
        ---------
        amount: float or int, optional
            An optional amount of the `source` currency to convert.
        source: str
            The three letter code that represents a single currency to convert **from**.
            Examples include `AED`, `USD`, `EUR`.
        target: str
            The three letter code that represents a single currency to convert **to**.
            Examples include `GBP`, `NZD`, `CAD`.
        """
        async with httpx.AsyncClient() as client:
            try:
                url = f"https://api.exchangerate.host/convert?from={source}&to={target}"
                if amount != None:
                    url += f"&amount={amount}"

                resp = await client.get(url)
                json = jason.loads(resp.text)

                amount = json["result"]

                from_code = json["query"]["from"]
                to_code = json["query"]["to"]

                rate = json["info"]["rate"]

                date = json["date"]

                symbols_resp = await client.get("https://api.exchangerate.host/symbols")
                symbols = jason.loads(symbols_resp.text)

                embed = CustomEmbed(ctx)
                embed.title = "💱 Currency Rates"
                embed.add_field(
                    name="Amount",
                    value=f"**{round(amount, 2)}** {symbols['symbols'][to_code]['description']}",  # type: ignore
                )
                embed.add_field(
                    name="Rate", value=f"1 {from_code} == {round(rate, 2)} {to_code}"
                )
                embed.set_footer(text=f"Exchange rates correct as of {date}.")

                await ctx.send(embed=embed)
            except Exception as e:
                logger.error(f"Currency request failed. \n {log_traceback_maker(e)}")
                await ctx.send(traceback_maker(e))


def setup(bot: MontyBot):
    bot.add_cog(Info(bot))
