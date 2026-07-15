from card import Card

def rabble_effect(player, game):
    player.draw_cards(3)
    for other in game.attack_targets(player):
        revealed = other.draw_cards(3, return_card=True)
        if not revealed:
            continue
        print(f"{other.name} reveals: {[c.name for c in revealed]}")
        to_discard = [c for c in revealed
                      if "Action" in c.card_type or "Treasure" in c.card_type]
        for card in to_discard:
            revealed.remove(card)
            other.discard_pile.append(card)
        if to_discard:
            print(f"{other.name} discards: {[c.name for c in to_discard]}")
        if revealed:
            ordered = other.order_cards(revealed, f"{other.name}, put back (first = top):")
            for card in reversed(ordered):
                other.topdeck(card)

Rabble = Card(
    "Rabble",
    cost=5,
    card_type=["Action", "Attack"],
    description="+3 Cards. Each other player reveals the top 3 cards of their deck, discards the Actions and Treasures, and puts the rest back in any order they choose.",
    effect=rabble_effect,
    expansion="prosperity"
)
