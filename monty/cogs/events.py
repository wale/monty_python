from datetime import datetime

import discord
from discord.ext import commands
from discord.ext.commands import errors
from loguru import logger

from monty.bot import MontyBot
from monty.util import permissions
from monty.util.context import BotContext
from monty.util.traceback import traceback_maker


class Events(commands.Cog):
    def __init__(self, bot: MontyBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """The function that runs when the bot has started."""

        self.bot.uptime = datetime.now()

        # Check if user desires to have something other than online
        status = self.bot.config["bot"]["status"]["type"].lower()
        status_type = {
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "online": discord.Status.online,
        }

        # Check if user desires to have a different type of activity
        activity = self.bot.config["bot"]["activity"]["type"].lower()
        activity_type = {"listening": 2, "watching": 3, "competing": 5}

        await self.bot.change_presence(
            activity=discord.Activity(
                type=activity_type.get(activity, 0),
                name=self.bot.config["bot"]["status"]["text"],
            ),
            status=status_type.get(status, discord.Status.online),
        )

        logger.info(f"Ready as {self.bot.user}! | Servers: {len(self.bot.guilds)}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(
            err, errors.BadArgument
        ):
            helper = (
                str(ctx.invoked_subcommand)
                if ctx.invoked_subcommand
                else str(ctx.command)
            )
            await ctx.send_help(helper)

        elif isinstance(err, errors.CommandInvokeError):
            error = traceback_maker(err.original)

            if "2000 or fewer" in str(err) and len(ctx.message.clean_content) > 1900:
                return await ctx.send(
                    "You attempted to make the command display more than 2,000 characters...\n"
                    "Both error and command will be ignored."
                )

            await ctx.send(
                f"There was an error processing the command \n```\n{error}\n```"
            )

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.MaxConcurrencyReached):
            await ctx.send(
                "You've reached max capacity of command usage at once, please finish the previous one..."
            )

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(
                f"This command is on cooldown... try again in {err.retry_after:.2f} seconds."
            )

        elif isinstance(err, errors.CommandNotFound):
            pass

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if (
            not self.bot.is_ready()
            or message.author.bot
            or permissions.bot_has_permission(message, "send_messages")
        ):
            return

        await self.process_commands(message)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if not self.bot.is_ready() or not interaction.permissions.send_messages:
            return

        await self.process_application_commands(interaction)

    @commands.Cog.listener()
    async def on_command(self, ctx: BotContext):
        try:
            logger.debug(
                f"{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}"
            )
        except AttributeError:
            logger.debug(
                f"Private message > {ctx.author} > {ctx.message.clean_content}"
            )


def setup(bot: MontyBot) -> None:
    bot.add_cog(Events(bot))
