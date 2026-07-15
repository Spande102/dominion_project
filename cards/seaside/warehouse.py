from card import Card

def warehouse_effect(player, game):
    player.draw_cards(3)
    player.actions += 1
    n = min(3, len(player.hand))
    to_discard = player.choose_cards_from(
        player.hand, "Discard 3 cards:", min_count=n, max_count=n)
    for card in to_discard:
        player.hand.remove(card)
        player.discard_pile.append(card)
    print(f"{player.name} discards {n} card(s).")

Warehouse = Card(
    "Warehouse",
    cost=3,
    card_type=["Action"],
    description="+3 Cards +1 Action. Discard 3 cards.",
    effect=warehouse_effect,
    expansion="seaside"
)
