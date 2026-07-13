from card import Card

def chapel_effect(player, game):
    to_trash = player.choose_cards_from(player.hand, "Choose up to 4 cards to trash:", min_count=0, max_count=4)
    for card in to_trash:
        player.hand.remove(card)
        game.trash_pile.append(card)
        print(f"{player.name} trashes {card.name}.")
    print(f"{player.name} has trashed {len(to_trash)} card(s).")

Chapel = Card(
    "Chapel",
    cost=2,
    card_type=['Action'],
    description="Trash up to 4 cards from your hand.",
    effect=chapel_effect,
    expansion="base"
)
