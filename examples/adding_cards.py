"""Adding cards from the base set."""

from alpha_dom.cards import Card


def _main() -> None:  # noqa: PLR0915
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
        description="+2 cards, when another player plays an attack card, you may reveal this from your hand. If you do, you are unaffected by that attack",  # noqa: E501
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

    workshop = Card(
        name="Workshop",
        cost=3,
        types=["Action"],
        description="Gain a card costing up to 4 coins",
        expansion="base",
    )
    workshop.save()

    harbinger = Card(
        name="Harbinger",
        cost=3,
        types=["Action"],
        description="+1 Card. +1 Action. Look through your discard pile. You may put a card from it onto your deck",  # noqa: E501
        expansion="base",
    )
    harbinger.save()

    merchant = Card(
        name="Merchant",
        cost=3,
        types=["Action"],
        description="+1 Card. +1 Action. The first time you play a Silver this turn, +1 Coin",  # noqa: E501
        expansion="base",
    )
    merchant.save()

    vassal = Card(
        name="Vassal",
        cost=3,
        types=["Action"],
        description="+2 Coins. Discard the top card of your deck. If it's an Action card, you may play it",  # noqa: E501
        expansion="base",
    )
    vassal.save()

    smithy = Card(
        name="Smithy",
        cost=4,
        types=["Action"],
        description="+3 cards",
        expansion="base",
    )
    smithy.save()

    remodel = Card(
        name="Remodel",
        cost=4,
        types=["Action"],
        description="Trash a card from your hand. Gain a card costing up to 2 coins more than the trashed card",  # noqa: E501
        expansion="base",
    )
    remodel.save()

    gardens = Card(
        name="Gardens",
        cost=4,
        types=["Victory"],
        description="Worth 1 VP per 10 cards you have (rounded down)",
        expansion="base",
    )
    gardens.save()

    moneylender = Card(
        name="Moneylender",
        cost=4,
        types=["Action"],
        description="Trash a Copper from your hand.\nIf you do, +3 Coins",
        expansion="base",
    )
    moneylender.save()

    militia = Card(
        name="Militia",
        cost=4,
        types=["Action", "Attack"],
        description="+2 coins. Each other player discards down to 3 cards in hand",  # noqa: E501
        expansion="base",
    )
    militia.save()

    bureaucrat = Card(
        name="Bureaucrat",
        cost=4,
        types=["Action", "Attack"],
        description="Gain a Silver onto your deck. Each other player reveals a Victory card from their hand and puts it onto their deck (or reveals a hand with no Victory cards)",  # noqa: E501
        expansion="base",
    )
    bureaucrat.save()

    poacher = Card(
        name="Poacher",
        cost=4,
        types=["Action"],
        description="+1 Card, +1 Action, +1 Coin. Discard a card per empty Supply pile",
        expansion="base",
    )
    poacher.save()

    throne_room = Card(
        name="Throne Room",
        cost=4,
        types=["Action"],
        description="Choose an Action card in your hand. Play it twice",
        expansion="base",
    )
    throne_room.save()

    market = Card(
        name="Market",
        cost=5,
        types=["Action"],
        description="+1 card, +1 action, +1 buy, +1 coin",
        expansion="base",
    )
    market.save()

    mine = Card(
        name="Mine",
        cost=5,
        types=["Action"],
        description="Trash a Treasure card from your hand. Gain a Treasure card costing up to 3 coins more; put it into your hand",  # noqa: E501
        expansion="base",
    )
    mine.save()

    witch = Card(
        name="Witch",
        cost=5,
        types=["Action", "Attack"],
        description="+2 cards. Each other player gains a Curse card",
        expansion="base",
    )
    witch.save()

    library = Card(
        name="Library",
        cost=5,
        types=["Action"],
        description="Draw until you have 7 cards in hand. You may set aside any Action cards drawn this way, and then discard them",  # noqa: E501
        expansion="base",
    )
    library.save()

    festival = Card(
        name="Festival",
        cost=5,
        types=["Action"],
        description="+2 actions, +1 buy, +2 coins",
        expansion="base",
    )
    festival.save()

    bandit = Card(
        name="Bandit",
        cost=5,
        types=["Action", "Attack"],
        description="Gain a Gold. Each other player reveals the top 2 cards of their deck, trashes a revealed Treasure other than Copper, and discards the rest",  # noqa: E501
        expansion="base",
    )
    bandit.save()

    sentry = Card(
        name="Sentry",
        cost=5,
        types=["Action"],
        description="+1 card, +1 action. Look at the top 2 cards of your deck. You may trash and/or discard any number of them. Put the rest back on top in any order",  # noqa: E501
        expansion="base",
    )
    sentry.save()

    council_room = Card(
        name="Council Room",
        cost=5,
        types=["Action"],
        description="+4 Cards\n+1 Buy\nEach other player draws a card",
        expansion="base",
    )
    council_room.save()

    artisan = Card(
        name="Artisan",
        cost=6,
        types=["Action"],
        description="Gain a card to your hand costing up to 5 coins. Put a card from your hand onto your deck",  # noqa: E501
        expansion="base",
    )
    artisan.save()


if __name__ == "__main__":
    _main()
