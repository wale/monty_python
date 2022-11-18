import discord
from loguru import logger
from sqlmodel import Session
from sqlmodel import select as sel

from monty.db_models import Pronoun, User
from monty.util.db import engine
from monty.util.traceback import log_traceback_maker


class PronounChoice(discord.ui.View):
    @discord.ui.select(
        placeholder="Select your pronoun choice.",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="he/him/his/his/himself"),
            discord.SelectOption(label="she/her/her/hers/herself"),
            discord.SelectOption(label="they/them/their/theirs/themselves"),
            discord.SelectOption(label="Custom Pronouns"),
            #discord.SelectOption(label="Clear Pronouns"),
        ],
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        if select.values[0] == "Custom Pronouns":
            await interaction.response.send_modal(
                PronounSetupModal(title="Custom Pronouns")
            )
        #elif select.values[0] == "Clear Pronouns":
            #user_id = interaction.user.id # type: ignore
            
            #with Session(engine) as session:
        
                #statement = sel(User, Pronoun).where(User.id == user_id).join(Pronoun)
                #results = session.exec(statement)
        
                #user = results.one()

                #if user == None:
                    #await interaction.response.send_message(
                    #    "No user field found, run `m:pronounsetup`."
                    #)
                    #return
                #else:
                    #try:
                        #user[0].pronouns = None

                        #session.add(user[0])
                        #session.add(user[1])
                        #session.commit()
                        #session.flush([user[0], user[1]])
                        #await interaction.response.send_message("Cleared pronouns!")
                    #except Exception as e:
                        #logger.error(
                        #    f"Removing `pronouns` row in DB failed. \n{log_traceback_maker(e)}"
                        #)
                        #await interaction.response.send_message(
                            #content="Removing `pronouns` row in DB failed. Pinged <@255114091360681986>."
                        #)
        else:
            pronoun_split = select.values[0].split("/")

            subject = pronoun_split[0]
            objectPro = pronoun_split[1]
            posDet = pronoun_split[2]
            posPro = pronoun_split[3]
            reflexive = pronoun_split[4]

            embed = discord.Embed()
            embed.description = "Pronoun Confirmation"
            embed.add_field(
                name="Example",
                value=f"""
                **{subject.capitalize()}** (*subject*) went to the park.
                I went with **{objectPro}** (object).
                **{subject.capitalize()}** (*subject*)  brought **{posDet}** (*pos. determiner*) frisbee.
                At least, I think it was **{posPro}** (*possessive*).
                **{subject.capitalize()}** (*subject*) threw the frisbee to **{reflexive}** (*reflexive*).
            """,
            )

            await interaction.response.edit_message(
                embed=embed, view=PronounConfirmation(pronouns=pronoun_split)
            )


class PronounSetupModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Subject",
                placeholder="The pronoun that performs the action in a sentence.",
                required=True,
            )
        )

        self.add_item(
            discord.ui.InputText(
                label="Object",
                placeholder="The pronoun that refers to someone as an object in the third person.",
                required=True,
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Possessive Determiner",
                placeholder='The pronoun that expresses that someone owns, or possesses something. "He owns that ball."',
                required=True,
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Possessive Pronoun",
                placeholder='The pronoun that expresses if someone owns something; "Is that her scarf?"',
                required=True,
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Reflexive",
                placeholder='The pronoun that refers to a pronoun in the same sentence. "They helped themselves."',
            )
        )

    async def callback(self, interaction: discord.Interaction):
        subject = str(self.children[0].value) # required to make type checking stfu
        objectPro = self.children[1].value
        posDet = self.children[2].value
        posPro = self.children[3].value
        reflexive = self.children[4].value

        pronoun_list = [subject, objectPro, posDet, posPro, reflexive]

        embed = discord.Embed()
        embed.description = "Pronoun Confirmation"
        embed.add_field(
            name="Example",
            value=f"""
            **{subject.capitalize()}** (*subject*) went to the park.
            I went with **{objectPro}** (*object*).
            **{subject.capitalize()}** (*subject*)  brought **{posDet}** (*pos. determiner*) frisbee.
            At least, I think it was **{posPro}** (*possessive*).
            **{subject.capitalize()}** (*subject*) threw the frisbee to **{reflexive}** (*reflexive*).
        """,
        )

        await interaction.response.edit_message(
            embed=embed, view=PronounConfirmation(pronouns=pronoun_list)
        )


class PronounConfirmation(discord.ui.View):
    def __init__(self, pronouns: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pronouns = pronouns

    @discord.ui.button(label="Confirm", row=0, style=discord.ButtonStyle.success)
    async def confirm_callback(
        self, button: discord.Button, interaction: discord.Interaction
    ):
        user_id = interaction.user.id # type: ignore
        with Session(engine) as session:
            statement = sel(User, Pronoun).where(User.id == user_id).join(Pronoun)
            results = session.exec(statement)

            try:
                user = results.one_or_none()
                if user == None:
                    try:
                        pronouns = Pronoun(
                            subj=str(self.pronouns[0]), # type: ignore
                            obj=str(self.pronouns[1]),
                            posDet=str(self.pronouns[2]),
                            posPro=str(self.pronouns[3]),
                            refl=str(self.pronouns[4]),
                        )
                        user = User(id=user_id, pronouns=pronouns)

                        session.add(user)
                        session.commit()
                    except Exception as e:
                        logger.error(
                            f"Creating user in DB failed. \n{log_traceback_maker(e)}"
                        )
                        await interaction.response.send_message(
                            content="Creating user in DB failed. Pinged <@255114091360681986>."
                        )
                else:
                    try:
                        user[1].subj = str(self.pronouns[0])
                        user[1].obj = str(self.pronouns[1])
                        user[1].posDet = str(self.pronouns[2])
                        user[1].posPro = str(self.pronouns[3])
                        user[1].refl = str(self.pronouns[4])

                        session.add(user[0])
                        session.add(user[1])
                        session.commit()

                        await interaction.response.send_message(
                            "Pronouns have been submitted to DB!"
                        )
                    except Exception as e:
                        logger.error(
                            f"Updating user in DB failed. \n{log_traceback_maker(e)}"
                        )
                        await interaction.response.send_message(
                            content="Updating user in DB failed. Pinged <@255114091360681986>."
                        )
            except Exception as e:
                logger.error(f"Updating user in DB failed. \n{log_traceback_maker(e)}")
                await interaction.response.send_message(
                    content="Updating user in DB failed. Pinged <@255114091360681986>."
                )

    @discord.ui.button(label="Cancel", row=0, style=discord.ButtonStyle.danger)
    async def cancel_callback(
        self, button: discord.Button, interaction: discord.Interaction
    ):
        await interaction.delete_original_message()
        await interaction.response.send_message("Cancelled!")
