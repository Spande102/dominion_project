from card import Card

def expand_effect(player, game):
    if not player.hand:
        print("No cards in hand to trash.")
        return
    to_trash = player.choose_card_from(player.hand, "Choose a card to trash:", optional=False)
    player.hand.remove(to_trash)
    game.trash_pile.append(to_trash)
    print(f"{player.name} trashes {to_trash.name}.")

    max_cost = game.card_cost(to_trash) + 3
    pile_name = player.choose_supply_pile(
        game, f"Gain a card costing up to {max_cost}:",
        predicate=game.costs_at_most(max_cost, to_trash.potion_cost), optional=False)
    gained = player.gain_card(game, pile_name)
    if gained:
        print(f"{player.name} gains {gained.name}.")

Expand = Card(
    "Expand",
    cost=7,
    card_type=["Action"],
    description="Trash a card from your hand. Gain a card costing up to 3 more than it.",
    effect=expand_effect,
    expansion="prosperity"
)
