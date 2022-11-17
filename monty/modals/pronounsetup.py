import discord


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
        subject = self.children[0].value
        objectPro = self.children[1].value
        posDet = self.children[2].value
        posPro = self.children[3].value
        reflexive = self.children[4].value

        embed = discord.Embed()
        embed.description = "Pronoun Confirmation"
        embed.add_field(
            name="Example",
            value=f"""
            **{subject.capitalize()}** (subject) went to the park.
            I went with **{objectPro}** (object).
            **{subject.capitalize()}**  brought **{posDet}** (pos. determiner) frisbee.
            At least, I think it was **{posPro}** (possessive).
            **{subject.capitalize()}** (subject) threw the frisbee to **{reflexive}** (reflexive).
        """,
        )

        await interaction.response.send_message(embed=embed, view=PronounConfirmation())


class PronounConfirmation(discord.ui.View):
    @discord.ui.button(label="Confirm", row=0, style=discord.ButtonStyle.success)
    async def confirm_callback(
        self, button: discord.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("Confirmed!")

    @discord.ui.button(label="Cancel", row=0, style=discord.ButtonStyle.danger)
    async def cancel_callback(
        self, button: discord.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("Cancelled!")
