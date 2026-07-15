def victory_pile_count(num_players):
    return 8 if num_players == 2 else 12


def build_kingdom_supply(kingdom_cards, num_players=2, include_colony=False):
    """Build a full supply from 10 kingdom cards plus the standard cards.
    Kingdom Victory piles use the victory count (8/12) instead of 10.
    A Potion pile is added when any kingdom card has a Potion cost."""
    supply = {}
    for card in kingdom_cards:
        count = victory_pile_count(num_players) if "Victory" in card.card_type else 10
        supply[card.name] = [card] * count
    if any(card.potion_cost > 0 for card in kingdom_cards):
        from cards.alchemy.potion import Potion
        supply["Potion"] = [Potion] * 16
    add_standard_cards(supply, num_players, include_colony=include_colony)
    return supply


def add_standard_cards(supply, num_players=2, include_colony=False):
    from cards.base_set.copper import Copper
    from cards.base_set.silver import Silver
    from cards.base_set.gold import Gold
    from cards.base_set.estate import Estate
    from cards.base_set.duchy import Duchy
    from cards.base_set.province import Province
    from cards.base_set.curse import Curse

    if include_colony:
        from cards.prosperity.platinum import Platinum
        from cards.prosperity.colony import Colony

    # Treasures
    supply["Copper"] = [Copper for _ in range(60)]
    supply["Silver"] = [Silver for _ in range(40)]
    supply["Gold"]   = [Gold for _ in range(30)]



    # Victory cards
    victory_count = victory_pile_count(num_players)
    supply["Estate"]   = [Estate for _ in range(victory_count)]
    supply["Duchy"]    = [Duchy for _ in range(victory_count)]
    supply["Province"] = [Province for _ in range(victory_count)]


    if include_colony:
        supply["Platinum"] = [Platinum for _ in range(12)]
        supply["Colony"] = [Colony for _ in range(victory_count)]

    # Curses
    curse_count = (num_players - 1) * 10
    supply["Curse"] = [Curse for _ in range(curse_count)]