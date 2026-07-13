import random

from cards.base_set.village import Village
from cards.base_set.smithy import Smithy

from helpers import BigMoneyPlayer, ScriptedPlayer, make_game


def test_game_not_over_at_start():
    game = make_game([ScriptedPlayer("A"), ScriptedPlayer("B")], kingdom=[Village])
    assert not game.is_game_over()


def test_game_over_when_provinces_empty():
    game = make_game([ScriptedPlayer("A"), ScriptedPlayer("B")], kingdom=[Village])
    game.supply["Province"] = []
    assert game.is_game_over()


def test_game_over_when_colonies_empty():
    game = make_game([ScriptedPlayer("A"), ScriptedPlayer("B")], kingdom=[Village])
    game.supply["Colony"] = []
    assert game.is_game_over()


def test_game_over_when_three_piles_empty():
    game = make_game([ScriptedPlayer("A"), ScriptedPlayer("B")], kingdom=[Village, Smithy])
    game.supply["Village"] = []
    game.supply["Smithy"] = []
    assert not game.is_game_over()
    game.supply["Curse"] = []
    assert game.is_game_over()


def test_find_supply_pile_is_case_insensitive():
    game = make_game([ScriptedPlayer("A"), ScriptedPlayer("B")], kingdom=[Village])
    assert game.find_supply_pile("village") == "Village"
    assert game.find_supply_pile("  SILVER ") == "Silver"
    assert game.find_supply_pile("Throne Room") is None
    assert game.find_supply_pile("") is None


def test_initial_decks_are_shuffled_and_drawn():
    random.seed(0)
    players = [ScriptedPlayer("A"), ScriptedPlayer("B")]
    game = make_game(players, kingdom=[Village])
    for p in players:
        assert len(p.hand) == 5
        assert len(p.deck) == 5
    # With a shuffle, at least one of the players' opening hands should not
    # be the unshuffled top-of-deck (3 Estates + 2 Coppers).
    hands = [[c.name for c in p.hand] for p in players]
    assert any(h != ["Estate", "Estate", "Estate", "Copper", "Copper"] for h in hands)


def test_full_big_money_game_completes():
    random.seed(42)
    players = [BigMoneyPlayer("Alice"), BigMoneyPlayer("Bob")]
    game = make_game(players, kingdom=[Village, Smithy])
    game.run()

    assert game.is_game_over()
    for p in players:
        total = len(p.deck) + len(p.hand) + len(p.discard_pile) + len(p.in_play)
        assert total > 10  # both bots bought cards
        assert isinstance(p.get_victory_points(), int)
    # Provinces were actually contested
    assert len(game.supply["Province"]) < 8


def test_resign_ends_game():
    players = [ScriptedPlayer("A"), ScriptedPlayer("B")]
    game = make_game(players, kingdom=[Village])
    assert game.handle_command(players[0], "resign")
    assert not game.running
    assert game.ended_by_resignation
    assert game.resigned_player is players[0]
