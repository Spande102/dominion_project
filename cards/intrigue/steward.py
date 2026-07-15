from card import Card

def steward_effect(player, game):
    choice = player.choose_options(
        ["+2 Cards", "+2 Coins", "Trash 2 cards from your hand"],
        "Steward - choose one:")[0]

    if choice == "+2 Cards":
        player.draw_cards(2)
    elif choice == "+2 Coins":
        player.coins += 2
    else:
        n = min(2, len(player.hand))
        to_trash = player.choose_cards_from(
            player.hand, "Choose 2 cards to trash:", min_count=n, max_count=n)
        for card in to_trash:
            player.hand.remove(card)
            game.trash_pile.append(card)
            print(f"{player.name} trashes {card.name}.")

Steward = Card(
    "Steward",
    cost=3,
    card_type=["Action"],
    description="Choose one: +2 Cards; or +2 Coins; or trash 2 cards from your hand.",
    effect=steward_effect,
    expansion="intrigue"
)
