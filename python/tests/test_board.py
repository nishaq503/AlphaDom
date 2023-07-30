"""Test certain components of the Board class."""


import pathlib
import tempfile

from alpha_dom import board
from alpha_dom import cards


def test_board() -> None:
    """Tests that board members are correct."""
    b = board.Board(
        name="Test",
        kingdom_supply_cards=[
            "Cellar",
            "Chapel",
            "Moat",
            "Harbinger",
            "Merchant",
            "Vassal",
            "Village",
            "Workshop",
            "Bureaucrat",
            "Gardens",
        ],
    )

    assert (
        cards.load("Estate") in b.non_kingdom_supply_cards
    ), "Estate not in non-kingdom supply cards."
    assert (
        cards.load("Duchy") in b.non_kingdom_supply_cards
    ), "Duchy not in non-kingdom supply cards."
    assert (
        cards.load("Province") in b.non_kingdom_supply_cards
    ), "Province not in non-kingdom supply cards."

    assert (
        cards.load("Curse") not in b.non_kingdom_supply_cards
    ), "Curse in non-kingdom supply cards."

    assert (
        cards.load("Copper") in b.non_kingdom_supply_cards
    ), "Copper not in non-kingdom supply cards."
    assert (
        cards.load("Silver") in b.non_kingdom_supply_cards
    ), "Silver not in non-kingdom supply cards."
    assert (
        cards.load("Gold") in b.non_kingdom_supply_cards
    ), "Gold not in non-kingdom supply cards."

    b = board.Board(
        name="Test",
        kingdom_supply_cards=[
            "Cellar",
            "Chapel",
            "Moat",
            "Harbinger",
            "Merchant",
            "Vassal",
            "Village",
            "Workshop",
            "Bureaucrat",
            "Witch",
        ],
    )

    assert (
        cards.load("Curse") in b.non_kingdom_supply_cards
    ), "Curse not in non-kingdom supply cards."


def test_loading_kingdoms() -> None:
    """Test that all preset kingdoms can be loaded."""
    for s in board.SuggestedSet:
        b = board.load_suggested(s)

        assert b.name == s.value, f"Board {s} not loaded correctly."


def test_loading_random() -> None:
    """Test that random boards are loaded correctly."""
    b = board.load_random()
    assert (
        len(b.kingdom_supply_cards) == 10
    ), f"Random board does not have 10 cards, but {len(b.kingdom_supply_cards)}."

    cards = sorted(map(str, b.kingdom_supply_cards))
    name = "-".join(c.lower() for c in cards)
    assert b.name == name, f"Board was not named correctly. {b.name} != {name}"


def test_loading_custom() -> None:
    """Test that custom boards are loaded correctly."""
    cards = [
        "Artisan",
        "Bandit",
        "Bureaucrat",
        "Cellar",
        "Chapel",
        "Council Room",
        "Festival",
        "Gardens",
        "Harbinger",
        "Laboratory",
    ]

    b = board.load_custom(cards)
    assert (
        len(b.kingdom_supply_cards) == 10
    ), f"Custom board does not have 10 cards, but {len(b.kingdom_supply_cards)}."

    for c in b.kingdom_supply_cards:
        assert (
            c.name in cards
        ), f"Custom board contains card {c} not in the given cards."

    cards = sorted(map(str, cards))
    name = "-".join(c.lower() for c in cards)
    assert b.name == name, f"Board was not named correctly. {b.name} != {name}"


def test_saving() -> None:
    """Test that boards can be saved."""
    cards = [
        "Artisan",
        "Cellar",
        "Market",
        "Merchant",
        "Mine",
        "Moat",
        "Moneylender",
        "Poacher",
        "Remodel",
        "Witch",
    ]
    b = board.load_custom(cards, name="Improvements")

    with tempfile.TemporaryDirectory() as boards_dir:
        path = pathlib.Path(boards_dir).joinpath("Improvements.json")
        b.save(path.parent)

        assert path.exists(), "Board not saved."
