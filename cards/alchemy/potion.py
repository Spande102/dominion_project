from card import Card

def potion_effect(player, game):
    player.potions += 1
    return 0

Potion = Card(
    "Potion",
    cost=4,
    card_type=["Treasure"],
    description="1 Potion. (Some Alchemy cards need Potions to buy.)",
    effect=potion_effect,
    expansion="alchemy"
)
