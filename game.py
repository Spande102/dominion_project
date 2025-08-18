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
            player.draw_cards(5)

    def initial_deck(self):
        from cards.base_set.copper import Copper
        from cards.base_set.estate import Estate
        return [Copper]*7 + [Estate]*3

    def display_supply(self):
        print("\nSupply:")
        for name, pile in self.supply.items():
            if pile:
                print(f"{name} (Cost {pile[0].cost}): {len(pile)} left")

    def topdeck_gained_card(self, player, card_name):
        """
        Moves a specified card from the supply to the top of the given player's deck.

        :param player: The player gaining the card.
        :param card_name: The name of the card to be gained.
        :return: The card object gained, or None if the gain is unsuccessful.
        """
        if card_name in self.supply and self.supply[card_name]:  # Check if the card is in supply and available
            card = self.supply[card_name].pop()  # Remove the card from the supply
            player.deck.insert(0, card)  # Place it on top of the player's deck
            print(f"{player.name} gains a {card_name} to the top of their deck.")
            return card
        else:
            print(f"{card_name} is not available in the supply.")
            return None

    def trash_card(self, card_name, game, zone='hand'):
        """
        Trashes a card from the specified zone ('hand', 'in_play', 'discard', 'deck')
        and moves it to the game trash pile.
        """
        zone_list = getattr(self, zone, [])
        card = next((c for c in zone_list if c.name.lower() == card_name.lower()), None)

        if not card:
            print(f"{card_name} not found in your {zone}.")
            return None

        zone_list.remove(card)
        game.trash_pile.append(card)
        print(f"{self.name} trashes {card.name} from {zone}.")
        return card


    def run(self):
        turn = 0
        while not self.is_game_over() and self.running:
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
        if not self.supply.get("Province") or len(self.supply["Province"]) == 0:
            return True
        empty_piles = sum(1 for pile in self.supply.values() if not pile)
        return empty_piles >= 3

    def tally_scores(self):
        print("\n--- Final Scores ---")
        scores = {}
        max_score = float('-inf')
        for player in self.players:
            vp = player.get_victory_points()
            scores[player.name] = vp
            max_score = max(max_score, vp)
            print(f"{player.name}: {vp} points")
            print(
                f"  Cards: {[card.name for card in player.deck + player.hand + player.discard_pile + player.in_play]}")

        winners = [name for name, score in scores.items() if score == max_score]
        if len(winners) == 1:
            print(f"\n{winners[0]} wins!")
        else:
            print(f"\nIt's a tie between: {', '.join(winners)}")

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
            game.display_supply()
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
                if card_name in self.supply and self.supply[card_name]:
                    card = self.supply[card_name][0]  # Get one copy from supply
                else:
                    card = next((c for c in player.hand if c.name.lower() == card_name.lower()), None)
            else:
                print("Usage: disp [card name]")
            return True

        elif cmd == "Help":
            print("Available commands: resign, hand, actions, buys, coins, disp [card], help")
            return True

        return False  # Not a recognized command
