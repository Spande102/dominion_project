from card import Card

def ironworks_effect(player, game):
    max_cost = 4
    pile_name = player.choose_supply_pile(
        game, f"Gain a card costing up to {max_cost}:",
        predicate=lambda c: game.card_cost(c) <= max_cost, optional=False)
    gained = player.gain_card(game, pile_name)
    if not gained:
        print("No cards available to gain.")
        return
    print(f"{player.name} gains {gained.name}.")
    if "Action" in gained.card_type:
        player.actions += 1
    if "Treasure" in gained.card_type:
        player.coins += 1
    if "Victory" in gained.card_type:
        player.draw_cards(1)

Ironworks = Card(
    "Ironworks",
    cost=4,
    card_type=["Action"],
    description="Gain a card costing up to 4. If the gained card is an Action card, +1 Action; Treasure card, +1 Coin; Victory card, +1 Card.",
    effect=ironworks_effect,
    expansion="intrigue"
)
