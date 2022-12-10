import discord
from discord.ext import commands, pages
from docstring_parser import parse

from monty.util.embed import CustomEmbed


class MontyHelpCommand(commands.HelpCommand):
    def format_slash_options(self, options: list[discord.Option]):
        ret = ""
        if options.count == 0:
            return ret

        for o in options:
            if o.required == False:
                ret += f"[{o.name}] "
            else:
                ret += f"<{o.name}> "
        return ret.strip()

    def get_command_signature(self, command):
        if isinstance(command, discord.SlashCommand):
            return (
                "/",
                command.qualified_name,
                self.format_slash_options(command.options),
                command.description
                if command.description != None
                else "No Description",
            )
        return (
            self.context.clean_prefix,
            command.qualified_name,
            command.signature,
            command.help if command.help != None else "No Description",
        )

    async def send_bot_help(self, mapping):
        help_pages = []
        for cog, commands in mapping.items():
            embed = discord.Embed()
            if command_signatures := [self.get_command_signature(c) for c in commands]:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.title = f"Help | {cog_name}"
                for c in command_signatures:
                    embed.add_field(
                        name=f"{c[0]}{c[1]} {c[2]}", value=c[3], inline=True
                    )
                page = pages.Page(embeds=[embed])
                help_pages.append(page)

        paginator = pages.Paginator(pages=help_pages)
        await paginator.send(ctx=self.context, target=self.get_destination())

    async def send_command_help(self, command):

        embed = discord.Embed(title=command.name)
        if command.help:
            parsed = parse(command.help)

            formatted_help = f"""
            {parsed.short_description}
            """

            if parsed.long_description:
                formatted_help += parsed.long_description

            for arg in parsed.params:
                type_name = arg.type_name.replace(":class:`", "").replace("`", "")
                formatted_help += (
                    f"**{arg.arg_name}** (`{type_name}`) - {arg.description}"
                )

            if alias := command.aliases:
                embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

            embed.description = formatted_help.strip()

        channel = self.get_destination()
        await channel.send(embed=embed)
