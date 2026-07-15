import random


class Game:
    def __init__(self, players, supply):
        self.players = players
        self.supply = supply
        self.trash_pile = []
        self.running = True
        self.current_player = None
        self.ended_by_resignation = False
        self.resigned_player = None  # optional, used only on resignation

        self.gain_listeners = []           # callables(player, card) — Monkey, Blockade
        self.treasure_play_listeners = []  # callables(player, card) — Corsair
        self.embargo_tokens = {}           # pile name -> token count
        self.trade_route_gained = set()    # Victory piles gained from (Trade Route)

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

    def card_cost(self, card):
        """A card's coin cost this turn: Bridge reduces everything, Quarry
        reduces Actions, Peddler discounts itself per Action in play."""
        player = self.current_player
        if player is None:
            return card.cost
        cost = card.cost - player.turn_state.cost_reduction
        if "Action" in card.card_type:
            cost -= player.turn_state.action_cost_reduction
        if card.name == "Peddler":
            # Official: only during the buy phase; simplified to any time
            # on the owner's turn.
            cost -= 2 * sum(1 for c in player.in_play if "Action" in c.card_type)
        return max(0, cost)

    def costs_at_most(self, max_cost, max_potions=0):
        """Predicate for gains 'costing up to X' (Potion costs must fit too)."""
        return lambda c: self.card_cost(c) <= max_cost and c.potion_cost <= max_potions

    def costs_exactly(self, cost, potions=0):
        return lambda c: self.card_cost(c) == cost and c.potion_cost == potions

    def can_buy(self, player, pile_name):
        pile = self.supply.get(pile_name)
        if not pile:
            return False
        card = pile[0]
        if self.card_cost(card) > player.coins or card.potion_cost > player.potions:
            return False
        if pile_name in player.turn_state.forbidden_buys:
            return False    # Contraband
        if card.name == "Grand Market" and any(c.name == "Copper" for c in player.in_play):
            return False
        return True

    def notify_gain(self, player, card):
        player.gained_this_turn.append(card)
        if "Victory" in card.card_type:
            self.trade_route_gained.add(card.name)
        # Collection: +1 VP per Collection in play when its owner gains an Action
        if "Action" in card.card_type:
            collections = sum(1 for c in player.in_play if c.name == "Collection")
            if collections:
                player.victory_tokens += collections
                print(f"{player.name} gets +{collections} VP (Collection).")
        for listener in list(self.gain_listeners):
            listener(player, card)

    def notify_treasure_play(self, player, card):
        for listener in list(self.treasure_play_listeners):
            listener(player, card)

    def resolve_on_buy(self, player, card):
        # Embargo tokens: gain a Curse per token on the bought pile
        for _ in range(self.embargo_tokens.get(card.name, 0)):
            if player.gain_card(self, self.find_supply_pile("Curse")):
                print(f"{player.name} gains a Curse (Embargo).")
        # Goons: +1 VP per Goons in play for each buy
        goons = sum(1 for c in player.in_play if c.name == "Goons")
        if goons:
            player.victory_tokens += goons
            print(f"{player.name} gets +{goons} VP (Goons).")
        # Hoard: buying a Victory card gains a Gold per Hoard in play
        if "Victory" in card.card_type:
            for c in player.in_play:
                if c.name == "Hoard" and player.gain_card(self, self.find_supply_pile("Gold")):
                    print(f"{player.name} gains a Gold (Hoard).")
        # Talisman: buying a non-Victory card costing up to 4 gains a copy
        if "Victory" not in card.card_type and self.card_cost(card) <= 4 and card.potion_cost == 0:
            for c in player.in_play:
                if c.name == "Talisman" and player.gain_card(self, self.find_supply_pile(card.name)):
                    print(f"{player.name} gains a copy of {card.name} (Talisman).")
        # Mint (on buying Mint itself): trash all Treasures in play
        if card.name == "Mint":
            treasures = [c for c in player.in_play if "Treasure" in c.card_type]
            for t in treasures:
                player.in_play.remove(t)
                self.trash_pile.append(t)
            if treasures:
                print(f"{player.name} trashes {len(treasures)} Treasure(s) in play (Mint).")
        # Royal Seal / Tiara: may put the bought card onto the deck
        if (any(c.name in ("Royal Seal", "Tiara") for c in player.in_play)
                and card in player.discard_pile
                and player.confirm(f"Put the bought {card.name} onto your deck?")):
            player.discard_pile.remove(card)
            player.topdeck(card)

    def player_to_left(self, player):
        return self.players[(self.players.index(player) + 1) % len(self.players)]

    def player_to_right(self, player):
        return self.players[(self.players.index(player) - 1) % len(self.players)]

    def attack_targets(self, attacker):
        """
        Returns the players affected by an Attack, after each other player
        gets the chance to reveal Reaction cards.

        A Reaction card may define:
        - reaction_effect(defender, game) -> bool: runs on reveal; returning
          True blocks the attack (Moat), False just applies the effect
          (Diplomat, Secret Chamber).
        - reaction_available(defender) -> bool: whether it may be revealed now.
        """
        targets = []
        for other in self.other_players(attacker):
            # Lighthouse protects while in play
            if any(c.name == "Lighthouse" for c in other.duration_in_play + other.in_play):
                print(f"{other.name}'s Lighthouse protects them from the attack.")
                continue
            blocked = False
            for reaction in [c for c in other.hand if "Reaction" in c.card_type]:
                effect = getattr(reaction, "reaction_effect", None)
                if effect is None:
                    continue    # not an attack reaction (e.g. Watchtower)
                available = getattr(reaction, "reaction_available", None)
                if available and not available(other):
                    continue
                if not other.confirm(f"{other.name}, reveal {reaction.name} in response to the attack?"):
                    continue
                if effect(other, self):
                    print(f"{other.name} reveals {reaction.name} and is unaffected by the attack.")
                    blocked = True
                    break
                print(f"{other.name} reveals {reaction.name}.")
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
                cost = f"{pile[0].cost}" + ("P" if pile[0].potion_cost else "")
                print(f"{name} (Cost {cost}): {len(pile)} left")
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
            player = self.players[turn % len(self.players)]
            self.current_player = player
            player.outpost_turn = False
            player.take_turn(self)
            # Outpost: one extra turn (with the 3-card hand drawn at cleanup)
            if player.outpost_requested and self.running and not self.is_game_over():
                player.outpost_requested = False
                player.outpost_turn = True
                print(f"\n{player.name} takes an extra turn (Outpost).")
                player.take_turn(self)
                player.outpost_turn = False
            player.outpost_requested = False
            self.current_player = None
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
