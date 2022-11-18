import os
import time

import discord
import psutil
from discord.ext import commands

from monty.bot import MontyBot
from monty.util.context import BotContext
from monty.util.date import date
from monty.util.embed import CustomEmbed


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
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)

        embed = CustomEmbed(ctx)  # type: ignore
        embed.set_thumbnail(url=ctx.bot.user.avatar)  # type: ignore
        embed.add_field(name="Last boot", value=date(self.bot.uptime, ago=True))
        embed.add_field(
            name=f"Developer{'' if len(self.bot.config['bot']['owners']) == 1 else 's'}",
            value=", ".join(
                [str(self.bot.get_user(x)) for x in self.bot.config["bot"]["owners"]]
            ),
        )
        embed.add_field(name="Library", value="discord.py")
        embed.add_field(
            name="Servers",
            value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers:,.2f} users/server )",
        )
        embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]))  # type: ignore
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB")

        await ctx.send(content=f"ℹ About **{ctx.bot.user}**", embed=embed)


def setup(bot: MontyBot):
    bot.add_cog(Info(bot))
