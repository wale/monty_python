import tomli


class Config:
    def __init__(self):
        self.config: dict = {}

    def load(self, filename: str = "config.bot.toml") -> None:
        """Loads the config file into memory."""
        try:
            with open(filename, "rb") as data:
                self.config = tomli.load(data)
        except FileNotFoundError:
            raise FileNotFoundError("Config file not found.")

    def get_config(self) -> dict:
        """Retrieves the loaded configuration file."""
        return self.config
