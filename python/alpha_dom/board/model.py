"""Implements Dominion kingdom as a pydantic model."""

import enum
import json
import pathlib
import random
import typing

import pydantic

from .. import cards


class Board(pydantic.BaseModel):
    """A pydantic model for a board in Dominion.

    Attributes:
        name: A name for the board.
        kingdom_names: Names of kingdom cards in the board.
        non_kingdom_supply: Common cards in the board.
        trash: Cards in the trash and their multiplicity.
    """

    name: str
    kingdom_supply_cards: list[cards.Card]
    non_kingdom_supply_cards: list[cards.Card] = []
    trash: dict[cards.Card, int] = {}

    def __str__(self) -> str:
        """Return the name of the board."""
        return self.name

    def __repr__(self) -> str:
        """Return a string representation of the board."""
        line = ", ".join(
            [
                f"name: {self.name}",
                f"kingdom_supply_cards: {self.kingdom_supply_cards}",
                f"non_kingdom_supply_cards: {self.non_kingdom_supply_cards}",
                f"trash: {self.trash}",
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
        # TODO: Ensure that the same kingdom cards
        # listed in a different order are equal
        return self.name == other.name

    def __lt__(self, other: typing.Self) -> bool:  # type: ignore[override]
        """Allows sorting kindgoms by name."""
        return self.name < other.name

    def __hash__(self) -> int:
        """Returns the hash of the card."""
        return hash(self.name)

    def __init__(self, *, name: str, kingdom_supply_cards: list[str]) -> None:
        """Initialize the board."""
        has_witch = "Witch" in kingdom_supply_cards
        super().__init__(
            name=name,
            kingdom_supply_cards=list(map(cards.load, kingdom_supply_cards)),
            non_kingdom_supply_cards=cards.load_common(load_curse=has_witch),
        )

    def save(self, dir_path: pathlib.Path) -> None:
        """Save the card to a json file."""
        with dir_path.joinpath(f"{self.name}.json").open("w") as f:
            json.dump(self.model_dump(exclude_defaults=True), f, indent=2)


def load_random() -> Board:
    """Load board with 10 random kingdom cards from the Base set."""
    kingdom_supply_cards: list[str] = random.sample(
        cards.Expansion.Base.list_names(),
        10,
    )
    kingdom_supply_cards.sort()

    name = "-".join(kingdom_supply_cards)

    return Board(name=name, kingdom_supply_cards=kingdom_supply_cards)


def load(path: pathlib.Path) -> Board:
    """Load a board from a json file."""
    if path.exists():
        with path.open() as f:
            return Board(**json.load(f))

    msg = f"{path} is not a valid path to a board"
    raise FileNotFoundError(msg)


class SuggestedSet(str, enum.Enum):
    """The suggested boards for base-game Dominion."""

    DeckTop = "DeckTop"
    FirstGame = "FirstGame"
    SizeDistortion = "SizeDistortion"


def load_suggested(name: SuggestedSet) -> Board:
    """Load board from suggested set of kingdom cards."""
    return load(
        pathlib.Path(__file__).parent.joinpath("suggested_sets", f"{name.value}.json"),
    )
