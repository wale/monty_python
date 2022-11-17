import os
from datetime import datetime

import discord
from discord.ext import bridge, commands
from loguru import logger

from monty.util.config import Config


class MontyBot(bridge.AutoShardedBot):
    def __init__(self, *args, prefix: str = None, config: dict = None, **kwargs):
        super().__init__(*args, command_prefix=prefix, **kwargs)
        self.prefix = prefix
        self.uptime: datetime = None
        self.config = config

    @commands.Cog.listener()
    async def on_connect(self) -> None:
        try:
            for file in os.listdir("monty/cogs"):
                if file.endswith(".py") and not file.startswith("__init__"):
                    name = file[:-3]
                    self.load_extension(f"monty.cogs.{name}")
        except Exception as e:
            logger.error(f"Could not setup hook: \n{e}")
