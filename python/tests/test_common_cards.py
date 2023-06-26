"""Test the common cards in the game."""

from alpha_dom import cards


def test_common_cards() -> None:
    """Test that all common cards are in the `cards` module."""
    true_names = [
        "Copper",
        "Curse",
        "Duchy",
        "Estate",
        "Gold",
        "Province",
        "Silver",
    ]

    common_names = cards.Expansion.Common.list_names()
    assert len(true_names) == len(
        common_names,
    ), f"Incorrect number of cards. {len(true_names)} != {len(common_names)}"
    assert set(true_names) == set(
        common_names,
    ), f"Incorrect names. {set(true_names)} != {set(common_names)}"

    common_cards = cards.load_common()
    assert len(common_cards) == len(true_names), "Incorrect number of cards."

    for card in common_cards:
        assert card.name in true_names, f"{card.name} not in true_names."
