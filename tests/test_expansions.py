"""Tests for Seaside (Durations), Prosperity (buy hooks, VP tokens),
and Alchemy (Potions)."""
import random

from cards.base_set.copper import Copper
from cards.base_set.silver import Silver
from cards.base_set.gold import Gold
from cards.base_set.estate import Estate
from cards.base_set.village import Village
from cards.base_set.smithy import Smithy

from helpers import ScriptedPlayer, make_game


def two_player_game(a_script=(), b_script=(), kingdom=(Village, Smithy)):
    a = ScriptedPlayer("A", a_script)
    b = ScriptedPlayer("B", b_script)
    game = make_game([a, b], kingdom=kingdom)
    return game, a, b


def run_queued_duration_effects(player, game):
    effects = player.next_turn_effects
    player.next_turn_effects = []
    for effect in effects:
        effect(player, game)
    player.in_play.extend(player.duration_in_play)
    player.duration_in_play = []


# ---------------------------------------------------------------- Durations

def test_wharf_stays_in_play_and_fires_next_turn():
    from cards.seaside.wharf import Wharf
    game, a, _ = two_player_game()
    a.hand = [Wharf]
    a.deck = [Copper] * 8

    a.play_card(Wharf, game)
    assert len(a.hand) == 2 and a.buys == 2
    assert Wharf in a.duration_in_play

    a.cleanup(game)
    assert Wharf in a.duration_in_play          # not discarded
    assert Wharf not in a.discard_pile

    a.start_turn()
    run_queued_duration_effects(a, game)
    assert a.buys == 2                          # +1 Buy again
    assert Wharf in a.in_play                   # discards at this cleanup


def test_haven_delivers_set_aside_card():
    from cards.seaside.haven import Haven
    game, a, _ = two_player_game(a_script=["Gold"])
    a.hand = [Haven, Gold]
    a.deck = [Copper] * 2

    a.play_card(Haven, game)
    assert Gold in a.set_aside
    assert Gold not in a.hand

    a.start_turn()
    run_queued_duration_effects(a, game)
    assert Gold in a.hand
    assert a.set_aside == []


def test_lighthouse_blocks_attacks_while_in_play():
    from cards.seaside.lighthouse import Lighthouse
    from cards.base_set.witch import witch_effect
    game, a, b = two_player_game()
    b.hand = [Lighthouse] + [Copper] * 4
    b.play_card(Lighthouse, game)
    b.discard_pile = []
    a.deck = [Copper] * 3

    witch_effect(a, game)
    assert not any(c.name == "Curse" for c in b.discard_pile)


def test_tactician_discards_hand_for_big_next_turn():
    from cards.seaside.tactician import Tactician
    game, a, _ = two_player_game()
    a.hand = [Tactician, Copper, Copper]
    a.deck = [Copper] * 6

    a.play_card(Tactician, game)
    assert a.hand == []

    a.start_turn()
    run_queued_duration_effects(a, game)
    assert len(a.hand) == 5 and a.actions == 2 and a.buys == 2


def test_outpost_requests_extra_turn_and_draws_three():
    from cards.seaside.outpost import Outpost
    game, a, b = two_player_game(a_script=["Outpost"])
    a.hand = [Outpost]
    a.deck = [Copper] * 10

    a.take_turn(game)
    assert a.outpost_requested
    assert len(a.hand) == 3     # cleanup drew 3, not 5


def test_monkey_draws_on_right_players_gains():
    from cards.seaside.monkey import monkey_effect
    game, a, b = two_player_game()
    a.hand = []
    a.deck = [Copper] * 3
    monkey_effect(a, game)   # watches b (player to a's right in 2p)

    b.gain_card(game, "Silver")
    assert len(a.hand) == 1

    a.start_turn()
    run_queued_duration_effects(a, game)
    assert len(a.hand) == 2      # +1 Card at start of turn
    b.gain_card(game, "Silver")
    assert len(a.hand) == 2      # listener unregistered


def test_corsair_trashes_first_silver_or_gold():
    from cards.seaside.corsair import corsair_effect
    game, a, b = two_player_game()
    corsair_effect(a, game)
    assert a.coins == 2

    b.hand = [Silver, Silver]
    b.play_treasure(b.hand[0], game)
    assert Silver in game.trash_pile             # first Silver trashed
    trash_count = len(game.trash_pile)
    b.play_treasure(b.hand[0], game)
    assert len(game.trash_pile) == trash_count   # second one safe


def test_island_and_native_village_mats_count_for_vp():
    from cards.seaside.island import Island, island_effect
    game, a, _ = two_player_game(a_script=["Estate"])
    a.deck, a.hand, a.discard_pile = [], [Estate, Copper], []
    a.in_play = [Island]
    island_effect(a, game)

    assert Island in a.island_mat and Estate in a.island_mat
    assert a.get_victory_points() == 3   # Island 2 + Estate 1

    a.native_village_mat = [Estate]
    assert a.get_victory_points() == 4


def test_treasure_map_needs_two_maps():
    from cards.seaside.treasure_map import Treasure_Map, treasure_map_effect
    game, a, _ = two_player_game()
    a.in_play = [Treasure_Map]
    a.hand = [Treasure_Map]
    a.deck = []

    treasure_map_effect(a, game)
    assert len([c for c in a.deck if c.name == "Gold"]) == 4
    assert len(game.trash_pile) == 2


def test_sea_hag_curses_onto_deck():
    from cards.seaside_1st_edition.sea_hag import sea_hag_effect
    game, a, b = two_player_game()
    b.hand = []
    b.deck = [Copper]
    sea_hag_effect(a, game)
    assert b.deck and b.deck[-1].name == "Curse"
    assert Copper in b.discard_pile


def test_ghost_ship_topdecks_down_to_three():
    from cards.seaside_1st_edition.ghost_ship import ghost_ship_effect
    game, a, b = two_player_game(b_script=[["Copper", "Copper"]])
    a.deck = [Copper] * 3
    b.hand = [Copper] * 5
    b.deck = []
    ghost_ship_effect(a, game)
    assert len(b.hand) == 3 and len(b.deck) == 2


def test_embargo_curses_buys():
    from cards.seaside_1st_edition.embargo import Embargo, embargo_effect
    game, a, _ = two_player_game(a_script=["Silver"])
    a.in_play = [Embargo]
    embargo_effect(a, game)
    assert game.embargo_tokens["Silver"] == 1
    assert Embargo in game.trash_pile

    game.current_player = a
    a.coins, a.buys = 3, 1
    a.buy_card(game, "Silver")
    assert any(c.name == "Curse" for c in a.discard_pile)


# ---------------------------------------------------------------- Prosperity

def test_goons_gives_vp_per_buy():
    from cards.prosperity_1st_edition.goons import Goons
    game, a, _ = two_player_game()
    game.current_player = a
    a.in_play = [Goons]
    a.coins, a.buys = 6, 2
    a.buy_card(game, "Silver")
    a.buy_card(game, "Silver")
    assert a.victory_tokens == 2


def test_hoard_gains_gold_on_victory_buy():
    from cards.prosperity.hoard import Hoard
    game, a, _ = two_player_game()
    game.current_player = a
    a.in_play = [Hoard]
    a.coins, a.buys = 2, 1
    a.buy_card(game, "Estate")
    assert any(c.name == "Gold" for c in a.discard_pile)


def test_talisman_copies_cheap_non_victory_buys():
    from cards.prosperity_1st_edition.talisman import Talisman
    game, a, _ = two_player_game()
    game.current_player = a
    a.in_play = [Talisman]
    a.coins, a.buys = 3, 1
    a.buy_card(game, "Silver")
    assert sum(1 for c in a.discard_pile if c.name == "Silver") == 2


def test_mint_buy_trashes_treasures_in_play():
    from cards.prosperity.mint import Mint
    game, a, _ = two_player_game(kingdom=(Village, Mint))
    game.current_player = a
    a.in_play = [Copper, Silver, Village]
    a.coins, a.buys = 5, 1
    a.buy_card(game, "Mint")
    assert Copper in game.trash_pile and Silver in game.trash_pile
    assert Village in a.in_play


def test_royal_seal_topdecks_bought_card():
    from cards.prosperity_1st_edition.royal_seal import Royal_Seal
    game, a, _ = two_player_game(a_script=[True])
    game.current_player = a
    a.in_play = [Royal_Seal]
    a.coins, a.buys = 3, 1
    a.buy_card(game, "Silver")
    assert a.deck and a.deck[-1].name == "Silver"


def test_watchtower_reaction_on_gain():
    from cards.prosperity.watchtower import Watchtower
    game, a, _ = two_player_game(a_script=[True, ["Trash it"]])
    a.hand = [Watchtower]
    a.gain_card(game, "Curse")
    assert any(c.name == "Curse" for c in game.trash_pile)
    assert not any(c.name == "Curse" for c in a.discard_pile)


def test_treasury_topdecks_at_cleanup_unless_victory_bought():
    from cards.seaside.treasury import Treasury
    game, a, _ = two_player_game(a_script=[True])
    a.in_play = [Treasury]
    a.deck = [Copper] * 5
    a.cleanup(game)
    assert Treasury in a.hand    # topdecked, then drawn into the next hand

    a2 = ScriptedPlayer("A2", [True])
    a2.in_play = [Treasury]
    a2.deck = [Copper] * 5
    a2.turn_state.bought_victory = True
    a2.cleanup(game)
    assert Treasury in a2.discard_pile


def test_quarry_and_bridge_stack():
    from cards.prosperity.quarry import quarry_effect
    from cards.intrigue.bridge import bridge_effect
    game, a, _ = two_player_game()
    game.current_player = a
    quarry_effect(a, game)
    bridge_effect(a, game)
    assert game.card_cost(Village) == 0    # 3 - 2 - 1
    assert game.card_cost(Silver) == 2     # 3 - 1 (Quarry only hits Actions)


def test_peddler_discount_per_action_in_play():
    from cards.prosperity.peddler import Peddler
    game, a, _ = two_player_game()
    game.current_player = a
    assert game.card_cost(Peddler) == 8
    a.in_play = [Village, Smithy, Village]
    assert game.card_cost(Peddler) == 2


def test_bank_counts_treasures_in_play():
    from cards.prosperity.bank import Bank
    game, a, _ = two_player_game()
    a.hand = [Copper, Copper, Bank]
    a.play_treasure(a.hand[0], game)
    a.play_treasure(a.hand[0], game)
    a.play_treasure(a.hand[0], game)   # Bank: 3 treasures in play incl. itself
    assert a.coins == 5


def test_kings_court_plays_three_times():
    from cards.prosperity.kings_court import kings_court_effect
    game, a, _ = two_player_game(a_script=["Smithy"])
    a.hand = [Smithy]
    a.deck = [Copper] * 9
    kings_court_effect(a, game)
    assert len(a.hand) == 9
    assert Smithy in a.in_play


def test_forge_gains_exact_total():
    from cards.prosperity.forge import forge_effect
    game, a, _ = two_player_game(a_script=[["Estate", "Estate"], "Smithy"])
    a.hand = [Estate, Estate, Copper]
    a.discard_pile = []
    forge_effect(a, game)   # 2 + 2 = 4 -> Smithy costs 4
    assert any(c.name == "Smithy" for c in a.discard_pile)
    assert len(game.trash_pile) == 2


def test_mountebank_curse_defense():
    from cards.prosperity_1st_edition.mountebank import mountebank_effect
    from cards.base_set.curse import Curse
    game, a, b = two_player_game(b_script=[True])
    b.hand = [Curse]
    b.discard_pile = []
    mountebank_effect(a, game)
    assert Curse in b.discard_pile               # discarded the Curse
    assert not any(c.name == "Copper" for c in b.discard_pile)

    b.script = []
    b.hand = []
    mountebank_effect(a, game)
    assert any(c.name == "Curse" for c in b.discard_pile)
    assert any(c.name == "Copper" for c in b.discard_pile)


def test_venture_digs_and_plays_treasure():
    from cards.prosperity_1st_edition.venture import Venture
    game, a, _ = two_player_game()
    a.hand = [Venture]
    a.deck = [Silver, Estate, Estate]   # digs past 2 Estates to the Silver
    a.play_treasure(a.hand[0], game)
    assert a.coins == 3                 # 1 (Venture) + 2 (Silver)
    assert Silver in a.in_play
    assert len(a.discard_pile) == 2


def test_counting_house_takes_coppers():
    from cards.prosperity_1st_edition.counting_house import counting_house_effect
    game, a, _ = two_player_game(a_script=[["Take 2 Copper(s)"]])
    a.hand = []
    a.discard_pile = [Copper, Copper, Estate]
    counting_house_effect(a, game)
    assert len(a.hand) == 2


# ---------------------------------------------------------------- Alchemy

def test_potion_needed_to_buy_alchemy_cards():
    from cards.alchemy.familiar import Familiar
    game, a, _ = two_player_game(kingdom=(Familiar, Village))
    assert "Potion" in game.supply
    game.current_player = a
    a.coins, a.potions, a.buys = 5, 0, 1
    assert not game.can_buy(a, "Familiar")
    a.potions = 1
    assert game.can_buy(a, "Familiar")
    a.buy_card(game, "Familiar")
    assert a.potions == 0
    assert any(c.name == "Familiar" for c in a.discard_pile)


def test_coin_gainers_cannot_gain_potion_cost_cards():
    from cards.alchemy.familiar import Familiar
    game, a, _ = two_player_game(kingdom=(Familiar, Village))
    game.current_player = a
    assert not game.costs_at_most(4)(Familiar)
    assert game.costs_at_most(4)(Village)


def test_potion_treasure_produces_potion():
    from cards.alchemy.potion import Potion
    game, a, _ = two_player_game()
    a.start_turn()
    a.hand = [Potion]
    a.play_treasure(a.hand[0], game)
    assert a.potions == 1 and a.coins == 0


def test_vineyard_vp():
    from cards.alchemy.vineyard import Vineyard
    p = ScriptedPlayer("VP")
    p.deck = [Village] * 7 + [Vineyard]
    assert p.get_victory_points() == 2   # 7 Actions // 3


def test_transmute_conversions():
    from cards.alchemy.transmute import transmute_effect
    game, a, _ = two_player_game(a_script=["Estate"])
    a.hand = [Estate]
    a.discard_pile = []
    transmute_effect(a, game)
    assert any(c.name == "Gold" for c in a.discard_pile)   # Victory -> Gold


def test_apprentice_draws_cost_plus_potion():
    from cards.alchemy.apprentice import apprentice_effect
    from cards.alchemy.familiar import Familiar
    game, a, _ = two_player_game(a_script=["Familiar"])
    a.hand = [Familiar]
    a.deck = [Copper] * 6
    apprentice_effect(a, game)
    assert len(a.hand) == 5   # 3 coins + 2 for the Potion cost


def test_golem_finds_and_plays_two_actions():
    from cards.alchemy.golem import golem_effect
    game, a, _ = two_player_game()
    a.hand = []
    a.deck = [Village, Estate, Smithy, Copper] + [Copper] * 3
    # top of deck = end: reveals Copper, Copper, Copper, Smithy... then Estate, Village
    golem_effect(a, game)
    assert Smithy in a.in_play and Village in a.in_play
    assert a.actions == 3        # Village's +2
    assert a.turn_state.actions_played == 2


def test_alchemist_topdecks_with_potion_in_play():
    from cards.alchemy.alchemist import Alchemist
    from cards.alchemy.potion import Potion
    game, a, _ = two_player_game(a_script=[True])
    a.in_play = [Alchemist, Potion]
    a.deck = [Copper] * 5
    a.cleanup(game)
    assert Alchemist in a.hand   # topdecked, then drawn into the next hand


def test_herbalist_topdecks_a_treasure():
    from cards.alchemy.herbalist import Herbalist
    game, a, _ = two_player_game(a_script=[True, "Gold"])
    a.in_play = [Herbalist, Gold]
    a.deck = [Copper] * 5
    a.cleanup(game)
    assert Gold in a.hand        # topdecked, then drawn into the next hand
    assert Herbalist in a.discard_pile


# ---------------------------------------------------------------- full games

def test_bot_game_on_seaside_kingdom_completes():
    from bots import EngineBot, SmithyMoneyBot
    from cards.seaside.wharf import Wharf
    from cards.seaside.caravan import Caravan
    from cards.seaside.fishing_village import Fishing_Village
    from cards.seaside.warehouse import Warehouse
    from cards.seaside.cutpurse import Cutpurse
    from cards.seaside.sea_witch import Sea_Witch
    from cards.seaside.merchant_ship import Merchant_Ship
    from cards.seaside.lighthouse import Lighthouse
    from cards.seaside.tide_pools import Tide_Pools
    from cards.seaside.bazaar import Bazaar

    random.seed(7)
    kingdom = [Wharf, Caravan, Fishing_Village, Warehouse, Cutpurse,
               Sea_Witch, Merchant_Ship, Lighthouse, Tide_Pools, Bazaar]
    players = [EngineBot("engine"), SmithyMoneyBot("smx")]
    game = make_game(players, kingdom=kingdom)
    game.run(max_turns=400)
    assert game.winners()
    for p in players:
        assert isinstance(p.get_victory_points(), int)
        assert p.duration_in_play == [] or len(p.hand) == 5


def test_bot_game_on_prosperity_kingdom_completes():
    from bots import EngineBot, BigMoneyBot
    from cards.prosperity.city import City
    from cards.prosperity.grand_market import Grand_Market
    from cards.prosperity.rabble import Rabble
    from cards.prosperity.magnate import Magnate
    from cards.prosperity.quarry import Quarry
    from cards.prosperity.bank import Bank
    from cards.prosperity.peddler import Peddler
    from cards.prosperity.watchtower import Watchtower
    from cards.prosperity_1st_edition.goons import Goons
    from cards.prosperity_1st_edition.mountebank import Mountebank

    random.seed(13)
    kingdom = [City, Grand_Market, Rabble, Magnate, Quarry,
               Bank, Peddler, Watchtower, Goons, Mountebank]
    players = [EngineBot("engine"), BigMoneyBot("bm")]
    game = make_game(players, kingdom=kingdom)
    game.run(max_turns=400)
    assert game.winners()
