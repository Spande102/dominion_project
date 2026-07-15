from card import Card

def conspirator_effect(player, game):
    player.coins += 2
    if player.turn_state.actions_played >= 3:
        player.draw_cards(1)
        player.actions += 1
        print(f"{player.name} has played 3+ Actions: +1 Card +1 Action.")

Conspirator = Card(
    "Conspirator",
    cost=4,
    card_type=["Action"],
    description="+2 Coins. If you've played 3 or more Actions this turn (counting this), +1 Card and +1 Action.",
    effect=conspirator_effect,
    expansion="intrigue"
)
