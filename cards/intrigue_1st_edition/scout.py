from card import Card

def scout_effect(player, game):
    player.actions += 1
    revealed = player.draw_cards(4, return_card=True)
    if not revealed:
        return
    print(f"{player.name} reveals: {[c.name for c in revealed]}")

    victories = [c for c in revealed if "Victory" in c.card_type]
    for card in victories:
        revealed.remove(card)
        player.hand.append(card)
    if victories:
        print(f"Victory cards to hand: {[c.name for c in victories]}")

    if revealed:
        ordered = player.order_cards(revealed, "Put the rest back on your deck (first = top):")
        for card in reversed(ordered):
            player.topdeck(card)

Scout = Card(
    "Scout",
    cost=4,
    card_type=["Action"],
    description="+1 Action. Reveal the top 4 cards of your deck. Put the revealed Victory cards into your hand. Put the other cards on top of your deck in any order.",
    effect=scout_effect,
    expansion="intrigue_1st_edition"
)
