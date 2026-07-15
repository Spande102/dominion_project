"""
AI opponents implementing the Player decision interface.

The strategy bots follow the classic archetypes described on
dominionstrategy.com / wiki.dominionstrategy.com:

- BigMoneyBot     -- "Money strategies": treasure + Provinces, Duchy-dance endgame.
- SmithyMoneyBot  -- "Big Money + X": money plus a couple of terminal draw cards.
- EngineBot       -- "Engine": trash junk, balance villages vs terminal draw,
                     add payload, green late.
- GardensRushBot  -- "Rush": Workshop/Gardens, fatten the deck with Copper,
                     pile out fast.
- SlogBot         -- "Slog": Duchies plus alt-VP (Duke / Silk Road / Gardens)
                     and deck bulk; wins long games on VP density.
"""
import re

from player import Player


def plus_amount(card, word):
    """Parse '+N Card(s)/Action(s)/...' out of a card's description."""
    match = re.search(rf"\+(\d+) {word}", card.description)
    return int(match.group(1)) if match else 0


def cards_gain(card):
    return plus_amount(card, "Card")


def actions_gain(card):
    return plus_amount(card, "Action")


def junk_first(cards):
    """Sort cards junk-first: Curses, then pure Victory cards, then by cost."""
    def key(card):
        if "Curse" in card.card_type:
            return (0, card.cost)
        if "Victory" in card.card_type and "Action" not in card.card_type:
            return (1, card.cost)
        return (2, card.cost)
    return sorted(cards, key=key)


class Bot(Player):
    """
    Shared decision defaults for all bots; strategy subclasses override
    choose_buy and choose_action_to_play.

    Note: confirm() and choose_cards_from() dispatch on prompt keywords,
    which couples bots to the card prompts. A structured decision context
    would be cleaner -- revisit if the prompts grow.
    """

    keeps_actions = False  # Library: keep drawn Action cards in hand?

    # -- helpers ------------------------------------------------------

    def count_owned(self, name):
        return sum(1 for c in self.all_cards() if c.name == name)

    @staticmethod
    def pile_size(game, name):
        pile = game.supply.get(name)
        return len(pile) if pile else 0

    # -- generic decisions --------------------------------------------

    def choose_card_from(self, cards, prompt, optional=True):
        if optional:
            return None
        return junk_first(cards)[0]

    def choose_cards_from(self, cards, prompt, min_count=0, max_count=None):
        if max_count is None:
            max_count = len(cards)
        if min_count > 0:
            # Forced discards (Militia): give up junk first
            return junk_first(cards)[:min_count]
        p = prompt.lower()
        if "trash" in p:
            junk = [c for c in cards if c.name in ("Curse", "Estate")]
            return junk[:max_count]
        if "discard" in p:
            dead = [c for c in cards if "Curse" in c.card_type
                    or ("Victory" in c.card_type and "Action" not in c.card_type)]
            return dead[:max_count]
        return []

    def confirm(self, prompt):
        p = prompt.lower()
        if "in response to the attack" in p:
            return True                          # always reveal Reactions
        if "revealed card" in p:
            return self.name.lower() not in p    # Spy: keep own card, flip others'
        if "keep it in hand" in p:
            return self.keeps_actions            # Library
        if "trash a copper" in p:
            return True                          # Moneylender
        if p.startswith("play "):
            return True                          # Vassal
        if "entire deck" in p:
            return True                          # Chancellor: cycle faster
        if "gain" in p:
            return "copper" not in p and "curse" not in p  # Thief loot
        return False

    def choose_supply_pile(self, game, prompt, predicate=None, optional=True):
        if optional:
            return None
        eligible = [(name, pile[0]) for name, pile in game.supply.items()
                    if pile and (predicate is None or predicate(pile[0]))]
        if not eligible:
            return None
        # Forced gain: take the most expensive non-Curse option
        non_curse = [e for e in eligible if "Curse" not in e[1].card_type]
        return max(non_curse or eligible, key=lambda e: e[1].cost)[0]

    def order_cards(self, cards, prompt):
        return list(cards)

    def choose_options(self, options, prompt, count=1):
        # Card effects list their generally-best options first
        return list(options[:count])

    # -- turn flow ----------------------------------------------------

    def choose_action_to_play(self, game, action_cards):
        return None

    def choose_treasure_play(self, game, treasures):
        return "all"

    def choose_buy(self, game):
        return None


class BigMoneyBot(Bot):
    """Pure Big Money: Province at 8, Gold at 6, Silver at 3, with the
    classic Duchy/Estate 'dance' as the Province pile empties."""

    def choose_buy(self, game):
        coins = self.coins
        provinces = self.pile_size(game, "Province")
        if coins >= 11 and self.pile_size(game, "Colony"):
            return "Colony"
        if coins >= 8 and provinces:
            return "Province"
        if 0 < provinces <= 4 and coins >= 5 and self.pile_size(game, "Duchy"):
            return "Duchy"
        if 0 < provinces <= 2 and coins >= 2 and self.pile_size(game, "Estate"):
            return "Estate"
        if coins >= 9 and self.pile_size(game, "Platinum"):
            return "Platinum"
        if coins >= 6 and self.pile_size(game, "Gold"):
            return "Gold"
        if coins >= 3 and self.pile_size(game, "Silver"):
            return "Silver"
        return None


class SmithyMoneyBot(BigMoneyBot):
    """Big Money + X: money with up to two terminal draw cards."""

    DRAW_PREFERENCE = ("Witch", "Council Room", "Smithy")

    def choose_action_to_play(self, game, action_cards):
        for name in self.DRAW_PREFERENCE + ("Moat",):
            card = next((c for c in action_cards if c.name == name), None)
            if card:
                return card
        return None

    def choose_buy(self, game):
        owned_draw = sum(self.count_owned(n) for n in self.DRAW_PREFERENCE)
        if owned_draw < 2 and 4 <= self.coins <= 5:
            for name in self.DRAW_PREFERENCE:
                pile = game.supply.get(name)
                if pile and pile[0].cost <= self.coins:
                    return name
        return super().choose_buy(game)


class EngineBot(BigMoneyBot):
    """Engine: one early trasher, keep villages ahead of terminals, stack
    draw, then payload, greening when rich or when Provinces run low.
    Falls back to Big Money when the kingdom has no village-type card."""

    keeps_actions = True

    @staticmethod
    def kingdom_supports_engine(game):
        return any(pile and actions_gain(pile[0]) >= 2 and "Action" in pile[0].card_type
                   for pile in game.supply.values())

    def choose_action_to_play(self, game, action_cards):
        # Non-terminals first (keep the chain alive), then best draw
        def key(card):
            return (0 if actions_gain(card) >= 1 else 1, -cards_gain(card), -card.cost)
        return min(action_cards, key=key)

    def choose_cards_from(self, cards, prompt, min_count=0, max_count=None):
        # Chapel/Sentry: thin the deck early, but stop burning Estate VP
        # once the opening is over
        if min_count == 0 and "trash" in prompt.lower():
            if max_count is None:
                max_count = len(cards)
            junk = [c for c in cards if "Curse" in c.card_type]
            if self.turns_taken <= 10:
                junk += [c for c in cards if c.name == "Estate"]
                if self.count_owned("Silver") + self.count_owned("Gold") >= 2:
                    junk += [c for c in cards if c.name == "Copper"]
            return junk[:max_count]
        return super().choose_cards_from(cards, prompt, min_count, max_count)

    def choose_buy(self, game):
        if not self.kingdom_supports_engine(game):
            return super().choose_buy(game)   # no villages: play Big Money

        coins = self.coins
        provinces = self.pile_size(game, "Province")
        if coins >= 11 and self.pile_size(game, "Colony"):
            return "Colony"
        if coins >= 8 and provinces:
            return "Province"
        if 0 < provinces <= 4 and coins >= 5 and self.pile_size(game, "Duchy"):
            return "Duchy"
        if 0 < provinces <= 2 and coins >= 2 and self.pile_size(game, "Estate"):
            return "Estate"

        owned = self.all_cards()
        terminals = sum(1 for c in owned if "Action" in c.card_type and actions_gain(c) == 0)
        villages = sum(1 for c in owned if actions_gain(c) >= 2)
        draw_owned = sum(1 for c in owned if "Action" in c.card_type and cards_gain(c) >= 2)

        affordable = [pile[0] for name, pile in game.supply.items()
                      if pile and "Action" in pile[0].card_type
                      and pile[0].cost <= coins and pile[0].potion_cost == 0]

        # One early trasher (never with a hand that could buy something big)
        if (self.turns_taken <= 4 and 2 <= coins <= 4
                and self.pile_size(game, "Chapel") and not self.count_owned("Chapel")):
            return "Chapel"
        # Payload before yet more draw once a small draw core exists
        if coins >= 6 and draw_owned >= 2 and self.pile_size(game, "Gold"):
            return "Gold"
        # A little money first: engines still need an economy to get going
        if coins == 3 and self.count_owned("Silver") < 2 and self.pile_size(game, "Silver"):
            return "Silver"
        # Keep villages ahead of terminals
        if terminals > villages:
            village_options = [c for c in affordable if actions_gain(c) >= 2]
            if village_options:
                return max(village_options, key=lambda c: (cards_gain(c), c.cost)).name
        # Draw, cost 4+ only (no Moat spam); prefer non-terminal draw like Laboratory
        if draw_owned < 5:
            draw_options = [c for c in affordable if cards_gain(c) >= 2 and c.cost >= 4
                            and (actions_gain(c) >= 1 or terminals <= villages)]
            if draw_options:
                return max(draw_options,
                           key=lambda c: (actions_gain(c), cards_gain(c), c.cost)).name
        # Payload
        if coins >= 6 and self.pile_size(game, "Gold"):
            return "Gold"
        cantrips = [c for c in affordable if actions_gain(c) >= 1 and c.cost >= 4]
        if cantrips:
            return max(cantrips, key=lambda c: c.cost).name
        if coins >= 3 and self.pile_size(game, "Silver") and self.count_owned("Silver") < 4:
            return "Silver"
        return None


class GardensRushBot(BigMoneyBot):
    """Gardens rush: Workshops gain Gardens, every spare coin buys deck bulk,
    and the game is ended fast on piles. Falls back to Big Money when the
    kingdom has no Gardens."""

    GAIN_PREFERENCE = ("Gardens", "Workshop", "Estate", "Silver")

    def choose_action_to_play(self, game, action_cards):
        return next((c for c in action_cards if c.name == "Workshop"), None)

    def choose_supply_pile(self, game, prompt, predicate=None, optional=True):
        for target in self.GAIN_PREFERENCE:
            name = game.find_supply_pile(target)
            if name and game.supply[name] and (predicate is None or predicate(game.supply[name][0])):
                return name
        return super().choose_supply_pile(game, prompt, predicate, optional)

    def choose_buy(self, game):
        if "Gardens" not in game.supply:
            return super().choose_buy(game)
        coins = self.coins
        if coins >= 8 and self.pile_size(game, "Province"):
            return "Province"
        if coins >= 4 and self.pile_size(game, "Gardens"):
            return "Gardens"
        if coins >= 3 and self.pile_size(game, "Workshop") and self.count_owned("Workshop") < 4:
            return "Workshop"
        if not self.pile_size(game, "Gardens") and coins >= 2 and self.pile_size(game, "Estate"):
            return "Estate"    # pile out
        if coins >= 3 and self.pile_size(game, "Silver") and self.count_owned("Silver") < 2:
            return "Silver"
        if self.pile_size(game, "Copper"):
            return "Copper"    # deck bulk = Gardens VP
        return None


class SlogBot(BigMoneyBot):
    """Slog: Duchies plus alt-VP (Duke / Silk Road / Gardens) and cheap deck
    bulk; expects to out-point Province decks over a long game. Falls back
    to Big Money when the kingdom has no alt-VP card."""

    def choose_buy(self, game):
        alt_vp = [n for n in ("Duke", "Silk Road", "Gardens") if n in game.supply]
        if not alt_vp:
            return super().choose_buy(game)

        coins = self.coins
        if coins >= 8 and self.pile_size(game, "Province"):
            return "Province"
        if coins >= 5:
            duchies, dukes = self.count_owned("Duchy"), self.count_owned("Duke")
            if self.pile_size(game, "Duchy") and ("Duke" not in game.supply or duchies - dukes < 4):
                return "Duchy"
            if self.pile_size(game, "Duke"):
                return "Duke"
            if self.pile_size(game, "Duchy"):
                return "Duchy"
        if coins >= 4:
            for name in ("Silk Road", "Gardens"):
                if self.pile_size(game, name):
                    return name
        # Keep the money density up: the deck must keep hitting 5 for Duchies
        if coins >= 3 and self.pile_size(game, "Silver"):
            return "Silver"
        if coins >= 2 and self.pile_size(game, "Estate") and self.count_owned("Silk Road"):
            return "Estate"    # every Victory card feeds Silk Road
        if self.pile_size(game, "Copper") and self.count_owned("Gardens"):
            return "Copper"    # deck bulk feeds Gardens
        return None


BOT_TYPES = {
    "big_money": BigMoneyBot,
    "smithy_money": SmithyMoneyBot,
    "engine": EngineBot,
    "gardens_rush": GardensRushBot,
    "slog": SlogBot,
}
