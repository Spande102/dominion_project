from card import Card

def bank_effect(player, game):
    value = sum(1 for c in player.in_play if "Treasure" in c.card_type)
    print(f"Bank is worth {value} Coins ({value} Treasures in play).")
    return value

Bank = Card(
    "Bank",
    cost=7,
    card_type=["Treasure"],
    description="+1 Coin per Treasure you have in play (counting this).",
    effect=bank_effect,
    expansion="prosperity"
)
