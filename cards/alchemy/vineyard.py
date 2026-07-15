from card import Card

def vineyard_vp(player):
    actions = sum(1 for c in player.all_cards() if "Action" in c.card_type)
    return actions // 3

Vineyard = Card(
    "Vineyard",
    cost=0,
    potion_cost=1,
    card_type=["Victory"],
    description="Worth 1 VP per 3 Action cards you have (round down).",
    expansion="alchemy"
)
Vineyard.get_victory_points = vineyard_vp
