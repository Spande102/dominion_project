from card import Card

def workshop_effect(player, game):
    max_cost = 4
    pile_name = player.choose_supply_pile(
        game, f"Gain a card costing up to {max_cost}:",
        predicate=lambda c: c.cost <= max_cost, optional=False)
    gained_card = player.gain_card(game, pile_name)
    if gained_card:
        print(f"{player.name} gains {gained_card.name}.")
    else:
        print("No cards available to gain.")

Workshop = Card(
    "Workshop",
    cost=3,
    card_type=['Action'],
    description="Gain a card costing up to 4.",
    effect=workshop_effect,
    expansion="base"
)
