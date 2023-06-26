"""Provides the models for the cards from the base game."""

from . import model
from .model import Card
from .model import Expansion
from .model import Type

__base_cards = model.load_base()
__common_cards = model.load_common()

__all_cards = __common_cards + __base_cards


def __getattr__(name: str) -> Card | list[Card]:
    if name == "list":
        return __all_cards

    return model.load(name, Expansion.Base)
