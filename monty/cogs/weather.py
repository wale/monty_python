import json
from datetime import datetime

import discord
import httpx
from discord.ext import commands

from monty.bot import MontyBot
from monty.util import math
from monty.util.context import BotContext
from monty.util.embed import CustomEmbed


class Weather(commands.Cog):
    def __init__(self, bot: MontyBot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx: BotContext, *location):
        key = self.bot.config["bot"]["api"]["openWeatherMap"]

        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={','.join(location)}&appid={key}"
            )

            result = r.text

            json_result = json.loads(result)

            celsius = math.kelvin_to_celsius(json_result["main"]["temp"])
            fahrenheit = math.kelvin_to_fahrenheit(json_result["main"]["temp"])

            celsiusMin = math.kelvin_to_celsius(json_result["main"]["temp_min"])
            fahrenheitMin = math.kelvin_to_fahrenheit(json_result["main"]["temp_min"])

            celsiusMax = math.kelvin_to_celsius(json_result["main"]["temp_max"])
            fahrenheitMax = math.kelvin_to_celsius(json_result["main"]["temp_max"])

            celsiusFl = math.kelvin_to_celsius(json_result["main"]["feels_like"])
            fahrenheitFl = math.kelvin_to_celsius(json_result["main"]["feels_like"])

            embed = CustomEmbed(ctx=ctx)
            embed.title = f":flag_{json_result['sys']['country'].lower()}: Weather for {json_result['name']}."
            embed.description = (
                f"{json_result['weather'][0]['description'].capitalize()}"
            )
            embed.add_field(
                name="Current Temperature", value=f"{celsius}°C/{fahrenheit}°F"
            )
            embed.add_field(
                name="Min. Temp.", value=f"{celsiusMin}°C/{fahrenheitMin}°F"
            )
            embed.add_field(
                name="Max. Temp.", value=f"{celsiusMax}°C/{fahrenheitMax}°F"
            )
            embed.add_field(name="Feels Like", value=f"{celsiusFl}°C/{fahrenheitFl}°F")

            embed.set_thumbnail(
                url=f"https://openweathermap.com/img/wn/{json_result['weather'][0]['icon']}@2x.png"
            )

            await ctx.send(embed=embed)


def setup(bot: MontyBot) -> None:
    bot.add_cog(Weather(bot))
