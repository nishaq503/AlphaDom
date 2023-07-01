"""Tests for cards in the base game."""

from alpha_dom import cards


def test_base_cards() -> None:
    """Test that all kingdom cards in the Base expansion are in the `cards` module."""
    true_names = [
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
        "Library",
        "Market",
        "Merchant",
        "Militia",
        "Mine",
        "Moat",
        "Moneylender",
        "Poacher",
        "Remodel",
        "Sentry",
        "Smithy",
        "Throne Room",
        "Vassal",
        "Village",
        "Witch",
        "Workshop",
    ]

    base_names = cards.Expansion.Base.list_names()
    assert len(true_names) == len(
        base_names,
    ), f"Incorrect number of cards. {len(true_names)} != {len(base_names)}"
    assert set(true_names) == set(
        base_names,
    ), f"Incorrect names. {set(true_names)} != {set(base_names)}"

    base_cards = cards.load_base()
    assert len(base_cards) == len(true_names), "Incorrect number of cards."

    for card in base_cards:
        assert card.name in true_names, f"{card.name} not in true_names."
