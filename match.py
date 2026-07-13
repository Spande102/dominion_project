"""Automated bot-vs-bot matches: run N silent games and tally the results."""
import io
import random
from contextlib import redirect_stdout

from bots import BOT_TYPES
from cards import load_cards
from game import Game
from utils.kingdom_cards import random_kingdom
from utils.supply_build import add_standard_cards


def run_match(bot_specs, num_games=20, kingdom_cards=None, max_turns=500, seed=None):
    """
    Play num_games games between the given bot types (keys of BOT_TYPES).

    Each game gets fresh bots, a fresh supply, and (unless kingdom_cards is
    given) a fresh random kingdom. Seating rotates between games so no bot
    always goes first. Returns {player_name: wins, ..., 'tie': n}.
    """
    for spec in bot_specs:
        if spec not in BOT_TYPES:
            raise ValueError(f"Unknown bot type: {spec!r}. Choose from: {', '.join(BOT_TYPES)}")
    if seed is not None:
        random.seed(seed)

    _, cards_by_expansion = load_cards()
    names = [f"{spec}-{i + 1}" for i, spec in enumerate(bot_specs)]
    results = {name: 0 for name in names}
    results["tie"] = 0

    for game_index in range(num_games):
        players = [BOT_TYPES[spec](name) for spec, name in zip(bot_specs, names)]
        rotation = game_index % len(players)
        players = players[rotation:] + players[:rotation]

        kingdom = kingdom_cards or random_kingdom(cards_by_expansion)
        supply = {card.name: [card] * 10 for card in kingdom}
        add_standard_cards(supply, num_players=len(players))

        game = Game(players, supply)
        with redirect_stdout(io.StringIO()):
            game.run(max_turns=max_turns)

        winners = game.winners()
        if len(winners) == 1:
            results[winners[0].name] += 1
        else:
            results["tie"] += 1

    return results


def print_results(results, num_games):
    print(f"\n--- Match results ({num_games} games) ---")
    for name, wins in results.items():
        label = "Ties" if name == "tie" else name
        print(f"{label}: {wins} ({wins / num_games:.0%})")
