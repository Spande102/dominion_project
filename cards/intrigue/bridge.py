from card import Card

def bridge_effect(player, game):
    player.buys += 1
    player.coins += 1
    player.turn_state.cost_reduction += 1
    print("All cards cost 1 less this turn.")

Bridge = Card(
    "Bridge",
    cost=4,
    card_type=["Action"],
    description="+1 Buy +1 Coin. This turn, cards (everywhere) cost 1 Coin less.",
    effect=bridge_effect,
    expansion="intrigue"
)
