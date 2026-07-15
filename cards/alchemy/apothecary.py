from card import Card

def apothecary_effect(player, game):
    player.draw_cards(1)
    player.actions += 1
    revealed = player.draw_cards(4, return_card=True)
    if not revealed:
        return
    print(f"{player.name} reveals: {[c.name for c in revealed]}")
    to_hand = [c for c in revealed if c.name in ("Copper", "Potion")]
    for card in to_hand:
        revealed.remove(card)
        player.hand.append(card)
    if to_hand:
        print(f"Coppers/Potions to hand: {[c.name for c in to_hand]}")
    if revealed:
        ordered = player.order_cards(revealed, "Put the rest back (first = top):")
        for card in reversed(ordered):
            player.topdeck(card)

Apothecary = Card(
    "Apothecary",
    cost=2,
    potion_cost=1,
    card_type=["Action"],
    description="+1 Card +1 Action. Reveal the top 4 cards of your deck. Put the Coppers and Potions into your hand. Put the rest back in any order.",
    effect=apothecary_effect,
    expansion="alchemy"
)
