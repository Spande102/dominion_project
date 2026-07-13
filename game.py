import random


class Game:
    def __init__(self, players, supply):
        self.players = players
        self.supply = supply
        self.trash_pile = []
        self.running = True
        self.ended_by_resignation = False
        self.resigned_player = None  # optional, used only on resignation

        for player in self.players:
            player.deck = self.initial_deck()
            random.shuffle(player.deck)
            player.draw_cards(5)

    def initial_deck(self):
        from cards.base_set.copper import Copper
        from cards.base_set.estate import Estate
        return [Copper]*7 + [Estate]*3

    def other_players(self, player):
        return [p for p in self.players if p is not player]

    def attack_targets(self, attacker):
        """
        Returns the players affected by an Attack, after each other player
        gets the chance to reveal a Reaction card (e.g. Moat) to block it.
        """
        targets = []
        for other in self.other_players(attacker):
            blocked = False
            for reaction in [c for c in other.hand if "Reaction" in c.card_type]:
                if other.confirm(f"{other.name}, reveal {reaction.name} to block the attack?"):
                    print(f"{other.name} reveals {reaction.name} and is unaffected by the attack.")
                    blocked = True
                    break
            if not blocked:
                targets.append(other)
        return targets

    def find_supply_pile(self, name):
        """Case-insensitive lookup of a supply pile. Returns the pile's key or None."""
        if not name:
            return None
        for key in self.supply:
            if key.lower() == name.strip().lower():
                return key
        return None

    def display_supply(self):
        print("\nSupply:")
        for name, pile in self.supply.items():
            if pile:
                print(f"{name} (Cost {pile[0].cost}): {len(pile)} left")
            else:
                print(f"{name}: empty")

    def topdeck_gained_card(self, player, card_name):
        """
        Moves a specified card from the supply to the top of the given player's deck.

        :param player: The player gaining the card.
        :param card_name: The name of the card to be gained.
        :return: The card object gained, or None if the gain is unsuccessful.
        """
        pile_name = self.find_supply_pile(card_name)
        card = player.gain_card(self, pile_name, destination='deck')
        if card:
            print(f"{player.name} gains a {card.name} to the top of their deck.")
        else:
            print(f"{card_name} is not available in the supply.")
        return card

    def run(self, max_turns=None):
        turn = 0
        while not self.is_game_over() and self.running:
            if max_turns is not None and turn >= max_turns:
                print("Turn limit reached; ending the game.")
                break
            current_player = self.players[turn % len(self.players)]
            current_player.take_turn(self)
            turn += 1

        if self.ended_by_resignation:
            print(f"{self.resigned_player.name} resigned. Game has concluded.")
            self.tally_scores()
        else:
            print("Game over! Tallying scores...")
            self.tally_scores()

    def is_game_over(self):
        if "Province" in self.supply and not self.supply["Province"]:
            return True
        if "Colony" in self.supply and not self.supply["Colony"]:
            return True
        empty_piles = sum(1 for pile in self.supply.values() if not pile)
        return empty_piles >= 3

    def winners(self):
        """Players with the highest victory point total (more than one on a tie)."""
        scores = {player: player.get_victory_points() for player in self.players}
        best = max(scores.values())
        return [player for player, vp in scores.items() if vp == best]

    def tally_scores(self):
        print("\n--- Final Scores ---")
        for player in self.players:
            print(f"{player.name}: {player.get_victory_points()} points")
            print(f"  Cards: {[card.name for card in player.all_cards()]}")

        winners = self.winners()
        if len(winners) == 1:
            print(f"\n{winners[0].name} wins!")
        else:
            print(f"\nIt's a tie between: {', '.join(p.name for p in winners)}")

    def handle_command(self, player, command):
        tokens = command.strip().split()
        if not tokens:
            return False

        cmd = tokens[0].capitalize()
        args = tokens[1:]

        if cmd == "Resign":
            print(f"{player.name} has resigned. Game over.")
            self.ended_by_resignation = True
            self.resigned_player = player
            self.running = False
            return True

        elif cmd == "Hand":
            print(f"{player.name}'s hand: {[card.name for card in player.hand]}")
            return True

        elif cmd == "Supply":
            self.display_supply()
            return True

        elif cmd == "Actions":
            print(f"{player.name} has {player.actions} action(s) remaining.")
            return True

        elif cmd == "Buys":
            print(f"{player.name} has {player.buys} buy(s) remaining.")
            return True

        elif cmd == "Coins":
            print(f"{player.name} has {player.coins} coin(s).")
            return True

        elif cmd in ("Disp", "Display"):
            if args:
                card_name = " ".join(args)
                card = None
                pile_name = self.find_supply_pile(card_name)
                if pile_name and self.supply[pile_name]:
                    card = self.supply[pile_name][0]
                else:
                    card = next((c for c in player.hand if c.name.lower() == card_name.lower()), None)
                if card:
                    print(f"{card.name} (Cost {card.cost}) [{', '.join(card.card_type)}]")
                    print(f"  {card.description}")
                else:
                    print(f"Card '{card_name}' not found in supply or hand.")
            else:
                print("Usage: disp [card name]")
            return True

        elif cmd == "Help":
            print("Available commands: resign, hand, supply, actions, buys, coins, disp [card], help")
            return True

        return False  # Not a recognized command
