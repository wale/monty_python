import sqlmodel

from .config import Config

config_class = Config()
config = config_class.get_config()

engine = sqlmodel.create_engine(config['bot']['db']['url'])

session = sqlmodel.SQLModel.metadata.create_all(engine)