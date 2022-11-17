from discord.ext import commands

from ..bot import MontyBot


class BotContext(commands.Context):
    def __init__(self, bot, *args, **kwargs):
        self.bot: MontyBot = bot

        super().__init__(bot=bot, *args, **kwargs)
