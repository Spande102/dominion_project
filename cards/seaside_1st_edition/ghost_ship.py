from card import Card

def ghost_ship_effect(player, game):
    player.draw_cards(2)
    for other in game.attack_targets(player):
        excess = len(other.hand) - 3
        if excess <= 0:
            print(f"{other.name} has 3 or fewer cards in hand.")
            continue
        to_topdeck = other.choose_cards_from(
            other.hand, f"{other.name}, put cards on your deck until you have 3 in hand:",
            min_count=excess, max_count=excess)
        for card in reversed(to_topdeck):
            other.hand.remove(card)
            other.topdeck(card)
        print(f"{other.name} puts {excess} card(s) on their deck.")

Ghost_Ship = Card(
    "Ghost Ship",
    cost=5,
    card_type=["Action", "Attack"],
    description="+2 Cards. Each other player with 4 or more cards in hand puts cards from their hand onto their deck until they have 3 cards in hand.",
    effect=ghost_ship_effect,
    expansion="seaside_1st_edition"
)
