from card import Card

def coppersmith_effect(player, game):
    player.turn_state.copper_bonus += 1
    print("Copper produces an extra 1 Coin this turn.")

Coppersmith = Card(
    "Coppersmith",
    cost=4,
    card_type=["Action"],
    description="Copper produces an extra 1 Coin this turn.",
    effect=coppersmith_effect,
    expansion="intrigue_1st_edition"
)
