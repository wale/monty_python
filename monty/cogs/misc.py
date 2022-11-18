import discord
from discord.ext import commands

from monty.bot import MontyBot
from monty.util.context import BotContext


class Misc(commands.Cog):
    def __init__(self, bot: MontyBot) -> None:
        self.bot = bot

    @commands.command()
    async def hug(self, ctx: BotContext, user: discord.User) -> None:
        """Hugs a given user."""
        await ctx.send(f"<@{ctx.author.id}> hugged <@{user.id}>.")


def setup(bot: MontyBot) -> None:
    bot.add_cog(Misc(bot))
