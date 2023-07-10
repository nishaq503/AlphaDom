"""A pydantic model for a player in Dominion."""

import random
import typing

import pydantic

from alpha_dom import board
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
    turn_money: int = 0
    turn_actions: int = 1
    turn_buys: int = 1
    cards_in_play: list[cards.Card] = []

    def __str__(self) -> str:
        """Return the id of the player."""
        return str(self.name)

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
        location: typing.Literal["DiscardPile", "DrawPile", "Hand"],
        board: board.Board,
    ) -> board.Board:
        """Gain a card to the specified location."""
        if location == "DiscardPile":
            self.discard_pile[card] = self.discard_pile.get(card, 0) + 1
        elif location == "DrawPile":
            self.draw_pile.append(card)
        elif location == "Hand":
            self.hand[card] = self.hand.get(card, 0) + 1
        else:
            msg = f"Invalid location: {location}. Can only gain to 'DiscardPile', 'DrawPile', or 'Hand'."  # noqa: E501
            raise ValueError(
                msg,
            )

        # (Not sure where supply should be stored yet and
        # which classes should be able to edit it). Should a player hold a copy?
        # Should some Game or GameState class deal with this?
        # I think it is better that gain/trash not return an edited board
        # but rather edit it directly.
        board.supply[card] -= 1
        return board

    def buy(self, card: cards.Card, board: board.Board) -> board.Board:
        """Buy a card."""
        # I assume we would want to check "legality" of a buy before we get here.
        # i.e. check if the card is (still) in the supply, if the player has
        # enough money, enough buys, etc.
        self.turn_money -= card.cost
        self.turn_buys -= 1
        self.gain(card, "DiscardPile", board)
        return board

    def cleanup(self) -> None:
        """Clean up the player's turn."""
        for card, multiplicity in self.hand.items():
            if card in self.discard_pile:
                self.discard_pile[card] += multiplicity
            else:
                self.discard_pile[card] = multiplicity

        self.hand = {}

        for card in self.cards_in_play:
            if card in self.discard_pile:
                self.discard_pile[card] += 1
            else:
                self.discard_pile[card] = 1

        self.cards_in_play = []

        self.turn_money = 0
        self.turn_actions = 1
        self.turn_buys = 1

    def trash(
        self,
        board: board.Board,
        card: cards.Card,
        location: typing.Literal["Hand", "OpponentDrawPile", "Supply"],
        opponent: typing.Self | None,
    ) -> board.Board:
        """Trash a card."""
        # I assume we would want to check "legality" of a trash before we get here.
        # i.e. check if the card is in the player's hand/draw pile,if the card is
        # in the supply (if you're  dict[cards.Card, int] trying to trash from supply)
        # etc.
        #
        # As with gain, I'm not happy about this function returning board. That seems
        # like the incorrect choice, but I am leaving it for now and we can reevaluate
        # when we decide what a Game or GameState class should look like and how
        # players will interact with communal aspects of the game.

        if location == "Hand":
            self.hand[card] -= 1

        elif location == "OpponentDrawPile":
            # My thought for the flow here is that, say for a card like Bandit,
            # the play method for Bandit would first draw the opponent's top card,
            # then check if it is a silver or gold, and then call this method
            # with the opponent's draw pile as the location and silver or
            # gold as the card. So you would always know that the card is in
            # the opponent's draw pile before getting here.
            if opponent is None:
                msg = "No opponent provided."
                raise ValueError(msg)

            opponent.draw_pile[card] -= 1  # type: ignore[call-overload]

        elif location == "Supply":
            board.supply[card] -= 1

        else:
            pass

        board.trash[card] = board.trash.get(card, 0) + 1
        return board
