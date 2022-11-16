import time

import discord
from discord.ext import commands

from monty.bot import MontyBot
from monty.util.context import BotContext


class Info(commands.Cog):
    def __init__(self, bot: MontyBot) -> None:
        self.bot: MontyBot = bot

    @commands.command()
    async def ping(self, ctx: BotContext):
        before = time.monotonic()
        message = await ctx.send("Pong...")

        ping = (time.monotonic() - before) * 1000

        await message.edit(content=f"Pong! `{int(ping)}ms`")


def setup(bot: MontyBot):
    bot.add_cog(Info(bot))
