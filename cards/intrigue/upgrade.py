from card import Card

def upgrade_effect(player, game):
    player.draw_cards(1)
    player.actions += 1
    if not player.hand:
        print("No cards in hand to trash.")
        return
    to_trash = player.choose_card_from(
        player.hand, "Choose a card to trash:", optional=False)
    player.hand.remove(to_trash)
    game.trash_pile.append(to_trash)
    print(f"{player.name} trashes {to_trash.name}.")

    target_cost = game.card_cost(to_trash) + 1
    pile_name = player.choose_supply_pile(
        game, f"Gain a card costing exactly {target_cost}:",
        predicate=lambda c: game.card_cost(c) == target_cost, optional=False)
    gained = player.gain_card(game, pile_name)
    if gained:
        print(f"{player.name} gains {gained.name}.")
    else:
        print(f"No card costing exactly {target_cost} to gain.")

Upgrade = Card(
    "Upgrade",
    cost=5,
    card_type=["Action"],
    description="+1 Card +1 Action. Trash a card from your hand. Gain a card costing exactly 1 more than it.",
    effect=upgrade_effect,
    expansion="intrigue"
)
