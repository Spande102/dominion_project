"""Per-card effect tests using ScriptedPlayer decisions (no I/O).

Reminder: the TOP of the deck is the END of the deck list.
"""
from cards.base_set.copper import Copper
from cards.base_set.silver import Silver
from cards.base_set.gold import Gold
from cards.base_set.estate import Estate
from cards.base_set.duchy import Duchy
from cards.base_set.village import Village
from cards.base_set.smithy import Smithy
from cards.base_set.moat import Moat

from helpers import ScriptedPlayer, make_game


def two_player_game(a_script=(), b_script=(), kingdom=(Village, Smithy)):
    a = ScriptedPlayer("A", a_script)
    b = ScriptedPlayer("B", b_script)
    game = make_game([a, b], kingdom=kingdom)
    return game, a, b


# ---------------------------------------------------------------- attacks

def test_militia_discard_and_moat_block():
    from cards.base_set.militia import militia_effect
    a = ScriptedPlayer("A")
    b = ScriptedPlayer("B", [True])                    # reveals Moat
    c = ScriptedPlayer("C", [["Copper", "Copper"]])    # discards two Coppers
    game = make_game([a, b, c], kingdom=[Village], num_players=3)
    b.hand = [Moat] + [Copper] * 4
    c.hand = [Copper] * 5

    militia_effect(a, game)

    assert a.coins == 2
    assert len(b.hand) == 5          # blocked
    assert len(c.hand) == 3
    assert len(c.discard_pile) == 2


def test_witch_gives_curses_unless_blocked():
    from cards.base_set.witch import witch_effect
    a = ScriptedPlayer("A")
    b = ScriptedPlayer("B", [True])   # Moat
    c = ScriptedPlayer("C")
    game = make_game([a, b, c], kingdom=[Village], num_players=3)
    b.hand = [Moat]
    c.hand = []
    c.discard_pile = []
    a.deck = [Copper] * 3

    witch_effect(a, game)

    assert not any(card.name == "Curse" for card in b.discard_pile)
    assert any(card.name == "Curse" for card in c.discard_pile)


def test_bandit_defender_chooses_treasure_to_trash():
    from cards.base_set.bandit import bandit_effect
    game, a, b = two_player_game(b_script=["Gold"])  # choose_card_from: trash the Gold
    b.hand = []
    b.deck = [Gold, Silver]           # reveals Silver (top) then Gold
    b.discard_pile = []

    bandit_effect(a, game)

    assert any(card.name == "Gold" for card in a.discard_pile)          # gained Gold
    assert any(card.name == "Gold" for card in game.trash_pile)         # B's Gold trashed
    assert any(card.name == "Silver" for card in b.discard_pile)        # rest discarded


def test_bureaucrat_topdecks_silver_and_victory_card():
    from cards.base_set.bureaucrat import bureaucrat_effect
    game, a, b = two_player_game()
    a.deck = []
    b.hand = [Estate, Copper]
    b.deck = []

    bureaucrat_effect(a, game)

    assert a.deck and a.deck[-1].name == "Silver"
    assert b.deck and b.deck[-1] is Estate
    assert Estate not in b.hand


def test_thief_trashes_and_attacker_gains():
    from cards.base_1st_edition.thief import thief_effect
    game, a, b = two_player_game(a_script=[True])   # confirm: gain the Gold
    b.hand = []
    b.deck = [Estate, Gold]   # top = Gold
    b.discard_pile = []

    thief_effect(a, game)

    assert Gold in a.discard_pile
    assert Estate in b.discard_pile
    assert Gold not in game.trash_pile   # moved from trash to attacker


def test_spy_attacker_decides_discard_or_topdeck():
    from cards.base_1st_edition.spy import spy_effect
    game, a, b = two_player_game(a_script=[True, False])  # discard own, keep B's
    a.hand = []
    a.deck = [Silver, Copper]   # draws Copper (+1 Card), then reveals Silver
    b.hand = []
    b.deck = [Gold]

    spy_effect(a, game)

    assert a.actions == 2
    assert [c.name for c in a.hand] == ["Copper"]
    assert Silver in a.discard_pile          # own revealed card discarded
    assert b.deck and b.deck[-1] is Gold     # B's card put back


# ---------------------------------------------------------------- trashing / gaining

def test_chapel_trashes_up_to_four():
    from cards.base_set.chapel import chapel_effect
    game, a, _ = two_player_game(a_script=[["Estate", "Estate"]])
    a.hand = [Estate, Estate, Copper]

    chapel_effect(a, game)

    assert [c.name for c in a.hand] == ["Copper"]
    assert len(game.trash_pile) == 2


def test_moneylender_confirm_and_decline():
    from cards.base_set.moneylender import moneylender_effect
    game, a, b = two_player_game(a_script=[True], b_script=[False])
    a.hand = [Copper]
    moneylender_effect(a, game)
    assert a.coins == 3 and a.hand == [] and Copper in game.trash_pile

    b.hand = [Copper]
    moneylender_effect(b, game)
    assert b.coins == 0 and b.hand == [Copper]


def test_remodel_trashes_and_gains_up_to_plus_two():
    from cards.base_set.remodel import remodel_effect
    game, a, _ = two_player_game(a_script=["Estate", "Silver"])
    a.hand = [Estate, Copper]
    a.discard_pile = []

    remodel_effect(a, game)

    assert Estate in game.trash_pile
    assert any(c.name == "Silver" for c in a.discard_pile)


def test_mine_trashes_treasure_gains_to_hand():
    from cards.base_set.mine import mine_effect
    game, a, _ = two_player_game(a_script=["Copper", "Silver"])
    a.hand = [Copper, Estate]

    mine_effect(a, game)

    assert Copper in game.trash_pile
    assert any(c.name == "Silver" for c in a.hand)


def test_workshop_gains_up_to_four():
    from cards.base_set.workshop import workshop_effect
    game, a, _ = two_player_game(a_script=["Smithy"])
    a.discard_pile = []

    workshop_effect(a, game)

    assert any(c.name == "Smithy" for c in a.discard_pile)


def test_artisan_gains_to_hand_and_topdecks():
    from cards.base_set.artisan import artisan_effect
    game, a, _ = two_player_game(a_script=["Duchy", "Duchy"])
    a.hand = [Copper]
    a.deck = []

    artisan_effect(a, game)

    assert a.deck and a.deck[-1].name == "Duchy"
    assert not any(c.name == "Duchy" for c in a.hand)


def test_feast_gains_and_trashes_itself():
    from cards.base_1st_edition.feast import Feast, feast_effect
    game, a, _ = two_player_game(a_script=["Duchy"])
    a.in_play = [Feast]   # as Player.play_card would have placed it
    a.discard_pile = []

    feast_effect(a, game)

    assert any(c.name == "Duchy" for c in a.discard_pile)
    assert Feast not in a.in_play
    assert Feast in game.trash_pile


# ---------------------------------------------------------------- deck manipulation

def test_sentry_trash_discard_and_reorder():
    from cards.base_set.sentry import sentry_effect
    game, a, _ = two_player_game(a_script=[["Estate"], ["Copper"]])
    a.hand = []
    a.deck = [Copper, Estate, Copper, Gold]  # draws Gold, looks at Copper+Estate
    a.discard_pile = []
    trash_before = len(game.trash_pile)

    sentry_effect(a, game)

    assert [c.name for c in a.hand] == ["Gold"]
    assert a.actions == 2
    assert len(game.trash_pile) == trash_before + 1
    assert len(a.discard_pile) == 1


def test_sentry_reorders_kept_cards():
    from cards.base_set.sentry import sentry_effect
    # keep both, order: Estate on top
    game, a, _ = two_player_game(a_script=[[], [], ["Estate", "Copper"]])
    a.hand = []
    a.deck = [Copper, Estate, Gold]

    sentry_effect(a, game)

    assert a.deck[-1] is Estate      # top
    assert a.deck[-2] is Copper


def test_harbinger_topdecks_from_discard():
    from cards.base_set.harbinger import harbinger_effect
    game, a, _ = two_player_game(a_script=["Estate"])
    a.hand = []
    a.deck = [Copper, Copper]
    a.discard_pile = [Estate]

    harbinger_effect(a, game)

    assert a.actions == 2
    assert a.deck[-1] is Estate


def test_chancellor_may_discard_deck():
    from cards.base_1st_edition.chancellor import chancellor_effect
    game, a, _ = two_player_game(a_script=[True])
    a.deck = [Copper] * 4
    a.discard_pile = []

    chancellor_effect(a, game)

    assert a.coins == 2
    assert a.deck == []
    assert len(a.discard_pile) == 4


def test_adventurer_digs_for_two_treasures():
    from cards.base_1st_edition.adventurer import adventurer_effect
    game, a, _ = two_player_game()
    a.hand = []
    a.deck = [Estate, Silver, Estate, Copper]  # draws Copper, Estate, Silver

    adventurer_effect(a, game)

    assert sorted(c.name for c in a.hand) == ["Copper", "Silver"]
    assert Estate in a.discard_pile
    assert a.deck == [Estate]


# ---------------------------------------------------------------- play-again / draw cards

def test_throne_room_plays_twice_and_keeps_card():
    from cards.base_set.throne_room import throne_room_effect
    game, a, _ = two_player_game(a_script=["Smithy"])
    a.hand = [Smithy]
    a.deck = [Copper] * 8

    throne_room_effect(a, game)

    assert Smithy in a.in_play
    assert len(a.hand) == 6   # two Smithy plays = 6 cards


def test_throne_room_can_be_skipped():
    from cards.base_set.throne_room import throne_room_effect
    game, a, _ = two_player_game(a_script=[None])
    a.hand = [Smithy]

    throne_room_effect(a, game)

    assert a.hand == [Smithy]
    assert a.in_play == []


def test_vassal_plays_discarded_action():
    from cards.base_set.vassal import vassal_effect
    game, a, _ = two_player_game(a_script=[True])
    a.hand = []
    a.deck = [Copper, Village]  # top = Village

    vassal_effect(a, game)

    assert a.coins == 2
    assert Village in a.in_play       # survived to be discarded at cleanup
    assert a.actions == 3             # Village gave +2 actions
    assert len(a.hand) == 1           # Village drew a card


def test_library_draws_to_seven_and_sets_aside():
    from cards.base_set.library import library_effect
    game, a, _ = two_player_game(a_script=[False])  # skip the Action
    a.hand = [Copper] * 5
    a.deck = [Copper, Village, Copper]  # draws Copper, Village (skipped), Copper
    a.discard_pile = []

    library_effect(a, game)

    assert len(a.hand) == 7
    assert Village in a.discard_pile


def test_merchant_first_silver_bonus():
    from cards.base_set.merchant import Merchant
    game, a, _ = two_player_game()
    a.start_turn()
    a.hand = [Merchant, Silver, Silver]
    a.deck = [Copper]

    a.play_card(Merchant, game)
    silver1 = next(c for c in a.hand if c.name == "Silver")
    a.play_treasure(silver1, game)
    silver2 = next(c for c in a.hand if c.name == "Silver")
    a.play_treasure(silver2, game)

    assert a.coins == 5   # 2 + 1 bonus + 2


def test_moat_draws_two():
    from cards.base_set.moat import moat_effect
    game, a, _ = two_player_game()
    a.hand = []
    a.deck = [Copper] * 3

    moat_effect(a, game)

    assert len(a.hand) == 2
