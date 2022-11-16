import asyncio
import os

import discord

from monty.bot import MontyBot
from monty.util.config import Config


async def run() -> None:
    config_class = Config()
    config_class.load()

    config = config_class.get_config()

    bot = MontyBot(
        config=config,
        prefix=config["bot"]["prefixes"],
        owner_ids=config["bot"]["owners"],
        allowed_mentions=discord.AllowedMentions(
            roles=False, users=True, everyone=False
        ),
        intents=discord.Intents.all(),
    )

    try:
        await bot.start(config["bot"]["token"])
    except Exception as e:
        print(f"Error when logging in: {e}")


def main() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


if __name__ == "__main__":
    main()
