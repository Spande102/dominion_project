"""Test players implementing the Player decision interface without any I/O."""
from bots import BigMoneyBot as BigMoneyPlayer  # noqa: F401 (re-export for tests)
from game import Game
from player import Player
from utils.supply_build import build_kingdom_supply


class ScriptedPlayer(Player):
    """
    Answers decisions from a queue, in the order they are asked.

    Script entry per decision method:
    - choose_card_from:      card name (str), or None to decline
    - choose_cards_from:     list of card names
    - confirm:               bool
    - choose_supply_pile:    pile name, or None to decline
    - order_cards:           list of card names (first = top), or None to keep order
    - choose_action_to_play: card name, or None to end the phase
    - choose_treasure_play:  'all', a card name, or None to stop
    - choose_buy:            pile name, or None to end the phase

    When the script is empty, decisions fall back to safe defaults
    (decline optional choices, first option for forced ones).
    """

    def __init__(self, name, script=()):
        super().__init__(name)
        self.script = list(script)

    def _pop(self, default=None):
        return self.script.pop(0) if self.script else default

    @staticmethod
    def _find(cards, name):
        return next(c for c in cards if c.name.lower() == name.lower())

    def choose_card_from(self, cards, prompt, optional=True):
        name = self._pop()
        if name is None:
            return None if optional else cards[0]
        return self._find(cards, name)

    def choose_cards_from(self, cards, prompt, min_count=0, max_count=None):
        names = self._pop()
        if names is None:
            return list(cards[:min_count])
        chosen, pool = [], list(cards)
        for n in names:
            card = self._find(pool, n)
            pool.remove(card)
            chosen.append(card)
        return chosen

    def confirm(self, prompt):
        return bool(self._pop(False))

    def choose_options(self, options, prompt, count=1):
        chosen = self._pop(None)
        if chosen is None:
            return list(options[:count])
        return [next(o for o in options if o.lower() == c.lower()) for c in chosen]

    def choose_supply_pile(self, game, prompt, predicate=None, optional=True):
        name = self._pop()
        if name is not None:
            return game.find_supply_pile(name)
        if optional:
            return None
        for key, pile in game.supply.items():
            if pile and (predicate is None or predicate(pile[0])):
                return key
        return None

    def order_cards(self, cards, prompt):
        names = self._pop()
        if names is None:
            return list(cards)
        ordered, pool = [], list(cards)
        for n in names:
            card = self._find(pool, n)
            pool.remove(card)
            ordered.append(card)
        return ordered + pool

    def choose_action_to_play(self, game, action_cards):
        name = self._pop()
        if name is None:
            return None
        return self._find(action_cards, name)

    def choose_treasure_play(self, game, treasures):
        value = self._pop("all")
        if value in ("all", None):
            return value
        return self._find(treasures, value)

    def choose_buy(self, game):
        return self._pop()


def make_game(players, kingdom=(), num_players=2):
    """Build a Game with the given kingdom card piles plus the standard cards."""
    return Game(list(players), build_kingdom_supply(kingdom, num_players=num_players))
