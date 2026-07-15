from card import Card

def salvager_effect(player, game):
    player.buys += 1
    if not player.hand:
        print("No cards in hand to trash.")
        return
    card = player.choose_card_from(player.hand, "Trash a card for +Coins equal to its cost:",
                                   optional=False)
    player.hand.remove(card)
    game.trash_pile.append(card)
    value = game.card_cost(card)
    player.coins += value
    print(f"{player.name} trashes {card.name} for +{value} Coins.")

Salvager = Card(
    "Salvager",
    cost=4,
    card_type=["Action"],
    description="+1 Buy. Trash a card from your hand. +Coins equal to its cost.",
    effect=salvager_effect,
    expansion="seaside"
)
