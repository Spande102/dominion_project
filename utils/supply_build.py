def add_standard_cards(supply, num_players=2):
    from cards.base_set.copper import Copper
    from cards.base_set.silver import Silver
    from cards.base_set.gold import Gold
    from cards.base_set.estate import Estate
    from cards.base_set.duchy import Duchy
    from cards.base_set.province import Province
    from cards.base_set.curse import Curse

    # Treasure cards
    supply["Copper"] = [Copper for _ in range(60)]
    supply["Silver"] = [Silver for _ in range(40)]
    supply["Gold"]   = [Gold   for _ in range(30)]

    # Victory cards (8 each for 2 players, 12 for 3-4)
    victory_count = 8 if num_players == 2 else 12
    supply["Estate"]   = [Estate for _ in range(victory_count)]
    supply["Duchy"]    = [Duchy for _ in range(victory_count)]
    supply["Province"] = [Province for _ in range(victory_count)]

    # Curse cards: 10 per opponent
    curse_count = (num_players - 1) * 10
    supply["Curse"] = [Curse for _ in range(curse_count)]