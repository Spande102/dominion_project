from card import Card

def workshop_effect(player, game):
    max_cost = 4

    # Filter cards that are gainable
    gainable = {
        name: pile for name, pile in game.supply.items()
        if pile and pile[0].cost <= max_cost
    }
    if not gainable:
        print("No cards available to gain for 4 or less.")
        return

    print(f"Available to gain (cost ≤ {max_cost}):")
    for name in gainable:
        print(f" - {name} ({len(gainable[name])} left)")

    while True:
        gain_choice = input("Gain which card? ").strip()
        if gain_choice in gainable:
            gained_card = gainable[gain_choice].pop()
            player.discard_pile.append(gained_card)
            print(f"{player.name} gains {gained_card.name}.")
            break
        else:
            print("Invalid choice. Please type the exact card name from the list.")

Workshop = Card(
    "Workshop",
    cost=3,
    card_type = ['Action'],
    description="Gain a card costing up to 4.",
    effect=workshop_effect,
    expansion = "base"
)