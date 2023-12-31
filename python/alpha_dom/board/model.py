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
        kingdom_supply_cards: The kingdom cards in the board.
        non_kingdom_supply: The common cards in the board.
        trash: Cards in the trash and their multiplicity.
        supply: Cards in the supply and their multiplicity.
    """

    name: str
    kingdom_supply_cards: list[cards.Card]
    non_kingdom_supply_cards: list[cards.Card] = []
    trash: dict[cards.Card, int] = {}
    supply: dict[cards.Card, int] = {}

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
                f"supply: {self.supply}",
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
        """Allows sorting kingdoms by name."""
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

    def gen_name(self, *, replace: bool) -> str:
        """Generate a name for the board.

        A `Kingdom` is a set of 10 kingdom cards. The name of the board is
        generated by concatenating the names of the kingdom cards in
        alphabetical order, separated by a hyphen.

        Args:
            replace: Whether to replace the name of the board.

        Returns:
            The auto-generated name of the board.
        """
        card_names = sorted(map(str, self.kingdom_supply_cards))
        name = "-".join(c.lower() for c in card_names)

        if replace:
            self.name = name

        return name

    @property
    def kingdom_cards(self) -> list[cards.Card]:
        """Return the kingdom cards in the board."""
        return self.kingdom_supply_cards + self.non_kingdom_supply_cards

    def set_initial_supply(self, num_players: int = 2) -> None:
        """Set initial card counts for supply cards.

        Args:
            num_players: The number of players in the game.
        """
        # TODO: Make a class hierarchy for cards and move this logic to the cards'
        # own class
        for card in self.kingdom_cards:
            if card.name == "Copper":
                self.supply[card] = 60
            elif card.name == "Silver":
                self.supply[card] = 40
            elif card.name == "Gold":
                self.supply[card] = 30
            elif card.name == "Curse":
                self.supply[card] = 10 * (num_players - 1)
            elif "Victory" in card.types:
                self.supply[card] = 4 + 2 * num_players
            else:  # "Action" in card.types
                self.supply[card] = 10


def load_random() -> Board:
    """Load board with 10 random kingdom cards from the Base set."""
    kingdom_supply_cards: list[str] = random.sample(
        cards.Expansion.Base.list_names(),
        10,
    )
    kingdom_supply_cards.sort()
    return load_custom(kingdom_supply_cards)


def load(path: pathlib.Path) -> Board:
    """Load a board from a json file."""
    if path.exists():
        with path.open() as f:
            return Board(**json.load(f))

    msg = f"{path} is not a valid path to a board"
    raise FileNotFoundError(msg)


def load_custom(cards: list[str], *, name: str | None = None) -> Board:
    """Load a board with the given cards."""
    b = Board(name="Custom", kingdom_supply_cards=cards)

    if name is None:
        b.gen_name(replace=True)
    else:
        b.name = name

    return b


class SuggestedSet(str, enum.Enum):
    """The suggested boards for base-game Dominion."""

    FirstGame = "FirstGame"
    SizeDistortion = "SizeDistortion"
    DeckTop = "DeckTop"


def load_suggested(name: SuggestedSet) -> Board:
    """Load board from suggested set of kingdom cards."""
    return load(
        pathlib.Path(__file__).parent.joinpath("suggested_sets", f"{name.value}.json"),
    )
