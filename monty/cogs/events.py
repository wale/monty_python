from datetime import datetime

import discord
from discord.ext import commands
from loguru import logger

from monty.bot import MontyBot
from monty.util import permissions


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


def setup(bot: MontyBot) -> None:
    bot.add_cog(Events(bot))
