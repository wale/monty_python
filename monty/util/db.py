import sqlmodel

from monty.main import config

engine = sqlmodel.create_engine(config["bot"]["db"]["url"])

session = sqlmodel.SQLModel.metadata.create_all(engine)
