from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    timezone: str = Field(default=None)
    pronouns: Optional["Pronoun"] = Relationship(back_populates="user")


class Pronoun(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True, foreign_key="user.id")
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"uselist": False}, back_populates="pronouns"
    )
    subj: str  # Subject pronoun
    obj: str  # Object pronoun
    posDet: str  # Possessive determiner
    posPro: str  # Possessive pronoun
    refl: str  # Reflexive pronoun
