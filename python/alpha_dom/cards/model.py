"""Implements Dominion cards as a pydantic model."""

import enum
import json
import pathlib
import typing

import pydantic


class Type(str, enum.Enum):
    """The types of cards in Dominion."""

    Victory = "Victory"
    Treasure = "Treasure"
    Action = "Action"
    Attack = "Attack"
    Reaction = "Reaction"
    Curse = "Curse"


class Expansion(str, enum.Enum):
    """The expansions of Dominion."""

    base = "base"


class Card(pydantic.BaseModel):
    """A pydantic model for a card in Dominion."""

    name: str
    cost: int
    types: list[Type]
    description: str
    expansion: Expansion

    def __str__(self) -> str:
        """Return the name of the card."""
        return self.name

    def __repr__(self) -> str:
        """Return a string representation of the card."""
        line = ", ".join(
            [
                self.name,
                str(self.cost),
                ", ".join(self.types),
                self.description,
                self.expansion,
            ],
        )
        return f"Card({line})"

    def __eq__(self, other: typing.Self) -> bool:  # type: ignore[override]
        """Return whether the cards are equal."""
        return self.name == other.name

    def __hash__(self) -> int:
        """Return the hash of the card."""
        return hash(self.name)

    def save(self) -> None:
        """Save the card to a json file."""
        path = pathlib.Path(__file__).parent.joinpath(
            "expansions",
            self.expansion.value,
            f"{self.name}.json",
        )
        with path.open("w") as f:
            json.dump(self.dict(), f, indent=2)
