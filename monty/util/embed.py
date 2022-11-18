import discord
from discord import Embed
from discord.ext import commands

from monty.util.context import BotContext


class CustomEmbed(Embed):
    def __init__(self, ctx: BotContext, *args, **kwargs):
        __slots__ = (
            "title",
            "url",
            "type",
            "_timestamp",
            "_colour",
            "_footer",
            "_image",
            "_thumbnail",
            "_video",
            "_provider",
            "_author",
            "_fields",
            "description",
        )

        embedColour = None
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour  # type: ignore

        self._fields = []
        self.type: discord.EmbedType = "rich"  # type: ignore

        super().__init__(colour=self.colour, *args, **kwargs)
