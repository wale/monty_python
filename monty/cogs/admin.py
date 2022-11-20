import ast
import os
import sys
import time

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
    @commands.check(author_is_owner)  # type: ignore
    async def load(self, ctx: BotContext, name: str) -> None:
        """Loads a cog."""
        try:
            self.bot.load_extension(f"monty.cogs.{name}")
        except Exception as e:
            return await ctx.send(traceback_maker(e))  # type: ignore
        await ctx.send(f"Loaded extension **{name}.py**!")

    @commands.command()
    @commands.check(author_is_owner)  # type: ignore
    async def unload(self, ctx: BotContext, name: str) -> None:
        """Unloads a cog."""
        try:
            self.bot.unload_extension(f"monty.cogs.{name}")
        except Exception as e:
            return await ctx.send(traceback_maker(e))  # type: ignore
        await ctx.send(f"Unoaded extension **{name}.py**!")

    @commands.command()
    @commands.check(author_is_owner)  # type: ignore
    async def reload(self, ctx: BotContext, name: str) -> None:
        """Loads a cog."""
        try:
            self.bot.reload_extension(f"monty.cogs.{name}")
        except Exception as e:
            return await ctx.send(traceback_maker(e))  # type: ignore
        await ctx.send(f"Reloaded extension **{name}.py**!")

    @commands.command()
    @commands.check(author_is_owner)  # type: ignore
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

    def insert_returns(self, body):
        # insert return stmt if the last expression is a expression statement
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        # for if statements, we insert returns into the body and the orelse
        if isinstance(body[-1], ast.If):
            self.insert_returns(body[-1].body)
            self.insert_returns(body[-1].orelse)

        # for with blocks, again we insert returns into the body
        if isinstance(body[-1], ast.With):
            self.insert_returns(body[-1].body)

    @commands.command()
    @commands.check(author_is_owner)  # type: ignore
    async def eval(self, ctx: BotContext, cmd: str):
        """Evaluates input.
        Input is interpreted as newline seperated statements.
        If the last statement is an expression, that is the return value.
        Usable globals:
        - `bot`: the bot instance
        - `discord`: the discord module
        - `commands`: the discord.ext.commands module
        - `ctx`: the invokation context
        - `__import__`: the builtin `__import__` function
        Such that `>eval 1 + 1` gives `2` as the result.
        The following invokation will cause the bot to send the text '9'
        to the channel of invokation and return '3' as the result of evaluating
        >eval ```
        a = 1 + 2
        b = a * 2
        await ctx.send(a + b)
        a
        ```
        """
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")
        cmd = cmd.strip("```")
        cmd = cmd.strip("```py")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body  # type: ignore

        self.insert_returns(body)

        env = {
            "bot": ctx.bot,
            "discord": discord,
            "commands": commands,
            "ctx": ctx,
            "__import__": __import__,
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = await eval(f"{fn_name}()", env)
        await ctx.send(result)

    @commands.command()
    @commands.check(author_is_owner)  # type: ignore
    async def reboot(self, ctx):
        """Reboot the bot"""
        await ctx.send("Rebooting now...")
        time.sleep(1)
        sys.exit(0)


def setup(bot: MontyBot) -> None:
    bot.add_cog(Admin(bot))
