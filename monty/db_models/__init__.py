from typing import Optional

from sqlmodel import BigInteger, Column, Field, ForeignKey, Relationship, SQLModel


class User(SQLModel, table=True):
    id: int = Field(
        default=None,
        primary_key=True,
        sa_column=Column(BigInteger(), primary_key=True, autoincrement=False),
    )
    timezone: str = Field(default=None)
    pronouns: Optional["Pronoun"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False, "cascade": "all, delete-orphan"},
    )


class Pronoun(SQLModel, table=True):
    user_id: int = Field(
        primary_key=True,
        foreign_key="user.id",
        sa_column=Column(BigInteger(), ForeignKey("user.id"), primary_key=True),
    )
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={
            "uselist": False,
            "cascade": "all, delete-orphan",
            "single_parent": True,
        },
        back_populates="pronouns",
    )
    subj: str  # Subject pronoun
    obj: str  # Object pronoun
    posDet: str  # Possessive determiner
    posPro: str  # Possessive pronoun
    refl: str  # Reflexive pronoun
