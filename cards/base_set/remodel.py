from card import Card


def remodel_effect(player, game):
    if not player.hand:
        print("No cards in hand to trash.")
        return

    card_to_trash = player.choose_card_from(player.hand, "Choose a card to trash:", optional=False)
    player.hand.remove(card_to_trash)
    game.trash_pile.append(card_to_trash)
    print(f"{player.name} trashes {card_to_trash.name}.")

    max_cost = game.card_cost(card_to_trash) + 2
    pile_name = player.choose_supply_pile(
        game, f"Gain a card costing up to {max_cost}:",
        predicate=lambda c: game.card_cost(c) <= max_cost, optional=False)
    gained_card = player.gain_card(game, pile_name)
    if gained_card:
        print(f"{player.name} gains {gained_card.name}.")


Remodel = Card(
    "Remodel",
    cost=4,
    card_type=['Action'],
    description="Trash a card from your hand. Gain a card costing up to 2 more.",
    effect=remodel_effect,
    expansion="base"
)
