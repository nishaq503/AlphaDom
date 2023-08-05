"""A pydantic model for a player in Dominion."""

import random
import typing

import pydantic

from alpha_dom import board
from alpha_dom import cards


class Player(pydantic.BaseModel):
    """A pydantic model for a player in Dominion.

    Attributes:
        name: A unique identifier for the player.
        draw_pile: Cards in the player's draw pile.
        hand: Cards in the player's hand and their multiplicity.
        discard_pile: Cards in the player's discard pile and their multiplicity.
    """

    name: int

    # deck management
    draw_pile: list[cards.Card] = []
    hand: dict[cards.Card, int] = {}
    discard_pile: dict[cards.Card, int] = {}

    # turn management
    actions: int = 1
    money: int = 0
    buys: int = 1
    cards_in_play: list[cards.Card] = []

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Initialize the player."""
        super().__init__(*args, **kwargs)

        # Shuffle the starting deck
        self.draw_pile = [cards.load("Copper")] * 7 + [cards.load("Estate")] * 3
        random.shuffle(self.draw_pile)

        # Draw 5 cards for the starting hand
        for _ in range(5):
            card: cards.Card = self.draw()  # type: ignore[assignment]
            self.hand[card] = self.hand.get(card, 0) + 1

    def __str__(self) -> str:
        """Return the id of the player."""
        return str(self.name)

    def __repr__(self) -> str:
        """Return a string representation of the player."""
        line = ", ".join(
            [
                f"name: {self.name}",
                f"deck: {self.deck}",
                f"draw_pile: {self.draw_pile}",
                f"hand: {self.hand}",
                f"discard_pile: {self.discard_pile}",
                f"actions: {self.actions}",
                f"money: {self.money}",
                f"buys: {self.buys}",
                f"cards_in_play: {self.cards_in_play}",
            ],
        )
        return f"Player({line})"

    def __eq__(self, other: typing.Self) -> bool:  # type: ignore[override]
        """Return whether the players are identical."""
        return self.name == other.name

    def __lt__(self, other: typing.Self) -> bool:  # type: ignore[override]
        """Allows sorting players by id."""
        return self.name < other.name

    def __hash__(self) -> int:
        """Returns the hash of the player."""
        return hash(self.name)

    def draw(self) -> cards.Card | None:
        """Draw a card from the draw pile.

        Returns:
            - next card in the draw pile if a card can be drawn
            - None if the draw pile and discard pile are both empty
        """
        if not self.draw_pile and not self.discard_pile:
            return None

        if not self.draw_pile:
            self.draw_pile = [
                card
                for card, multiplicity in self.discard_pile.items()
                for _ in range(multiplicity)
            ]
            random.shuffle(self.draw_pile)
            self.discard_pile = {}

        return self.draw_pile.pop()

    def gain(
        self,
        card: cards.Card,
        destination: typing.Literal["DiscardPile", "DrawPile", "Hand"],
        board: board.Board,
    ) -> None:
        """Gain a card to the specified location.

        This method is not responsible for checking if the card can be gained at
        all. That should be done before calling this method.

        This method will edit the board in place, by decrementing the supply pile
        of the card.

        Args:
            card: The card to gain.
            destination: The location to gain the card to.
            board: The board to gain the card from.
        """
        if destination == "DiscardPile":
            self.discard_pile[card] = self.discard_pile.get(card, 0) + 1

        elif destination == "DrawPile":
            # This top-decks the card. We will need to add a way to place the card
            # in an arbitrary position in the draw pile.
            self.draw_pile.append(card)

        elif destination == "Hand":
            self.hand[card] = self.hand.get(card, 0) + 1

        else:
            # TODO: Remove this after implementing an enum for destination
            msg = (
                f"Invalid destination: {destination}. "
                "Can only gain to 'DiscardPile', 'DrawPile', or 'Hand'."
            )
            raise ValueError(msg)

        board.supply[card] -= 1

    def top_deck(
        self,
        card: cards.Card,
        source: typing.Literal["DiscardPile", "Hand"],
    ) -> None:
        """Top deck a card.

        This method is not responsible for checking if the card can be top-decked.
        That should be done before calling this method.

        Args:
            card: The card to top-deck.
            source: The location to top-deck the card from.
        """
        if source == "DiscardPile":
            self.discard_pile[card] -= 1
            self.draw_pile.append(card)

        elif source == "Hand":
            self.hand[card] -= 1
            self.draw_pile.append(card)

        else:
            # TODO: Remove this after implementing an enum for destination
            msg = (
                f"Invalid source: {source}. "
                "Can only top deck from 'DiscardPile' or 'Hand'."
            )
            raise ValueError(msg)

    def buy(self, card: cards.Card, board: board.Board) -> None:
        """Buy a card.

        This method is not responsible for checking if the card can be bought with
        the player's current money and buys. That should be done before calling this
        method.

        This method will edit the board in place, by decrementing the supply pile
        of the card.

        Args:
            card: The card to buy.
            board: The board to buy the card from.
        """
        self.money -= card.cost
        self.buys -= 1
        self.gain(card, "DiscardPile", board)

    def cleanup(self) -> None:
        """Clean up the player's turn."""
        # Discard hand
        for card, multiplicity in self.hand.items():
            self.discard_pile[card] = self.discard_pile.get(card, 0) + multiplicity
        self.hand = {}

        for card in self.cards_in_play:
            self.discard_pile[card] = self.discard_pile.get(card, 0) + 1
        self.cards_in_play = []

        # Draw 5 cards
        for _ in range(5):
            card = self.draw()  # type: ignore[assignment]
            if card is None:
                break
            self.hand[card] = self.hand.get(card, 0) + 1

    def start_turn(self) -> None:
        """Start the player's turn."""
        self.actions = 1
        self.money = 0
        self.buys = 1

    def trash(
        self,
        board: board.Board,
        card: cards.Card,
        source: typing.Literal["Hand", "DrawPile"],
        index: int = -1,
    ) -> None:
        """Trash a card.

        This method assumes that the is in the player's hand or at the specified
        index in the player's draw pile.

        This method will edit the board in place, by incrementing the trash pile
        of the card.

        Args:
            board: The board in which to trash the card.
            card: The card to trash.
            source: From where to trash the card.
            index: The index of the card in the draw pile to trash.

        Raises:
            KeyError: If the card is not in the player's hand.
        """
        if source == "Hand":
            self.hand[card] -= 1

        elif source == "DrawPile":
            self.draw_pile.pop(index)

        else:
            # TODO: Remove this after implementing an enum for source
            msg = (
                f"Invalid source: {source}. "
                "Can only trash from 'Hand' or 'DrawPile'."
            )
            raise ValueError(msg)

        board.trash[card] = board.trash.get(card, 0) + 1
