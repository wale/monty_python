from typing import Optional

from sqlmodel import BigInteger, Column, Field, ForeignKey, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column=Column(BigInteger(), primary_key=True, autoincrement=False),
    )
    timezone: str = Field(default=None)
    pronouns: Optional["Pronoun"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False},
    )


class Pronoun(SQLModel, table=True):
    user_id: Optional[int] = Field(
        primary_key=True,
        foreign_key="user.id",
        default=None,
        sa_column=Column(BigInteger(), ForeignKey("user.id"), primary_key=True),
    )
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={
            "uselist": False,
            "single_parent": True,
        },
        back_populates="pronouns",
    )
    subj: str | None  # Subject pronoun
    obj: str | None  # Object pronoun
    posDet: str | None  # Possessive determiner
    posPro: str | None  # Possessive pronoun
    refl: str | None  # Reflexive pronoun
