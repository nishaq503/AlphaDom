"""Adding cards from the base set."""

from alpha_dom.cards import Card


def _main() -> None:
    copper = Card(
        name="Copper",
        cost=0,
        types=["Treasure"],
        description="+1 coin",
        expansion="base",
    )
    copper.save()

    silver = Card(
        name="Silver",
        cost=3,
        types=["Treasure"],
        description="+2 coin",
        expansion="base",
    )
    silver.save()

    gold = Card(
        name="Gold",
        cost=6,
        types=["Treasure"],
        description="+3 coin",
        expansion="base",
    )
    gold.save()

    estate = Card(
        name="Estate",
        cost=2,
        types=["Victory"],
        description="+1 victory point",
        expansion="base",
    )
    estate.save()

    duchy = Card(
        name="Duchy",
        cost=5,
        types=["Victory"],
        description="+3 victory points",
        expansion="base",
    )
    duchy.save()

    province = Card(
        name="Province",
        cost=8,
        types=["Victory"],
        description="+6 victory points",
        expansion="base",
    )
    province.save()

    curse = Card(
        name="Curse",
        cost=0,
        types=["Curse"],
        description="-1 victory point",
        expansion="base",
    )
    curse.save()

    cellar = Card(
        name="Cellar",
        cost=2,
        types=["Action"],
        description="+1 action, discard any number of cards, +1 card per card discarded",  # noqa: E501
        expansion="base",
    )
    cellar.save()

    chapel = Card(
        name="Chapel",
        cost=2,
        types=["Action"],
        description="Trash up to 4 cards from your hand",
        expansion="base",
    )
    chapel.save()

    moat = Card(
        name="Moat",
        cost=2,
        types=["Action", "Reaction"],
        description="+2 cards, when another player plays an attack card, you may reveal this from your hand, if you do, you are unaffected by that attack",  # noqa: E501
        expansion="base",
    )
    moat.save()

    village = Card(
        name="Village",
        cost=3,
        types=["Action"],
        description="+1 card, +2 actions",
        expansion="base",
    )
    village.save()


if __name__ == "__main__":
    _main()
