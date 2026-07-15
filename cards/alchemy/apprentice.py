from card import Card

def apprentice_effect(player, game):
    player.actions += 1
    if not player.hand:
        print("No cards in hand to trash.")
        return
    card = player.choose_card_from(
        player.hand, "Trash a card (+1 Card per Coin it costs, +2 per Potion):",
        optional=False)
    player.hand.remove(card)
    game.trash_pile.append(card)
    draw = game.card_cost(card) + 2 * card.potion_cost
    player.draw_cards(draw)
    print(f"{player.name} trashes {card.name} and draws {draw} card(s).")

Apprentice = Card(
    "Apprentice",
    cost=5,
    card_type=["Action"],
    description="+1 Action. Trash a card from your hand. +1 Card per Coin it costs. +2 Cards if it has a Potion in its cost.",
    effect=apprentice_effect,
    expansion="alchemy"
)
