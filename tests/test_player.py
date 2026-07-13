from cards.base_set.copper import Copper
from cards.base_set.estate import Estate
from cards.base_set.curse import Curse
from cards.base_set.duchy import Duchy
from cards.base_set.gardens import Gardens
from cards.hinterlands_1st_edition.silk_road import Silk_Road
from cards.intrigue.duke import Duke

from helpers import ScriptedPlayer


def test_draw_reshuffles_discard_when_deck_empty():
    p = ScriptedPlayer("P")
    p.deck = []
    p.discard_pile = [Copper, Copper, Copper]
    p.draw_cards(2)
    assert len(p.hand) == 2
    assert len(p.deck) == 1
    assert p.discard_pile == []


def test_draw_returns_none_when_nothing_left():
    p = ScriptedPlayer("P")
    assert p.draw_cards(1, return_card=True) is None
    assert p.draw_cards(2, return_card=True) == []


def test_top_of_deck_is_end_of_list():
    p = ScriptedPlayer("P")
    p.deck = [Copper]
    p.topdeck(Estate)
    assert p.draw_cards(1, return_card=True) is Estate


def test_cleanup_discards_everything_and_draws_five():
    p = ScriptedPlayer("P")
    p.hand = [Copper, Copper]
    p.in_play = [Estate]
    p.deck = [Copper] * 7
    p.cleanup()
    assert p.hand != []
    assert len(p.hand) == 5
    assert p.in_play == []
    assert len(p.deck) + len(p.discard_pile) == 5


def test_start_turn_resets_turn_state():
    p = ScriptedPlayer("P")
    p.turn_state.merchants_played = 3
    p.actions = 0
    p.start_turn()
    assert p.actions == 1 and p.buys == 1 and p.coins == 0
    assert p.turn_state.merchants_played == 0


def test_victory_point_tally():
    p = ScriptedPlayer("P")
    # 16 Coppers + Gardens + Duke + Duchy + Estate = 20 cards
    p.deck = [Copper] * 16 + [Gardens, Duke, Duchy, Estate]
    p.victory_tokens = 2
    # Gardens 20//10=2, Duke (1 Duchy) 1, Duchy 3, Estate 1, tokens 2
    assert p.get_victory_points() == 9

    p.deck += [Silk_Road]  # 5 Victory cards -> 5//4 = 1
    assert p.get_victory_points() == 10

    p.deck += [Curse]
    assert p.get_victory_points() == 9


def test_victory_points_count_all_zones():
    p = ScriptedPlayer("P")
    p.deck = [Estate]
    p.hand = [Estate]
    p.discard_pile = [Estate]
    p.in_play = [Estate]
    assert p.get_victory_points() == 4
