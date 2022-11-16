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

        if not hasattr(ctx, "guild"):
            self.colour = discord.Colour(0x7289DA)
        else:
            self.colour = ctx.me.colour
        self._fields = []
        self.type: discord.EmbedType = "rich"

        super().__init__(colour=self.colour, *args, **kwargs)
