import json
from datetime import datetime

import discord
import httpx
from discord.ext import commands
from loguru import logger

from monty.bot import MontyBot
from monty.util import math
from monty.util.context import BotContext
from monty.util.embed import CustomEmbed
from monty.util.traceback import log_traceback_maker


class Weather(commands.Cog):
    def __init__(self, bot: MontyBot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx: BotContext, *location):
        """Provides weather data, sourced from OpenWeatherMap.

        Parameters
        ----------
        *args : :class:`tuple`
            Additional arguments for the location that take up the rest of the command.
            Must match the format of ``<city> [state] [two-letter-country-code]``, without commas.
            Examples include ``Sydney``, ``Melbourne AU``, ``Croydon VIC AU``.
        """
        key = self.bot.config["bot"]["api"]["openWeatherMap"]

        if len(location) == 0:
            await ctx.send("No location provided.")
        else:
            async with httpx.AsyncClient() as client:
                try:
                    r = await client.get(
                        f"https://api.openweathermap.org/data/2.5/weather?q={','.join(location)}&appid={key}"
                    )

                    result = r.text

                    json_result = json.loads(result)

                    celsius = math.kelvin_to_celsius(json_result["main"]["temp"])
                    fahrenheit = math.kelvin_to_fahrenheit(json_result["main"]["temp"])

                    celsiusMin = math.kelvin_to_celsius(json_result["main"]["temp_min"])
                    fahrenheitMin = math.kelvin_to_fahrenheit(
                        json_result["main"]["temp_min"]
                    )

                    celsiusMax = math.kelvin_to_celsius(json_result["main"]["temp_max"])
                    fahrenheitMax = math.kelvin_to_celsius(
                        json_result["main"]["temp_max"]
                    )

                    celsiusFl = math.kelvin_to_celsius(
                        json_result["main"]["feels_like"]
                    )
                    fahrenheitFl = math.kelvin_to_celsius(
                        json_result["main"]["feels_like"]
                    )

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
                    embed.add_field(
                        name="Feels Like", value=f"{celsiusFl}°C/{fahrenheitFl}°F"
                    )

                    embed.set_thumbnail(
                        url=f"https://openweathermap.com/img/wn/{json_result['weather'][0]['icon']}@2x.png"
                    )

                    await ctx.send(embed=embed)
                except Exception as e:
                    logger.error(
                        f"Error calling OpenWeatherMap. {log_traceback_maker(e)}"
                    )
                    await ctx.send("Error calling OpenWeatherMap.")


def setup(bot: MontyBot) -> None:
    bot.add_cog(Weather(bot))
