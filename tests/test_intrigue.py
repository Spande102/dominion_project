"""Effect tests for Intrigue (2nd edition + removed 1st edition cards)."""
import random

from cards.base_set.copper import Copper
from cards.base_set.silver import Silver
from cards.base_set.gold import Gold
from cards.base_set.estate import Estate
from cards.base_set.village import Village
from cards.base_set.smithy import Smithy
from cards.base_set.moat import Moat

from helpers import ScriptedPlayer, make_game


def two_player_game(a_script=(), b_script=(), kingdom=(Village, Smithy)):
    a = ScriptedPlayer("A", a_script)
    b = ScriptedPlayer("B", b_script)
    game = make_game([a, b], kingdom=kingdom)
    return game, a, b


# ------------------------------------------------------------- cost 2-3

def test_courtyard_draws_three_topdecks_one():
    from cards.intrigue.courtyard import courtyard_effect
    game, a, _ = two_player_game(a_script=["Estate"])
    a.hand = [Estate]
    a.deck = [Copper] * 4

    courtyard_effect(a, game)

    assert len(a.hand) == 3
    assert a.deck[-1] is Estate


def test_lurker_trash_from_supply_then_gain_from_trash():
    from cards.intrigue.lurker import Lurker, lurker_effect
    game, a, b = two_player_game(
        a_script=[["Trash an Action card from the Supply"], "Smithy"],
        b_script=[["Gain an Action card from the trash"], "Smithy"])
    smithy_count = len(game.supply["Smithy"])

    lurker_effect(a, game)
    assert a.actions == 2
    assert len(game.supply["Smithy"]) == smithy_count - 1
    assert any(c.name == "Smithy" for c in game.trash_pile)

    lurker_effect(b, game)
    assert any(c.name == "Smithy" for c in b.discard_pile)
    assert not any(c.name == "Smithy" for c in game.trash_pile)


def test_pawn_choices():
    from cards.intrigue.pawn import pawn_effect
    game, a, _ = two_player_game(a_script=[["+1 Buy", "+1 Coin"]])
    a.hand = []

    pawn_effect(a, game)

    assert a.buys == 2 and a.coins == 1 and a.hand == []


def test_masquerade_passes_left_and_trashes():
    from cards.intrigue.masquerade import masquerade_effect
    game, a, b = two_player_game(a_script=["Gold", "Estate"], b_script=["Estate"])
    a.hand = [Gold, Estate]
    a.deck = [Copper, Copper]
    b.hand = [Estate, Silver]

    masquerade_effect(a, game)

    # A drew 2 Coppers, passed Gold to B, received B's Estate, trashed an Estate
    assert Gold in b.hand
    assert any(c.name == "Estate" for c in game.trash_pile)
    assert not any(c.name == "Gold" for c in a.hand)


def test_shanty_town_draws_only_without_actions():
    from cards.intrigue.shanty_town import shanty_town_effect
    game, a, _ = two_player_game()
    a.hand = [Copper]
    a.deck = [Copper] * 3
    shanty_town_effect(a, game)
    assert a.actions == 3 and len(a.hand) == 3

    a2 = ScriptedPlayer("A2")
    a2.hand = [Smithy]
    a2.deck = [Copper] * 3
    shanty_town_effect(a2, game)
    assert len(a2.hand) == 1   # no draw with an Action in hand


def test_steward_trash_choice():
    from cards.intrigue.steward import steward_effect
    game, a, _ = two_player_game(
        a_script=[["Trash 2 cards from your hand"], ["Estate", "Estate"]])
    a.hand = [Estate, Estate, Copper]

    steward_effect(a, game)

    assert [c.name for c in a.hand] == ["Copper"]
    assert len(game.trash_pile) == 2


def test_swindler_trashes_top_and_gives_same_cost():
    from cards.intrigue.swindler import swindler_effect
    game, a, b = two_player_game(a_script=["Curse"])
    b.hand = []
    b.deck = [Copper]   # Copper costs 0 -> attacker picks Curse (also 0)
    b.discard_pile = []

    swindler_effect(a, game)

    assert a.coins == 2
    assert any(c.name == "Copper" for c in game.trash_pile)
    assert any(c.name == "Curse" for c in b.discard_pile)


def test_wishing_well_correct_and_wrong_wish():
    from cards.intrigue.wishing_well import wishing_well_effect
    game, a, _ = two_player_game(a_script=["Silver"])
    a.hand = []
    a.deck = [Silver, Copper]   # draws Copper, reveals Silver

    wishing_well_effect(a, game)
    assert any(c.name == "Silver" for c in a.hand)

    a2 = ScriptedPlayer("A2", ["Gold"])
    a2.hand = []
    a2.deck = [Silver, Copper]
    wishing_well_effect(a2, game)
    assert not any(c.name == "Silver" for c in a2.hand)
    assert a2.deck[-1] is Silver   # put back


# ------------------------------------------------------------- cost 4

def test_baron_discard_estate_or_gain_one():
    from cards.intrigue.baron import baron_effect
    game, a, b = two_player_game(a_script=[True], b_script=[False])
    a.hand = [Estate]
    baron_effect(a, game)
    assert a.coins == 4 and a.buys == 2 and Estate in a.discard_pile

    b.hand = []
    b.discard_pile = []
    baron_effect(b, game)
    assert any(c.name == "Estate" for c in b.discard_pile)


def test_bridge_reduces_costs_for_buying_and_gaining():
    from cards.intrigue.bridge import bridge_effect
    game, a, _ = two_player_game()
    game.current_player = a
    a.start_turn()
    bridge_effect(a, game)

    assert a.coins == 1 and a.buys == 2
    silver = game.supply["Silver"][0]
    assert game.card_cost(silver) == 2   # 3 - 1

    # Buying uses the reduced cost
    a.coins = 2
    a.script = ["Silver"]
    a.buys = 1
    pile = a.choose_buy(game)
    assert pile == "Silver"
    game.current_player = None


def test_conspirator_needs_three_actions():
    from cards.intrigue.conspirator import Conspirator
    game, a, _ = two_player_game()
    a.start_turn()
    a.actions = 5
    a.deck = [Copper] * 3
    a.hand = [Village, Village, Conspirator]

    a.play_card(a.hand[0], game)
    a.play_card(a.hand[0], game)
    hand_before = len(a.hand)
    a.play_card(next(c for c in a.hand if c.name == "Conspirator"), game)

    assert a.coins == 2
    assert len(a.hand) == hand_before   # -1 played, +1 drawn from bonus


def test_diplomat_effect_and_reaction():
    from cards.intrigue.diplomat import Diplomat, diplomat_effect
    from cards.base_set.militia import militia_effect
    game, a, b = two_player_game(b_script=[True, ["Copper", "Copper", "Copper"], ["Copper"]])
    a.hand = []
    a.deck = [Copper] * 4
    diplomat_effect(a, game)
    assert len(a.hand) == 2 and a.actions == 3   # 2 <= 5 -> +2 Actions

    # Reaction: B has Diplomat + 4 Coppers (5 cards); A plays Militia
    b.hand = [Diplomat] + [Copper] * 4
    b.deck = [Copper] * 4
    b.discard_pile = []
    militia_effect(a, game)
    # B revealed Diplomat: drew 2, discarded 3 -> 4 cards, then militia: down to 3
    assert len(b.hand) == 3
    assert len(b.discard_pile) == 4


def test_ironworks_bonuses_by_type():
    from cards.intrigue.ironworks import ironworks_effect
    game, a, _ = two_player_game(a_script=["Silver", "Estate"])
    a.hand = []
    a.deck = [Copper]

    ironworks_effect(a, game)   # gains Silver -> +1 Coin
    assert a.coins == 1

    ironworks_effect(a, game)   # gains Estate -> +1 Card
    assert len(a.hand) == 1


def test_mill_vp_and_discard_for_coins():
    from cards.intrigue.mill import Mill, mill_effect
    game, a, _ = two_player_game(a_script=[True, ["Copper", "Copper"]])
    a.hand = [Copper, Copper]
    a.deck = [Silver]

    mill_effect(a, game)

    assert a.coins == 2
    assert a.actions == 2
    p = ScriptedPlayer("VP")
    p.deck = [Mill, Mill]
    assert p.get_victory_points() == 2


def test_mining_village_trashes_itself_once():
    from cards.intrigue.mining_village import Mining_Village, mining_village_effect
    game, a, _ = two_player_game(a_script=[True])
    a.in_play = [Mining_Village]
    a.deck = [Copper]

    mining_village_effect(a, game)

    assert a.coins == 2
    assert Mining_Village not in a.in_play
    assert Mining_Village in game.trash_pile


def test_secret_passage_top_or_bottom():
    from cards.intrigue.secret_passage import secret_passage_effect
    game, a, _ = two_player_game(a_script=["Estate", False])  # to the bottom
    a.hand = [Estate]
    a.deck = [Copper, Copper]

    secret_passage_effect(a, game)

    assert a.deck[0] is Estate
    assert a.actions == 2


# ------------------------------------------------------------- cost 5-6

def test_courtier_choices_scale_with_types():
    from cards.intrigue.courtier import courtier_effect
    game, a, _ = two_player_game(
        a_script=["Nobles", ["+3 Coins", "Gain a Gold"]])
    from cards.intrigue.nobles import Nobles
    a.hand = [Nobles, Copper]
    a.discard_pile = []

    courtier_effect(a, game)   # Nobles has 2 types -> 2 choices

    assert a.coins == 3
    assert any(c.name == "Gold" for c in a.discard_pile)


def test_minion_attack_mode():
    from cards.intrigue.minion import minion_effect
    game, a, b = two_player_game(
        a_script=[["Discard your hand, +4 Cards, and each other player with 5+ cards discards and draws 4"]])
    a.hand = [Copper, Copper]
    a.deck = [Copper] * 5
    b.hand = [Copper] * 5
    b.deck = [Silver] * 5
    b.discard_pile = []

    minion_effect(a, game)

    assert a.actions == 2
    assert len(a.hand) == 4
    assert len(b.hand) == 4
    assert len(b.discard_pile) == 5


def test_patrol_puts_victory_and_curses_in_hand():
    from cards.intrigue.patrol import patrol_effect
    from cards.base_set.curse import Curse
    game, a, _ = two_player_game()
    a.hand = []
    # top of deck is end: draws 3 Coppers, reveals Curse, Estate, Silver, Copper
    a.deck = [Copper, Silver, Estate, Curse] + [Copper] * 3

    patrol_effect(a, game)

    names = [c.name for c in a.hand]
    assert names.count("Copper") == 3
    assert "Curse" in names and "Estate" in names
    assert "Silver" not in names
    assert len(a.deck) == 2   # Silver + Copper back on top


def test_replace_topdecks_treasure_and_curses_on_victory():
    from cards.intrigue.replace import replace_effect
    game, a, b = two_player_game(a_script=["Copper", "Silver"])
    a.hand = [Copper]
    a.deck = []
    replace_effect(a, game)
    assert a.deck and a.deck[-1].name == "Silver"   # Treasure -> topdeck

    a.script = ["Estate", "Estate"]
    a.hand = [Estate]
    b.discard_pile = []
    replace_effect(a, game)
    assert any(c.name == "Curse" for c in b.discard_pile)   # Victory -> Curse attack


def test_torturer_both_choices():
    from cards.intrigue.torturer import torturer_effect
    game, a, b = two_player_game(
        b_script=[["Discard 2 cards"], ["Copper", "Copper"]])
    a.deck = [Copper] * 3
    b.hand = [Copper] * 4

    torturer_effect(a, game)
    assert len(b.hand) == 2

    b.script = [["Gain a Curse to your hand"]]
    torturer_effect(a, game)
    assert any(c.name == "Curse" for c in b.hand)


def test_trading_post_gains_silver_to_hand():
    from cards.intrigue.trading_post import trading_post_effect
    game, a, _ = two_player_game(a_script=[["Estate", "Estate"]])
    a.hand = [Estate, Estate, Copper]

    trading_post_effect(a, game)

    assert len(game.trash_pile) == 2
    assert any(c.name == "Silver" for c in a.hand)


def test_upgrade_gains_exactly_plus_one():
    from cards.intrigue.upgrade import upgrade_effect
    game, a, _ = two_player_game(a_script=["Estate", "Silver"])
    a.hand = [Estate]   # Estate costs 2 -> must gain a cost-3 card
    a.deck = [Copper]
    a.discard_pile = []

    upgrade_effect(a, game)

    assert Estate in game.trash_pile
    assert any(c.name == "Silver" for c in a.discard_pile)


def test_harem_and_nobles():
    from cards.intrigue.harem import Harem
    from cards.intrigue.nobles import Nobles, nobles_effect
    game, a, _ = two_player_game(a_script=[["+2 Actions"]])
    a.play_treasure(Harem, game) if Harem in a.hand else None
    a.hand = [Harem]
    a.play_treasure(Harem, game)
    assert a.coins == 2

    nobles_effect(a, game)
    assert a.actions == 3

    p = ScriptedPlayer("VP")
    p.deck = [Harem, Nobles]
    assert p.get_victory_points() == 4


# ------------------------------------------------------------- 1st edition

def test_secret_chamber_effect_and_reaction():
    from cards.intrigue_1st_edition.secret_chamber import Secret_Chamber, secret_chamber_effect
    from cards.base_set.witch import witch_effect
    game, a, b = two_player_game(a_script=[["Estate", "Estate"]],
                                 b_script=[True, ["Estate", "Estate"]])
    a.hand = [Estate, Estate, Copper]
    secret_chamber_effect(a, game)
    assert a.coins == 2 and len(a.hand) == 1

    # Reaction to Witch: draw 2, topdeck 2 (does not block the Curse)
    b.hand = [Secret_Chamber, Estate]
    b.deck = [Copper, Estate]
    b.discard_pile = []
    a.deck = [Copper, Copper]
    witch_effect(a, game)
    assert b.deck[-1].name == "Estate"          # topdecked
    assert any(c.name == "Curse" for c in b.discard_pile)   # still cursed


def test_great_hall_cantrip_and_vp():
    from cards.intrigue_1st_edition.great_hall import Great_Hall, great_hall_effect
    game, a, _ = two_player_game()
    a.hand = []
    a.deck = [Copper]
    great_hall_effect(a, game)
    assert len(a.hand) == 1 and a.actions == 2

    p = ScriptedPlayer("VP")
    p.deck = [Great_Hall]
    assert p.get_victory_points() == 1


def test_coppersmith_boosts_coppers():
    from cards.intrigue_1st_edition.coppersmith import coppersmith_effect
    game, a, _ = two_player_game()
    a.start_turn()
    coppersmith_effect(a, game)
    a.hand = [Copper, Copper]
    a.play_treasure(a.hand[0], game)
    a.play_treasure(a.hand[0], game)
    assert a.coins == 4   # 2 Coppers at 2 each


def test_scout_takes_victory_cards():
    from cards.intrigue_1st_edition.scout import scout_effect
    game, a, _ = two_player_game()
    a.hand = []
    a.deck = [Copper, Estate, Silver, Estate]   # reveals Estate, Silver, Estate, Copper

    scout_effect(a, game)

    assert [c.name for c in a.hand] == ["Estate", "Estate"]
    assert len(a.deck) == 2
    assert a.actions == 2


def test_saboteur_trashes_first_three_plus_cost():
    from cards.intrigue_1st_edition.saboteur import saboteur_effect
    game, a, b = two_player_game()
    b.hand = []
    b.deck = [Gold, Copper, Copper]   # reveals Copper, Copper then Gold
    b.discard_pile = []

    saboteur_effect(a, game)

    assert any(c.name == "Gold" for c in game.trash_pile)
    assert len(b.discard_pile) == 2   # the two Coppers


def test_tribute_bonuses_for_different_names():
    from cards.intrigue_1st_edition.tribute import tribute_effect
    game, a, b = two_player_game()
    a.deck = [Copper] * 4
    a.hand = []
    b.hand = []
    b.deck = [Estate, Silver]   # reveals Silver (Treasure) + Estate (Victory)

    tribute_effect(a, game)

    assert a.coins == 2          # Treasure
    assert len(a.hand) == 2      # Victory -> +2 Cards
    assert len(b.discard_pile) == 2


def test_bot_game_on_intrigue_kingdom_completes():
    from bots import BigMoneyBot, SmithyMoneyBot
    from cards.intrigue.courtyard import Courtyard
    from cards.intrigue.pawn import Pawn
    from cards.intrigue.shanty_town import Shanty_Town
    from cards.intrigue.swindler import Swindler
    from cards.intrigue.baron import Baron
    from cards.intrigue.bridge import Bridge
    from cards.intrigue.torturer import Torturer
    from cards.intrigue.minion import Minion
    from cards.intrigue.harem import Harem
    from cards.intrigue.nobles import Nobles

    random.seed(99)
    kingdom = [Courtyard, Pawn, Shanty_Town, Swindler, Baron,
               Bridge, Torturer, Minion, Harem, Nobles]
    players = [SmithyMoneyBot("smx"), BigMoneyBot("bm")]
    game = make_game(players, kingdom=kingdom)
    game.run(max_turns=400)

    assert game.winners()
    for p in players:
        assert isinstance(p.get_victory_points(), int)
