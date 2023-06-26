"""Tests for cards in the base expansion."""

from alpha_dom import cards


def test_cards() -> None:
    """Test that all cards in the base expansion are present in the `cards` module."""
    true_names = [
        "Artisan",
        "Bandit",
        "Bureaucrat",
        "Cellar",
        "Chapel",
        "Copper",
        "Council Room",
        "Curse",
        "Duchy",
        "Estate",
        "Festival",
        "Gardens",
        "Gold",
        "Harbinger",
        "Library",
        "Market",
        "Merchant",
        "Militia",
        "Mine",
        "Moat",
        "Moneylender",
        "Poacher",
        "Province",
        "Remodel",
        "Sentry",
        "Silver",
        "Smithy",
        "Throne Room",
        "Vassal",
        "Village",
        "Witch",
        "Workshop",
    ]

    base_cards = cards.list
    assert len(base_cards) == len(true_names), "Incorrect number of cards."

    for card in base_cards:
        assert card.name in true_names, f"{card.name} not in true_names."
