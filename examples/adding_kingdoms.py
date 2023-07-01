"""Adding suggested boards from the base set."""

import pathlib

from alpha_dom.board.model import Board


def _main() -> None:
    """Add suggested boards from the base set."""
    suggested_set_dir_path = pathlib.Path(__file__).parent.parent.joinpath(
        "python",
        "alpha_dom",
        "board",
        "suggested_sets",
    )

    first_game = Board(
        name="first_game",
        kingdom_names=[
            "Cellar",
            "Market",
            "Militia",
            "Mine",
            "Moat",
            "Remodel",
            "Smithy",
            "Village",
            "Woodcutter",
            "Workshop",
        ],
    )

    first_game.save(suggested_set_dir_path)

    size_distortion = Board(
        name="size_distortion",
        kingdom_names=[
            "Artisan",
            "Bandit",
            "Bureaucrat",
            "Chapel",
            "Festival",
            "Gardens",
            "Sentry",
            "Throne Room",
            "Witch",
            "Workshop",
        ],
    )

    size_distortion.save(suggested_set_dir_path)
    deck_top = Board(
        name="deck_top",
        kingdom_names=[
            "Artisan",
            "Bureaucrat",
            "Council Room",
            "Festival",
            "Harbinger",
            "Laboratory",
            "Moneylender",
            "Sentry",
            "Vassal",
            "Village",
        ],
    )

    deck_top.save(suggested_set_dir_path)


if __name__ == "__main__":
    _main()
