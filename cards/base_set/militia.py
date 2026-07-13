from card import Card

def militia_effect(player, game):
    # +2 Coins
    player.coins += 2
    print(f"{player.name} gets +2 Coins.")

    for other in game.attack_targets(player):
        if len(other.hand) > 3:
            excess = len(other.hand) - 3
            print(f"\n{other.name}'s hand: {[c.name for c in other.hand]}")
            to_discard = other.choose_cards_from(
                other.hand, f"{other.name}, discard down to 3 cards:",
                min_count=excess, max_count=excess)
            for card in to_discard:
                other.hand.remove(card)
                other.discard_pile.append(card)
                print(f"{other.name} discards {card.name}.")
        else:
            print(f"{other.name} has 3 or fewer cards, no discard needed.")

Militia = Card(
    "Militia",
    cost = 4,
    card_type = ['Action', 'Attack'],
    description = "+2 Coins. Each other player discards down to 3 cards.",
    effect = militia_effect,
    expansion = "base"
)
