from card import Card

def philosophers_stone_effect(player, game):
    value = (len(player.deck) + len(player.discard_pile)) // 5
    print(f"Philosopher's Stone is worth {value} Coins.")
    return value

Philosophers_Stone = Card(
    "Philosopher's Stone",
    cost=3,
    potion_cost=1,
    card_type=["Treasure"],
    description="When you play this, count your deck and discard pile. Worth 1 Coin per 5 cards total between them (round down).",
    effect=philosophers_stone_effect,
    expansion="alchemy"
)
