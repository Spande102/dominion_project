from player import Player


class HumanPlayer(Player):
    """Implements the Player decision interface with terminal prompts."""

    # ------------------------------------------------------------------
    # Generic decisions
    # ------------------------------------------------------------------

    def choose_card_from(self, cards, prompt, optional=True):
        if not cards:
            print("No cards available to choose from.")
            return None

        print("\n" + prompt)
        for i, card in enumerate(cards):
            print(f"{i + 1}: {card.name} - {card.description}")

        cancel_hint = " or type 0 to cancel" if optional else ""
        while True:
            choice = input(f"Choose a card (1-{len(cards)}){cancel_hint}: ").strip()
            if optional and choice == "0":
                print("Action canceled.")
                return None

            try:
                index = int(choice) - 1
                if 0 <= index < len(cards):
                    chosen_card = cards[index]
                    print(f"You selected: {chosen_card.name}")
                    return chosen_card
                else:
                    print("Invalid choice. Please choose a valid card.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def choose_cards_from(self, cards, prompt, min_count=0, max_count=None):
        if not cards:
            return []
        if max_count is None:
            max_count = len(cards)

        print("\n" + prompt)
        for i, card in enumerate(cards):
            print(f"{i + 1}: {card.name}")

        while True:
            hint = f"choose {min_count}" if min_count == max_count else f"choose {min_count}-{max_count}"
            choice = input(f"Enter numbers separated by commas ({hint}"
                           + (", or press Enter for none" if min_count == 0 else "") + "): ").strip()
            if not choice and min_count == 0:
                return []

            chosen_indices = []
            valid = True
            for token in choice.split(","):
                try:
                    index = int(token.strip()) - 1
                except ValueError:
                    print(f"Invalid entry: {token.strip()}")
                    valid = False
                    break
                if not (0 <= index < len(cards)) or index in chosen_indices:
                    print(f"Invalid or duplicate entry: {token.strip()}")
                    valid = False
                    break
                chosen_indices.append(index)

            if valid and min_count <= len(chosen_indices) <= max_count:
                return [cards[i] for i in chosen_indices]
            if valid:
                print(f"Please {hint} card(s).")

    def confirm(self, prompt):
        while True:
            answer = input(f"{prompt} (y/n): ").strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print("Please answer y or n.")

    def choose_options(self, options, prompt, count=1):
        print("\n" + prompt)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        while True:
            hint = "number" if count == 1 else f"{count} different numbers, comma-separated"
            choice = input(f"Choose ({hint}): ").strip()
            try:
                indices = [int(t.strip()) - 1 for t in choice.split(",")]
            except ValueError:
                print("Invalid input. Please enter numbers.")
                continue
            if (len(indices) == count and len(set(indices)) == count
                    and all(0 <= i < len(options) for i in indices)):
                return [options[i] for i in indices]
            print(f"Please choose exactly {count} different option(s).")

    def choose_supply_pile(self, game, prompt, predicate=None, optional=True):
        eligible = {
            name: pile for name, pile in game.supply.items()
            if pile and (predicate is None or predicate(pile[0]))
        }
        if not eligible:
            print("No eligible supply piles.")
            return None

        print("\n" + prompt)
        for name, pile in eligible.items():
            print(f" - {name} (Cost {game.card_cost(pile[0])}): {len(pile)} left")

        skip_hint = " (or press Enter to skip)" if optional else ""
        while True:
            choice = input(f"Card name{skip_hint}: ").strip()
            if optional and choice in ("", "0"):
                return None
            pile_name = game.find_supply_pile(choice)
            if pile_name in eligible:
                return pile_name
            print("Invalid choice. Please type a card name from the list.")

    def order_cards(self, cards, prompt):
        if len(cards) <= 1:
            return list(cards)

        print("\n" + prompt)
        for i, card in enumerate(cards):
            print(f"{i + 1}: {card.name}")

        while True:
            choice = input("Enter numbers in desired order, first = top "
                           "(comma-separated, or press Enter to keep this order): ").strip()
            if not choice:
                return list(cards)

            try:
                indices = [int(t.strip()) - 1 for t in choice.split(",")]
            except ValueError:
                print("Invalid input. Please enter numbers.")
                continue
            if sorted(indices) == list(range(len(cards))):
                return [cards[i] for i in indices]
            print(f"Please enter each number 1-{len(cards)} exactly once.")

    # ------------------------------------------------------------------
    # Turn-flow decisions
    # ------------------------------------------------------------------

    def choose_action_to_play(self, game, action_cards):
        print(f"Actions: {self.actions}")
        print("Action Cards:")
        for i, card in enumerate(action_cards):
            print(f"{i+1}. {card.name} - {card.description}")
        while True:
            choice = input("Play an action Card or Type a command \n (press Enter or type skip to skip): ").strip()
            if game.handle_command(self, choice):
                if not game.running:
                    return None
                continue
            if choice == "" or choice.lower() == "skip":
                return None
            try:
                return action_cards[int(choice) - 1]
            except (ValueError, IndexError):
                print("Invalid selection.")

    def choose_treasure_play(self, game, treasures):
        print(f"Treasures in hand: {[c.name for c in treasures]} (coins={self.coins})")
        while True:
            choice = input("Play Treasures: press Enter or 'all' to play all, a card name for one, 'done' to stop: ").strip()
            if choice == "" or choice.lower() == "all":
                return "all"
            if choice.lower() in ("done", "skip"):
                return None
            card = next((c for c in treasures if c.name.lower() == choice.lower()), None)
            if card:
                return card
            print("No such Treasure in hand.")

    def choose_buy(self, game):
        game.display_supply()
        while True:
            resources = f"coins={self.coins}" + (f", potions={self.potions}" if self.potions else "")
            buy = input(f"Buy a card ({resources}, buys={self.buys}) \n  Press Enter or type skip to skip: ").strip()
            if game.handle_command(self, buy):
                if not game.running:
                    return None
                continue
            if buy == "" or buy.lower() == "skip":
                return None
            pile_name = game.find_supply_pile(buy)
            if pile_name and game.can_buy(self, pile_name):
                return pile_name
            print("You can't buy that (cost, Potion, or a restriction).")
