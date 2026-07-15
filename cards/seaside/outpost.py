from card import Card

def outpost_effect(player, game):
    if player.outpost_turn:
        print("This is already an extra turn - Outpost does nothing.")
        return
    player.outpost_requested = True
    # Stays in play through the extra turn
    player.add_duration("Outpost", None)
    print(f"{player.name} will take an extra turn with a 3-card hand.")

Outpost = Card(
    "Outpost",
    cost=5,
    card_type=["Action", "Duration"],
    description="You only draw 3 cards for your next hand. Take an extra turn after this one (but not a 3rd turn in a row).",
    effect=outpost_effect,
    expansion="seaside"
)
