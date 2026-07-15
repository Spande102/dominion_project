from card import Card

def lighthouse_effect(player, game):
    player.actions += 1
    player.coins += 1

    def next_turn(pl, g):
        pl.coins += 1
        print(f"{pl.name} gets +1 Coin (Lighthouse).")
    # While in play (checked in Game.attack_targets), attacks don't affect you
    player.add_duration("Lighthouse", next_turn)

Lighthouse = Card(
    "Lighthouse",
    cost=2,
    card_type=["Action", "Duration"],
    description="+1 Action +1 Coin. At the start of your next turn, +1 Coin. While this is in play, when another player plays an Attack card, it doesn't affect you.",
    effect=lighthouse_effect,
    expansion="seaside"
)
