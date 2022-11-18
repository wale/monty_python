import discord
from discord.ext import bridge, commands
from loguru import logger
from sqlmodel import Session, select

from monty.bot import MontyBot
from monty.db_models import Pronoun, User
from monty.modals.pronounsetup import PronounChoice
from monty.util.db import engine
from monty.util.traceback import log_traceback_maker


class PronounCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @bridge.bridge_command()
    async def pronounsetup(self, ctx: bridge.BridgeExtContext) -> None:
        """Setup function for user-provided pronouns."""
        user_id = ctx.author.id
        with Session(engine) as session:
            statement = select(User, Pronoun).where(User.id == user_id).join(Pronoun)
            results = session.exec(statement)

            try:
                user = results.one()
                if user == None:
                    await ctx.respond(
                        "You can start the setup by clicking the below button.",
                        view=EntryView(),
                    )
                else:
                    pronouns = user[0].pronouns
                    content_format = "Your pronouns are: **"
                    content_format += f"{pronouns.subj}/{pronouns.obj}/{pronouns.posDet}/{pronouns.posPro}/{pronouns.refl}"
                    content_format += "** \n"
                    content_format += (
                        "You can start the setup anyway by clicking the below button."
                    )
                    await ctx.respond(content_format, view=EntryView())
            except Exception as e:
                logger.error(
                    f"Logger when accessing database. {log_traceback_maker(e)}"
                )


class EntryView(discord.ui.View):
    @discord.ui.button(label="Start setup", style=discord.ButtonStyle.primary)
    async def button_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.edit_message(
            content="Select your pronouns, or you can use a custom one.",
            view=PronounChoice(timeout=60),
        )


def setup(bot: MontyBot):
    bot.add_cog(PronounCog(bot))
