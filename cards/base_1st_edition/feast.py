from card import Card


def feast_effect(player, game):
    max_cost = 5
    pile_name = player.choose_supply_pile(
        game, f"Gain a card costing up to {max_cost}:",
        predicate=lambda c: c.cost <= max_cost, optional=False)
    gained = player.gain_card(game, pile_name)
    if gained:
        print(f"{player.name} gains {gained.name}.")
    else:
        print("No cards available to gain.")
    player.trash_card("Feast", game, zone="in_play")

Feast = Card(
    "Feast",
    cost=4,
    card_type=['Action'],
    description="Trash this card. Gain a card costing up to 5",
    effect=feast_effect,
    expansion="base_1st_edition"
)
