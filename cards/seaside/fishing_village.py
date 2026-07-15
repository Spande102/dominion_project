from card import Card

def fishing_village_effect(player, game):
    player.actions += 2
    player.coins += 1

    def next_turn(pl, g):
        pl.actions += 1
        pl.coins += 1
        print(f"{pl.name} gets +1 Action +1 Coin (Fishing Village).")
    player.add_duration("Fishing Village", next_turn)

Fishing_Village = Card(
    "Fishing Village",
    cost=3,
    card_type=["Action", "Duration"],
    description="+2 Actions +1 Coin. At the start of your next turn: +1 Action +1 Coin.",
    effect=fishing_village_effect,
    expansion="seaside"
)
