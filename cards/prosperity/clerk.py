from card import Card

def clerk_effect(player, game):
    player.coins += 2
    # Simplification: the official "at the start of your turn, you may play
    # this" Reaction is not implemented.
    for other in game.attack_targets(player):
        if len(other.hand) >= 5:
            card = other.choose_card_from(
                other.hand, f"{other.name}, put a card onto your deck:", optional=False)
            other.hand.remove(card)
            other.topdeck(card)
            print(f"{other.name} topdecks a card.")
        else:
            print(f"{other.name} has fewer than 5 cards in hand.")

Clerk = Card(
    "Clerk",
    cost=4,
    card_type=["Action", "Reaction", "Attack"],
    description="+2 Coins. Each other player with 5 or more cards in hand puts one onto their deck.",
    effect=clerk_effect,
    expansion="prosperity"
)
