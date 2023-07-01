"""Experiments with kingdoms."""

import pprint

from alpha_dom import board


def main() -> None:
    """Just some experiments."""
    deck_top = board.load_suggested(board.SuggestedSet.DeckTop)

    print(deck_top.name)
    pprint.pprint(deck_top.kingdom_names)


if __name__ == "__main__":
    main()
