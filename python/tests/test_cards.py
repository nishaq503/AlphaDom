"""Test that all cards in the game can be loaded."""

import pathlib
import tempfile

import pytest
from alpha_dom import cards
from alpha_dom.cards import Expansion
from alpha_dom.cards import Type


def test_loading_cards() -> None:
    """Test that all cards in the base expansion can be loaded."""
    names = Expansion.Common.list_names() + Expansion.Base.list_names()
    for name in names:
        card = cards.load(name)
        assert card.name == name, f"Card {name} not loaded correctly."


def test_loading_unknown_card() -> None:
    """Test that loading an unknown card raises an error."""
    with pytest.raises(FileNotFoundError):
        cards.load("Nobles")


def test_loading_expansions() -> None:
    """Test that all expansions can be loaded."""
    for expansion in Expansion:
        num_cards = len(expansion.list_names())
        loaded_cards = cards.load_expansion(expansion)
        assert num_cards == len(
            loaded_cards,
        ), (
            f"Incorrect number of cards in {expansion}. "
            f"{num_cards} != {len(loaded_cards)}"
        )


def test_sorting_cards() -> None:
    """Test that cards can be sorted."""
    cards_list = cards.load_all()
    cards_list.sort()
    for i in range(len(cards_list) - 1):
        assert (
            cards_list[i] < cards_list[i + 1]
        ), f"Cards not sorted correctly. {cards_list[i]} > {cards_list[i + 1]}"

    artisan = cards.load("Artisan", Expansion.Base)
    assert (
        artisan == cards_list[0]
    ), f"Artisan not first card. {artisan} != {cards_list[0]}"


def test_card_representations() -> None:
    """Tests that some cards have the correct string representations."""
    artisan = cards.load("Artisan", Expansion.Base)
    assert artisan.name == "Artisan", f"Artisan name is not Artisan. {artisan.name}"
    assert str(artisan) == "Artisan", f"Artisan string is not Artisan. {artisan!s}"

    artisan_repr = (
        "name: Artisan, "
        "cost: 6, "
        "types: [Action], "
        "description: Gain a card to your hand costing up to 5 coins. "
        "Put a card from your hand onto your deck, "
        "expansion: Base, "
        "associated_cards: []"
    )
    artisan_repr = f"Card({artisan_repr})"
    assert artisan_repr == repr(
        artisan,
    ), f"Artisan repr is not correct. {artisan_repr} != {artisan!r}"

    witch = cards.load("Witch", Expansion.Base)
    assert witch.name == "Witch", f"Witch name is not Witch. {witch.name}"
    assert str(witch) == "Witch", f"Witch string is not Witch. {witch!s}"

    witch_repr = (
        "name: Witch, "
        "cost: 5, "
        "types: [Action, Attack], "
        "description: +2 cards. Each other player gains a Curse card, "
        "expansion: Base, "
        "associated_cards: [Curse]"
    )
    witch_repr = f"Card({witch_repr})"
    assert witch_repr == repr(
        witch,
    ), f"Witch repr is not correct. {witch_repr} != {witch!r}"


def test_hash() -> None:
    """Test that cards are hashed properly."""
    artisan = cards.load("Artisan", Expansion.Base)
    hash_ = hash("Artisan")
    assert hash_ == hash(
        artisan,
    ), f"Artisan hash is not correct. {hash_} != {hash(artisan)}"


def test_card_types() -> None:
    """Test that all cards have a type."""
    artisan = cards.load("Artisan", Expansion.Base)
    assert artisan.types == [
        Type.Action,
    ], f"Artisan type is not Action. {artisan.types}"

    witch = cards.load("Witch", Expansion.Base)
    assert witch.types == [
        Type.Action,
        Type.Attack,
    ], f"Witch type is not Action_Attack. {witch.types}"

    copper = cards.load("Copper", Expansion.Common)
    assert copper.types == [
        Type.Treasure,
    ], f"Copper type is not Treasure. {copper.types}"

    curse = cards.load("Curse", Expansion.Common)
    assert curse.types == [Type.Curse], f"Curse type is not Curse. {curse.types}"

    estate = cards.load("Estate", Expansion.Common)
    assert estate.types == [Type.Victory], f"Estate type is not Victory. {estate.types}"

    moat = cards.load("Moat", Expansion.Base)
    assert moat.types == [
        Type.Action,
        Type.Reaction,
    ], f"Moat type is not Action_Reaction. {moat.types}"


def test_card_cost() -> None:
    """Tests that some cards have the correct cost."""
    province = cards.load("Province", Expansion.Common)
    assert province.cost == 8, f"Province cost is not 8. {province.cost}"

    artisan = cards.load("Artisan", Expansion.Base)
    assert artisan.cost == 6, f"Artisan cost is not 6. {artisan.cost}"

    witch = cards.load("Witch", Expansion.Base)
    assert witch.cost == 5, f"Witch cost is not 5. {witch.cost}"

    smithy = cards.load("Smithy", Expansion.Base)
    assert smithy.cost == 4, f"Smithy cost is not 4. {smithy.cost}"

    village = cards.load("Village", Expansion.Base)
    assert village.cost == 3, f"Village cost is not 3. {village.cost}"

    moat = cards.load("Moat", Expansion.Base)
    assert moat.cost == 2, f"Moat cost is not 2. {moat.cost}"

    copper = cards.load("Copper", Expansion.Common)
    assert copper.cost == 0, f"Copper cost is not 0. {copper.cost}"


def test_saving_cards() -> None:
    """Test that cards can be saved."""
    with tempfile.TemporaryDirectory() as cards_dir:
        path = pathlib.Path(cards_dir).joinpath("Artisan.json")
        artisan = cards.load("Artisan")
        artisan.save(path.parent)

        assert path.exists(), "Artisan not saved."


def test_associated_cards() -> None:
    """Test associated cards."""
    artisan = cards.load("Artisan")
    assert artisan.associated_cards == [], "Artisan has associated cards."

    curse = cards.load("Curse")
    witch = cards.load("Witch")
    assert witch.associated_cards == [curse], "Witch has incorrect associated cards."

    for c in cards.load_all():
        if c.name == "Witch":
            assert c.associated_cards == [
                curse,
            ], f"{c.name} has incorrect associated cards."
        else:
            assert c.associated_cards == [], f"{c.name} has associated cards."
