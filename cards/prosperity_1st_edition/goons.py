from card import Card

def goons_effect(player, game):
    player.buys += 1
    player.coins += 2
    # +1 VP per buy while in play is handled in Game.resolve_on_buy.
    for other in game.attack_targets(player):
        if len(other.hand) > 3:
            excess = len(other.hand) - 3
            to_discard = other.choose_cards_from(
                other.hand, f"{other.name}, discard down to 3 cards:",
                min_count=excess, max_count=excess)
            for card in to_discard:
                other.hand.remove(card)
                other.discard_pile.append(card)
                print(f"{other.name} discards {card.name}.")
        else:
            print(f"{other.name} has 3 or fewer cards in hand.")

Goons = Card(
    "Goons",
    cost=6,
    card_type=["Action", "Attack"],
    description="+1 Buy +2 Coins. Each other player discards down to 3 cards in hand. While this is in play, when you buy a card, +1 VP.",
    effect=goons_effect,
    expansion="prosperity_1st_edition"
)
