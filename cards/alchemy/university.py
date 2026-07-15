from card import Card

def university_effect(player, game):
    player.actions += 2
    pile_name = player.choose_supply_pile(
        game, "You may gain an Action card costing up to 5:",
        predicate=lambda c: "Action" in c.card_type and game.card_cost(c) <= 5
        and c.potion_cost == 0,
        optional=True)
    gained = player.gain_card(game, pile_name)
    if gained:
        print(f"{player.name} gains {gained.name}.")

University = Card(
    "University",
    cost=2,
    potion_cost=1,
    card_type=["Action"],
    description="+2 Actions. You may gain an Action card costing up to 5.",
    effect=university_effect,
    expansion="alchemy"
)
