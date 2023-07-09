"""A pydantic model for a player in Dominion."""

import random
import typing

import pydantic

from alpha_dom import cards


class Player(pydantic.BaseModel):
    """A pydantic model for a player in Dominion.

    Attributes:
        id: A unique identifier for the player.
        deck: Cards in the player's deck and their multiplicity.
        draw_pile: Cards in the player's draw pile.
        hand: Cards in the player's hand and their multiplicity.
        discard_pile: Cards in the player's discard pile and their multiplicity.
    """

    name: int
    deck: dict[cards.Card, int] = {
        cards.load("Copper"): 7,
        cards.load("Estate"): 3,
    }
    draw_pile: list[cards.Card] = []
    hand: dict[cards.Card, int] = {}
    discard_pile: dict[cards.Card, int] = {}

    def __str__(self) -> str:
        """Return the id of the player."""
        return self.id

    def __repr__(self) -> str:
        """Return a string representation of the player."""
        line = ", ".join(
            [
                f"id: {self.id}",
                f"deck: {self.deck}",
                f"draw_pile: {self.draw_pile}",
                f"hand: {self.hand}",
                f"discard_pile: {self.discard_pile}",
            ],
        )
        return f"Player({line})"

    def __eq__(self, other: typing.Self) -> bool:  # type: ignore[override]
        """Return whether the players are identical."""
        return self.id == other.id

    def __lt__(self, other: typing.Self) -> bool:  # type: ignore[override]
        """Allows sorting players by id."""
        return self.id < other.id

    def __hash__(self) -> int:
        """Returns the hash of the player."""
        return hash(self.id)

    def draw(self, n: int = 1) -> None:
        """Draw `n` cards from the draw pile."""
        for _ in range(n):
            if not self.draw_pile:
                self.draw_pile = [
                    card
                    for card, multiplicity in self.discard_pile.items()
                    for _ in range(multiplicity)
                ]
                random.shuffle(self.draw_pile)
                self.discard_pile = {}

            # Draw a card from the draw pile and add it to the hand
            card = self.draw_pile.pop()
            self.hand[card] = self.hand.get(card, 0) + 1
