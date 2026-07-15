from card import Card

def astrolabe_effect(player, game):
    player.buys += 1

    def next_turn(pl, g):
        pl.coins += 1
        pl.buys += 1
        print(f"{pl.name} gets +1 Coin +1 Buy (Astrolabe).")
    player.add_duration("Astrolabe", next_turn)
    return 1  # +1 Coin now

Astrolabe = Card(
    "Astrolabe",
    cost=3,
    card_type=["Treasure", "Duration"],
    description="Now and at the start of your next turn: +1 Coin +1 Buy.",
    effect=astrolabe_effect,
    expansion="seaside"
)
