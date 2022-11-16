from typing import Union

import discord
from discord.ext import commands


def bot_has_permission(ctx: commands.Context | discord.Message, permission: str):
    """Checks if a bot has a given permission."""
    return isinstance(ctx.channel, discord.DMChannel) or getattr(
        ctx.channel.permissions_for(ctx.guild.me), permission
    )
