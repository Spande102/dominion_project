from card import Card

def bishop_effect(player, game):
    player.coins += 1
    player.victory_tokens += 1
    if player.hand:
        card = player.choose_card_from(
            player.hand, "Trash a card (+1 VP per 2 Coins it costs):", optional=False)
        player.hand.remove(card)
        game.trash_pile.append(card)
        vp = game.card_cost(card) // 2
        player.victory_tokens += vp
        print(f"{player.name} trashes {card.name} for +{vp} VP.")
    # Each other player may trash a card (not an attack)
    for other in game.other_players(player):
        if other.hand:
            card = other.choose_card_from(
                other.hand, f"{other.name}, you may trash a card from your hand:")
            if card:
                other.hand.remove(card)
                game.trash_pile.append(card)
                print(f"{other.name} trashes {card.name}.")

Bishop = Card(
    "Bishop",
    cost=4,
    card_type=["Action"],
    description="+1 Coin +1 VP. Trash a card from your hand. +1 VP per 2 Coins it costs (round down). Each other player may trash a card from their hand.",
    effect=bishop_effect,
    expansion="prosperity"
)
