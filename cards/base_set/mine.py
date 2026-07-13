from card import Card

def mine_effect(player, game):
    treasures_in_hand = [card for card in player.hand if "Treasure" in card.card_type]
    if not treasures_in_hand:
        print("No Treasures in hand to trash.")
        return

    to_trash = player.choose_card_from(treasures_in_hand, "You may trash a Treasure from your hand:")
    if not to_trash:
        return

    player.hand.remove(to_trash)
    game.trash_pile.append(to_trash)
    max_cost = to_trash.cost + 3

    pile_name = player.choose_supply_pile(
        game, f"Gain a Treasure to your hand costing up to {max_cost}:",
        predicate=lambda c: "Treasure" in c.card_type and c.cost <= max_cost,
        optional=False)
    gained = player.gain_card(game, pile_name, destination='hand')
    if gained:
        print(f"{player.name} trashes {to_trash.name} and gains {gained.name} to hand.")

Mine = Card(
    "Mine",
    cost=5,
    card_type=["Action"],
    description="You may trash a Treasure from your hand. Gain a Treasure to your hand costing up to 3 more.",
    effect=mine_effect,
    expansion="base"
)
