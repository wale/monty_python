def kelvin_to_celsius(temp: int) -> float:
    return round(temp - 273.15, 1)


def kelvin_to_fahrenheit(temp: int) -> float:
    return round((temp - 273.15) * 9 / 5 + 32, 1)
