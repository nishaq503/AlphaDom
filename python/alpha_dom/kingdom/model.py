"""Implements Dominion kindom as a pydantic model."""

import json
import pathlib
import random
import typing

import pydantic

from ..cards import Card
from ..cards import Expansion
from ..cards import load
from ..cards import load_common


class Board(pydantic.BaseModel):
    """A pydantic model for a board in Dominion.

    Attributes:
        name: A name for the board.
        kingdom_names: Names of kingdom cards in the board.
        kingdom: Kingdom cards in the board.
        non_kingdom_supply: Common cards in the board.
        trash: Cards in the trash and their multiplicity.

    """

    name: str
    kingdom_names: list[str]
    kingdom: list[Card]
    non_kingdom_supply: list[Card]
    trash: dict[Card, int]

    def __str__(self) -> str:
        """Return the name of the board."""
        return self.name

    def __repr__(self) -> str:
        """Return a string representation of the board."""
        line = ", ".join(
            [
                f"kingdom: {self.kingdom}",
            ],
        )
        return f"Board({line})"

    def __eq__(self, other: typing.Self) -> bool:  # type: ignore[override]
        """Return whether the boards are identical.

        Args:
            other: The other board.


        Returns:
            Whether the boards are identical.
        """
        # TODO: decide if this is really what equality should mean
        # Should we account for what is in the trash or should this
        # only consider the starting state?

        return self.kingdom_names == other.kingdom_names

    def __lt__(self, other: typing.Self) -> bool:  # type: ignore[override]
        """Allows sorting kindgoms by name."""
        return self.name < other.name

    def __hash__(self) -> int:
        """Returns the hash of the card."""
        return hash(self.name)

    def save(self, dir_path: pathlib.Path) -> None:
        """Save the card to a json file."""
        with dir_path.joinpath(f"{self.name}.json").open("w") as f:
            json.dump(self.dict(), f, indent=2)


def load_random() -> Board:
    """Load board with 10 random kingdom cards from the Base set."""
    kingdom_names: list[str] = random.sample(Expansion.Base.list_names(), 10)

    name = "-".join(kingdom_names)

    return Board(name=name, kingdom_names=kingdom_names)


def load_suggested() -> Board:
    """Load voard from suggested set of kingdom cards."""
    raise NotImplementedError


def load_board(path: pathlib.Path) -> Board:
    """Load a board from a json file."""
    if path.exists():
        with path.open() as f:
            board = Board(**json.load(f))

            board.kingdom = []
            for card in board.kingdom_names:
                board.kingdom.append(load(card))

            board.non_kingdom_supply = load_common()

            # TODO: Account for the fact that not every set needs curses
            # Conditionally remove from common? Or load common cards indiviudally?

            return board

    msg = f"{path} is not a valid path to a board"
    raise FileNotFoundError(msg)
