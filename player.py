import random


class TurnState:
    """Per-turn state, recreated at the start of every turn."""
    def __init__(self):
        self.merchants_played = 0
        self.silvers_played = 0
        self.actions_played = 0            # Conspirator
        self.cost_reduction = 0            # Bridge: all cards cost this much less
        self.action_cost_reduction = 0     # Quarry: Actions cost this much less
        self.copper_bonus = 0              # Coppersmith: Copper produces +1 per play
        self.bought_victory = False        # Treasury
        self.forbidden_buys = set()        # Contraband
        self.war_chest_named = set()       # War Chest


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
        self.potions = 0
        self.victory_tokens = 0
        self.turns_taken = 0

        # Durations (Seaside): cards staying in play + queued next-turn effects
        self.duration_in_play = []
        self.next_turn_effects = []
        # Set-aside zones and mats; all count toward scoring
        self.set_aside = []          # Haven, Blockade, ...
        self.island_mat = []
        self.native_village_mat = []
        self.pirate_ship_tokens = 0
        # Outpost
        self.outpost_requested = False
        self.outpost_turn = False
        # Gains tracked for Smugglers
        self.gained_this_turn = []
        self.gained_last_turn = []

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

    def choose_options(self, options, prompt, count=1):
        """Choose `count` different options from a list of strings.
        Returns a list of the chosen option strings."""
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
        zone = {'hand': self.hand, 'deck': self.deck}.get(destination, self.discard_pile)
        zone.append(card)
        game.notify_gain(self, card)

        # Watchtower reaction: trash or topdeck the gained card
        if (any(c.name == "Watchtower" for c in self.hand) and card in zone
                and self.confirm(f"Reveal Watchtower in reaction to gaining {card.name}?")):
            choice = self.choose_options(
                ["Put it onto your deck", "Trash it"], "Watchtower:")[0]
            zone.remove(card)
            if choice == "Trash it":
                game.trash_pile.append(card)
                print(f"{self.name} trashes the gained {card.name}.")
            else:
                self.topdeck(card)
                print(f"{self.name} topdecks the gained {card.name}.")
        return card

    def add_duration(self, card_name, effect=None):
        """Keep a just-played card in play until the start of next turn;
        optionally queue effect(player, game) to run then."""
        card = next((c for c in self.in_play if c.name == card_name), None)
        if card:
            self.in_play.remove(card)
            self.duration_in_play.append(card)
        if effect:
            self.next_turn_effects.append(effect)

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
        self.potions = 0
        self.turns_taken += 1
        self.gained_last_turn = self.gained_this_turn
        self.gained_this_turn = []
        self.turn_state = TurnState()

    def take_turn(self, game):
        self.start_turn()
        print(f"\n-- {self.name}'s Turn --")

        # Resolve Duration effects queued last turn; the Duration cards then
        # return to play and get discarded at this turn's cleanup.
        if self.next_turn_effects or self.duration_in_play:
            effects = self.next_turn_effects
            self.next_turn_effects = []
            for effect in effects:
                effect(self, game)
            self.in_play.extend(self.duration_in_play)
            self.duration_in_play = []

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
        print(f"Coins: {self.coins}" + (f", Potions: {self.potions}" if self.potions else ""))

        while self.buys > 0:
            pile_name = self.choose_buy(game)
            if not game.running:
                return
            if pile_name is None:
                break
            if game.can_buy(self, pile_name):
                self.buy_card(game, pile_name)
            else:
                print(f"Invalid buy choice: {pile_name}")
                break  # guards against a misbehaving bot looping forever

        # --- Cleanup Phase ---
        self.cleanup(game)

    def buy_card(self, game, pile_name):
        card = game.supply[pile_name][0]
        self.coins -= game.card_cost(card)
        self.potions -= card.potion_cost
        self.buys -= 1
        gained = self.gain_card(game, pile_name)
        print(f"{self.name} bought {gained.name}")
        if "Victory" in gained.card_type:
            self.turn_state.bought_victory = True
        game.resolve_on_buy(self, gained)
        return gained

    def play_card(self, card, game):
        self.hand.remove(card)
        self.in_play.append(card)
        if "Action" in card.card_type:
            self.turn_state.actions_played += 1
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
        # Coppersmith: each Copper produces an extra coin per Coppersmith played
        if card.name == "Copper":
            self.coins += self.turn_state.copper_bonus
        # Merchant: the first time you play a Silver this turn, +1 Coin per Merchant played
        if card.name == "Silver":
            self.turn_state.silvers_played += 1
            if self.turn_state.silvers_played == 1 and self.turn_state.merchants_played > 0:
                self.coins += self.turn_state.merchants_played
                print(f"Merchant bonus: +{self.turn_state.merchants_played} Coin.")
        print(f"{self.name} plays {card.name} (coins={self.coins}).")
        game.notify_treasure_play(self, card)

    def cleanup(self, game=None):
        print(f"{self.name}'s turn has ended.")
        if game:
            self._cleanup_topdeck_offers(game)
        self.discard_pile += self.hand + self.in_play
        self.hand = []
        self.in_play = []
        self.draw_cards(3 if self.outpost_requested else 5)

    def _cleanup_topdeck_offers(self, game):
        """Treasury / Alchemist / Herbalist may go back on the deck at cleanup."""
        for card in list(self.in_play):
            if (card.name == "Treasury" and not self.turn_state.bought_victory
                    and self.confirm("Put Treasury on top of your deck?")):
                self.in_play.remove(card)
                self.topdeck(card)
            elif (card.name == "Alchemist"
                    and any(c.name == "Potion" for c in self.in_play)
                    and self.confirm("Put Alchemist on top of your deck?")):
                self.in_play.remove(card)
                self.topdeck(card)
            elif card.name == "Herbalist":
                treasures = [c for c in self.in_play if "Treasure" in c.card_type]
                if treasures and self.confirm("Herbalist: put a Treasure from play onto your deck?"):
                    chosen = self.choose_card_from(treasures, "Choose a Treasure to topdeck:",
                                                   optional=False)
                    self.in_play.remove(chosen)
                    self.topdeck(chosen)

    def all_cards(self):
        return (self.deck + self.hand + self.discard_pile + self.in_play
                + self.duration_in_play + self.set_aside
                + self.island_mat + self.native_village_mat)

    def get_victory_points(self):
        return (
            sum(card.get_victory_points(self) if hasattr(card, "get_victory_points") else 0
                for card in self.all_cards())
            + self.victory_tokens
        )
