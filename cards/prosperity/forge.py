from card import Card

def forge_effect(player, game):
    to_trash = player.choose_cards_from(
        player.hand, "Trash any number of cards (gain a card costing exactly the total):")
    total = 0
    for card in to_trash:
        player.hand.remove(card)
        game.trash_pile.append(card)
        total += game.card_cost(card)
    print(f"{player.name} trashes {len(to_trash)} card(s) totalling {total} Coins.")

    pile_name = player.choose_supply_pile(
        game, f"Gain a card costing exactly {total}:",
        predicate=game.costs_exactly(total), optional=False)
    gained = player.gain_card(game, pile_name)
    if gained:
        print(f"{player.name} gains {gained.name}.")
    else:
        print(f"No card costing exactly {total} to gain.")

Forge = Card(
    "Forge",
    cost=7,
    card_type=["Action"],
    description="Trash any number of cards from your hand. Gain a card with cost exactly equal to the total cost of the trashed cards.",
    effect=forge_effect,
    expansion="prosperity"
)
