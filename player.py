import random


class TurnState:
    """Per-turn state, recreated at the start of every turn."""
    def __init__(self):
        self.merchants_played = 0
        self.silvers_played = 0


class Player:
    """
    Game mechanics live here; decisions do not.

    Every choice a player makes goes through one of the decision methods below,
    which subclasses implement: HumanPlayer (human_player.py) prompts on the
    terminal, bots and test players answer programmatically.
    """

    def __init__(self, name):
        self.name = name
        self.deck = []
        self.hand = []
        self.discard_pile = []
        self.in_play = []

        self.actions = 1
        self.buys = 1
        self.coins = 0
        self.victory_tokens = 0
        self.turns_taken = 0

        self.turn_state = TurnState()

    # ------------------------------------------------------------------
    # Decision interface -- implemented by subclasses
    # ------------------------------------------------------------------

    def choose_card_from(self, cards, prompt, optional=True):
        """Choose one card from a list. Returns a card, or None if declined
        (only allowed when optional=True)."""
        raise NotImplementedError

    def choose_cards_from(self, cards, prompt, min_count=0, max_count=None):
        """Choose between min_count and max_count cards from a list.
        Returns a list of cards."""
        raise NotImplementedError

    def confirm(self, prompt):
        """A yes/no decision. Returns True or False."""
        raise NotImplementedError

    def choose_supply_pile(self, game, prompt, predicate=None, optional=True):
        """Choose a non-empty supply pile whose top card satisfies predicate.
        Returns the pile's key in game.supply, or None if declined."""
        raise NotImplementedError

    def order_cards(self, cards, prompt):
        """Put a list of cards in a chosen order. Returns the reordered list
        (first element = top of deck)."""
        raise NotImplementedError

    def choose_action_to_play(self, game, action_cards):
        """Pick an Action card from action_cards to play, or None to end
        the action phase."""
        raise NotImplementedError

    def choose_treasure_play(self, game, treasures):
        """Return 'all' to play every Treasure in hand, a specific Treasure
        card to play just that one, or None to stop playing Treasures."""
        raise NotImplementedError

    def choose_buy(self, game):
        """Return the supply key of an affordable pile to buy from, or None
        to end the buy phase."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Card movement
    # Convention: the TOP of the deck is the END of self.deck
    # (draw_cards pops from the end, topdeck appends).
    # ------------------------------------------------------------------

    def draw_cards(self, n=1, return_card=False):
        drawn_cards = []
        for _ in range(n):
            if not self.deck:
                self.deck = self.discard_pile
                self.discard_pile = []
                random.shuffle(self.deck)
            if self.deck:
                card = self.deck.pop()
                if return_card:
                    drawn_cards.append(card)
                else:
                    self.hand.append(card)
        if return_card:
            if n == 1:
                return drawn_cards[0] if drawn_cards else None
            return drawn_cards

    def topdeck(self, card):
        self.deck.append(card)

    def gain_card(self, game, pile_name, destination='discard'):
        """Gain the top card of a supply pile to 'discard', 'hand', or 'deck'
        (topdeck). Returns the card, or None if the pile is missing/empty."""
        if not pile_name or not game.supply.get(pile_name):
            return None
        card = game.supply[pile_name].pop()
        if destination == 'hand':
            self.hand.append(card)
        elif destination == 'deck':
            self.topdeck(card)
        else:
            self.discard_pile.append(card)
        return card

    def trash_card(self, card_name, game, zone='hand'):
        """
        Trashes a card from the specified zone ('hand', 'in_play', 'discard', 'deck')
        and moves it to the game trash pile.
        """
        zones = {
            'hand': self.hand,
            'in_play': self.in_play,
            'discard': self.discard_pile,
            'deck': self.deck,
        }
        zone_list = zones.get(zone)
        if zone_list is None:
            print(f"Unknown zone: {zone}")
            return None

        card = next((c for c in zone_list if c.name.lower() == card_name.lower()), None)
        if not card:
            print(f"{card_name} not found in your {zone}.")
            return None

        zone_list.remove(card)
        game.trash_pile.append(card)
        print(f"{self.name} trashes {card.name} from {zone}.")
        return card

    # ------------------------------------------------------------------
    # Turn structure
    # ------------------------------------------------------------------

    def start_turn(self):
        self.actions = 1
        self.buys = 1
        self.coins = 0
        self.turns_taken += 1
        self.turn_state = TurnState()

    def take_turn(self, game):
        self.start_turn()
        print(f"\n-- {self.name}'s Turn --")
        print(f"Hand: {[card.name for card in self.hand]}")

        # --- Action Phase ---
        print("\n-- Action Phase --")
        while self.actions > 0:
            action_cards = [card for card in self.hand if "Action" in card.card_type]
            if not action_cards:
                break
            card = self.choose_action_to_play(game, action_cards)
            if not game.running:
                return
            if card is None:
                break
            self.play_card(card, game)
            self.actions -= 1

        # --- Buy Phase ---
        print("\n-- Buy Phase --")
        self.play_treasures(game)
        print(f"Coins: {self.coins}")

        while self.buys > 0:
            pile_name = self.choose_buy(game)
            if not game.running:
                return
            if pile_name is None:
                break
            pile = game.supply.get(pile_name)
            if pile and pile[0].cost <= self.coins:
                gained_card = pile.pop()
                self.discard_pile.append(gained_card)
                self.coins -= gained_card.cost
                self.buys -= 1
                print(f"{self.name} bought {gained_card.name}")
            else:
                print(f"Invalid buy choice: {pile_name}")
                break  # guards against a misbehaving bot looping forever

        # --- Cleanup Phase ---
        self.cleanup()

    def play_card(self, card, game):
        self.hand.remove(card)
        self.in_play.append(card)
        if card.effect:
            card.effect(self, game)

    def play_treasures(self, game):
        while True:
            treasures = [c for c in self.hand if "Treasure" in c.card_type]
            if not treasures:
                break
            choice = self.choose_treasure_play(game, treasures)
            if choice == "all":
                for card in treasures:
                    self.play_treasure(card, game)
                break
            if choice is None:
                break
            if choice in treasures:
                self.play_treasure(choice, game)
            else:
                print("No such Treasure in hand.")

    def play_treasure(self, card, game):
        self.hand.remove(card)
        self.in_play.append(card)
        value = card.effect(self, game) if card.effect else 0
        self.coins += value or 0
        # Merchant: the first time you play a Silver this turn, +1 Coin per Merchant played
        if card.name == "Silver":
            self.turn_state.silvers_played += 1
            if self.turn_state.silvers_played == 1 and self.turn_state.merchants_played > 0:
                self.coins += self.turn_state.merchants_played
                print(f"Merchant bonus: +{self.turn_state.merchants_played} Coin.")
        print(f"{self.name} plays {card.name} (coins={self.coins}).")

    def cleanup(self):
        print(f"{self.name}'s turn has ended.")
        self.discard_pile += self.hand + self.in_play
        self.hand = []
        self.in_play = []
        self.draw_cards(5)

    def all_cards(self):
        return self.deck + self.hand + self.discard_pile + self.in_play

    def get_victory_points(self):
        return (
            sum(card.get_victory_points(self) if hasattr(card, "get_victory_points") else 0
                for card in self.all_cards())
            + self.victory_tokens
        )
