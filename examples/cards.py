"""Experiments with cards."""


from alpha_dom import cards


def main() -> None:
    """Just some experiments."""
    base_cards = cards.load_expansion(cards.Expansion.Base)
    print(", ".join(map(str, base_cards)))


if __name__ == "__main__":
    main()
