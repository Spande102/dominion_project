from card import Card

def quarry_effect(player, game):
    player.turn_state.action_cost_reduction += 2
    print("Action cards cost 2 less this turn (Quarry).")
    return 1

Quarry = Card(
    "Quarry",
    cost=4,
    card_type=["Treasure"],
    description="+1 Coin. While this is in play, Action cards cost 2 Coins less.",
    effect=quarry_effect,
    expansion="prosperity"
)
