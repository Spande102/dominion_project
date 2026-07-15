from card import Card

def harem_effect(player, game):
    return 2  # +2 coins

def harem_vp(player=None):
    return 2

Harem = Card(
    "Harem",
    cost=6,
    card_type=["Treasure", "Victory"],
    description="+2 Coins | 2 VP",
    effect=harem_effect,
    expansion="intrigue"
)
Harem.get_victory_points = harem_vp
