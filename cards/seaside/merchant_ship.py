from card import Card

def merchant_ship_effect(player, game):
    player.coins += 2

    def next_turn(pl, g):
        pl.coins += 2
        print(f"{pl.name} gets +2 Coins (Merchant Ship).")
    player.add_duration("Merchant Ship", next_turn)

Merchant_Ship = Card(
    "Merchant Ship",
    cost=5,
    card_type=["Action", "Duration"],
    description="Now and at the start of your next turn: +2 Coins.",
    effect=merchant_ship_effect,
    expansion="seaside"
)
