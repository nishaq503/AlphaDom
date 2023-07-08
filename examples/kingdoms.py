"""Experiments with kingdoms."""


from alpha_dom import board


def main() -> None:
    """Just some experiments."""
    deck_top = board.load_suggested(board.SuggestedSet.DeckTop)

    print(deck_top.name)
    list(map(print, (x.name for x in deck_top.kingdom_cards)))


if __name__ == "__main__":
    main()
