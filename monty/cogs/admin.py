import os

import discord
from discord.ext import commands

from monty.bot import MontyBot
from monty.util.context import BotContext
from monty.util.permissions import author_is_owner
from monty.util.traceback import traceback_maker


class Admin(commands.Cog):
    def __init__(self, bot: MontyBot):
        self.bot: MontyBot = bot

    @commands.command()
    @commands.check(author_is_owner)
    async def load(self, ctx: BotContext, name: str) -> None:
        """Loads a cog."""
        try:
            self.bot.load_extension(f"monty.cogs.{name}")
        except Exception as e:
            return await ctx.send(traceback_maker(e))
        await ctx.send(f"Loaded extension **{name}.py**!")

    @commands.command()
    @commands.check(author_is_owner)
    async def unload(self, ctx: BotContext, name: str) -> None:
        """Unloads a cog."""
        try:
            self.bot.unload_extension(f"monty.cogs.{name}")
        except Exception as e:
            return await ctx.send(traceback_maker(e))
        await ctx.send(f"Unoaded extension **{name}.py**!")

    @commands.command()
    @commands.check(author_is_owner)
    async def reload(self, ctx: BotContext, name: str) -> None:
        """Loads a cog."""
        try:
            self.bot.reload_extension(f"monty.cogs.{name}")
        except Exception as e:
            return await ctx.send(traceback_maker(e))
        await ctx.send(f"Reloaded extension **{name}.py**!")

    @commands.command()
    @commands.check(author_is_owner)
    async def reloadall(self, ctx):
        """Reloads all extensions."""
        error_collection = []
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.bot.reload_extension(f"monty.cogs.{name}")
                except Exception as e:
                    error_collection.append([file, traceback_maker(e, advance=False)])

        if error_collection:
            output = "\n".join(
                [f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection]
            )
            return await ctx.send(
                f"Attempted to reload all extensions, was able to reload, "
                f"however the following failed...\n\n{output}"
            )

        await ctx.send("Successfully reloaded all extensions!")


def setup(bot: MontyBot) -> None:
    bot.add_cog(Admin(bot))
