from typing import Union

import discord
from discord.ext import commands

from .config import Config


def bot_has_permission(ctx: commands.Context | discord.Message, permission: str):
    """Checks if a bot has a given permission."""
    return isinstance(ctx.channel, discord.DMChannel) or getattr(
        ctx.channel.permissions_for(ctx.guild.me), permission
    )


def author_is_owner(ctx: commands.Context):
    return ctx.author.id in ctx.bot.owners
