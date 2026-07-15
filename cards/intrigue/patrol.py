from card import Card

def patrol_effect(player, game):
    player.draw_cards(3)
    revealed = player.draw_cards(4, return_card=True)
    if not revealed:
        return
    print(f"{player.name} reveals: {[c.name for c in revealed]}")

    to_hand = [c for c in revealed
               if "Victory" in c.card_type or "Curse" in c.card_type]
    for card in to_hand:
        revealed.remove(card)
        player.hand.append(card)
    if to_hand:
        print(f"Victory/Curse cards to hand: {[c.name for c in to_hand]}")

    if revealed:
        ordered = player.order_cards(revealed, "Put the rest back on your deck (first = top):")
        for card in reversed(ordered):
            player.topdeck(card)

Patrol = Card(
    "Patrol",
    cost=5,
    card_type=["Action"],
    description="+3 Cards. Reveal the top 4 cards of your deck. Put the Victory cards and Curses into your hand. Put the rest back in any order.",
    effect=patrol_effect,
    expansion="intrigue"
)
