import random

import pytest

from bots import BOT_TYPES, BigMoneyBot, EngineBot, GardensRushBot, SlogBot
from cards.base_set.chapel import Chapel
from cards.base_set.copper import Copper
from cards.base_set.curse import Curse
from cards.base_set.estate import Estate
from cards.base_set.gardens import Gardens
from cards.base_set.gold import Gold
from cards.base_set.laboratory import Laboratory
from cards.base_set.market import Market
from cards.base_set.militia import Militia
from cards.base_set.moat import Moat
from cards.base_set.silver import Silver
from cards.base_set.smithy import Smithy
from cards.base_set.village import Village
from cards.base_set.witch import Witch
from cards.base_set.workshop import Workshop
from match import run_match

from helpers import make_game

TEST_KINGDOM = [Village, Smithy, Laboratory, Market, Chapel,
                Workshop, Gardens, Witch, Militia, Moat]


def test_bot_reveals_moat():
    bot = BigMoneyBot("B")
    assert bot.confirm("B, reveal Moat in response to the attack?") is True


def test_bot_discards_junk_first_under_militia():
    bot = BigMoneyBot("B")
    hand = [Gold, Estate, Copper, Curse, Silver]
    chosen = bot.choose_cards_from(hand, "discard down to 3 cards:", min_count=2, max_count=2)
    assert chosen == [Curse, Estate]


def test_bot_spy_keeps_own_card_flips_others():
    bot = BigMoneyBot("Alice")
    assert bot.confirm("Discard Alice's revealed card (Gold)?") is False
    assert bot.confirm("Discard Bob's revealed card (Gold)?") is True


def test_engine_bot_plays_village_before_smithy():
    bot = EngineBot("E")
    game = make_game([bot, BigMoneyBot("B")], kingdom=TEST_KINGDOM)
    assert bot.choose_action_to_play(game, [Smithy, Village]) is Village
    assert bot.choose_action_to_play(game, [Smithy]) is Smithy


def test_big_money_duchy_dance():
    bot = BigMoneyBot("B")
    game = make_game([bot, BigMoneyBot("B2")], kingdom=TEST_KINGDOM)
    bot.coins = 5
    assert bot.choose_buy(game) is None or bot.choose_buy(game) == "Silver"
    game.supply["Province"] = game.supply["Province"][:3]
    assert bot.choose_buy(game) == "Duchy"
    game.supply["Province"] = game.supply["Province"][:1]
    bot.coins = 3
    assert bot.choose_buy(game) == "Estate"


def test_gardens_rush_workshop_gains_gardens():
    from cards.base_set.workshop import workshop_effect
    bot = GardensRushBot("R")
    game = make_game([bot, BigMoneyBot("B")], kingdom=TEST_KINGDOM)
    bot.discard_pile = []

    workshop_effect(bot, game)

    assert any(c.name == "Gardens" for c in bot.discard_pile)


def test_gardens_rush_falls_back_to_big_money_without_gardens():
    bot = GardensRushBot("R")
    game = make_game([bot, BigMoneyBot("B")], kingdom=[Village, Smithy])
    bot.coins = 6
    assert bot.choose_buy(game) == "Gold"


def test_slog_prefers_duchies_then_dukes():
    from cards.intrigue.duke import Duke
    bot = SlogBot("S")
    game = make_game([bot, BigMoneyBot("B")], kingdom=[Duke, Village])
    bot.coins = 5
    assert bot.choose_buy(game) == "Duchy"
    bot.deck += [game.supply["Duchy"][0]] * 4   # owns 4 Duchies, 0 Dukes
    assert bot.choose_buy(game) == "Duke"


@pytest.mark.parametrize("bot_type", list(BOT_TYPES))
def test_every_bot_completes_a_game_vs_big_money(bot_type):
    random.seed(hash(bot_type) % 1000)
    players = [BOT_TYPES[bot_type](bot_type), BigMoneyBot("bm")]
    game = make_game(players, kingdom=TEST_KINGDOM)
    game.run(max_turns=400)

    for p in players:
        assert isinstance(p.get_victory_points(), int)
        assert len(p.hand) == 5   # cleanup ran on every turn
    assert game.winners()


def test_run_match_results_sum_to_num_games():
    results = run_match(["big_money", "smithy_money"], num_games=4,
                        kingdom_cards=TEST_KINGDOM, seed=7)
    assert sum(results.values()) == 4
    assert set(results) == {"big_money-1", "smithy_money-2", "tie"}


def test_run_match_rejects_unknown_bot():
    with pytest.raises(ValueError):
        run_match(["big_money", "nope"], num_games=1)
