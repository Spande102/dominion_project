from card import Card

def trading_post_effect(player, game):
    n = min(2, len(player.hand))
    if n == 0:
        print("No cards in hand to trash.")
        return
    to_trash = player.choose_cards_from(
        player.hand, "Trash 2 cards from your hand:", min_count=n, max_count=n)
    for card in to_trash:
        player.hand.remove(card)
        game.trash_pile.append(card)
        print(f"{player.name} trashes {card.name}.")
    if len(to_trash) == 2:
        gained = player.gain_card(game, game.find_supply_pile("Silver"), destination='hand')
        if gained:
            print(f"{player.name} gains a Silver to their hand.")

Trading_Post = Card(
    "Trading Post",
    cost=5,
    card_type=["Action"],
    description="Trash 2 cards from your hand. If you did, gain a Silver to your hand.",
    effect=trading_post_effect,
    expansion="intrigue"
)
