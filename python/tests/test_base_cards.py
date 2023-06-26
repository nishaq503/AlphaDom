"""Tests for cards in the base expansion."""

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

    base_cards = cards.list_base
    assert len(base_cards) == len(true_names), "Incorrect number of cards."

    for card in base_cards:
        assert card.name in true_names, f"{card.name} not in true_names."


def test_common_cards() -> None:
    """Test that all common cards in the base expansion are in the `cards` module."""
    true_names = [
        "Copper",
        "Curse",
        "Duchy",
        "Estate",
        "Gold",
        "Province",
        "Silver",
    ]

    common_cards = cards.list_common
    assert len(common_cards) == len(true_names), "Incorrect number of cards."

    for card in common_cards:
        assert card.name in true_names, f"{card.name} not in true_names."
