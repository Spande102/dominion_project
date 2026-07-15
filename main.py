import argparse
import random

from bots import BOT_TYPES
from human_player import HumanPlayer
from game import Game
from cards import load_cards  # Updated __init__.py now returns cards
from utils.supply_build import build_kingdom_supply
from utils.kingdom_cards import choose_kingdom_cards


def create_player(index):
    """Ask whether seat index is a human or a bot, and build the player."""
    while True:
        kind = input(f"Player {index + 1}: human or bot? (h/b): ").strip().lower()
        if kind in ("h", "human"):
            return HumanPlayer(input(f"Enter name for Player {index + 1}: "))
        if kind in ("b", "bot"):
            bot_names = list(BOT_TYPES)
            for j, bot_name in enumerate(bot_names, 1):
                print(f"{j}. {bot_name}")
            pick = input("Choose bot type (number): ").strip()
            try:
                bot_name = bot_names[int(pick) - 1]
            except (ValueError, IndexError):
                print("Invalid choice.")
                continue
            return BOT_TYPES[bot_name](f"{bot_name}-{index + 1}")
        print("Please enter h or b.")


def interactive_game():
    # Load all available cards
    all_cards, cards_by_expansion = load_cards()

    # Prompt for player count
    while True:
        try:
            num_players = int(input("How many players? (2-4): "))
            if 2 <= num_players <= 4:
                break
            else:
                print("Dominion is best with 2-4 players.")
        except ValueError:
            print("Enter a valid number.")

    players = [create_player(i) for i in range(num_players)]

    # Choose 10 Kingdom cards (either manually or randomly)
    selected_kingdom_cards = choose_kingdom_cards(cards_by_expansion)
    if len(selected_kingdom_cards) != 10:
        print("Invalid kingdom card setup. Exiting.")
        return

    # Per Prosperity rules, Platinum/Colony are used with a probability equal to the
    # proportion of Prosperity cards in the kingdom.
    prosperity_count = sum(1 for card in selected_kingdom_cards
                           if card.expansion.startswith("prosperity"))
    include_colony = random.random() < prosperity_count / 10
    if include_colony:
        print("\nThis game uses Platinum and Colony!")

    supply = build_kingdom_supply(selected_kingdom_cards, num_players,
                                  include_colony=include_colony)

    print("\nFinal Supply:")
    for name in supply:
        print(f"- {name} ({len(supply[name])} copies)")

    # Start the game
    game = Game(players, supply)
    game.run()


def main():
    parser = argparse.ArgumentParser(description="Text-based Dominion")
    parser.add_argument("--match", type=int, metavar="N",
                        help="run N automated bot-vs-bot games and report win rates")
    parser.add_argument("--bots", default="big_money,smithy_money", metavar="TYPES",
                        help="comma-separated bot types for --match "
                             f"(available: {', '.join(BOT_TYPES)})")
    args = parser.parse_args()

    if args.match:
        from match import run_match, print_results
        specs = [s.strip() for s in args.bots.split(",") if s.strip()]
        if len(specs) < 2:
            parser.error("--bots needs at least two comma-separated bot types")
        results = run_match(specs, num_games=args.match)
        print_results(results, args.match)
    else:
        interactive_game()


if __name__ == "__main__":
    main()
