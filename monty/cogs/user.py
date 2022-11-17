import discord
from discord.ext import bridge, commands

from monty.bot import MontyBot
from monty.modals.pronounsetup import PronounChoice
from monty.util.context import BotContext


class EntryView(discord.ui.View):
    @discord.ui.button(label="Start setup", style=discord.ButtonStyle.primary)
    async def button_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.edit_message(
            content="Select your pronouns, or you can use a custom one.",
            view=PronounChoice(),
        )


class User(commands.Cog):
    def __init__(self, bot: MontyBot) -> None:
        self.bot: MontyBot = bot

    @bridge.bridge_command()
    async def pronounsetup(self, ctx: bridge.BridgeExtContext) -> None:
        """Setup function for user-provided pronouns."""
        await ctx.respond(
            "You can start the setup by clicking the below button.", view=EntryView()
        )


def setup(bot: MontyBot):
    bot.add_cog(User(bot))
