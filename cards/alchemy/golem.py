from card import Card

def golem_effect(player, game):
    found = []
    others = []
    while len(found) < 2:
        card = player.draw_cards(1, return_card=True)
        if card is None:
            break
        if "Action" in card.card_type and card.name != "Golem":
            found.append(card)
        else:
            others.append(card)
    player.discard_pile.extend(others)
    if not found:
        print("Golem found no Action cards.")
        return
    print(f"Golem found: {[c.name for c in found]}")
    if len(found) > 1:
        found = player.order_cards(found, "Play them in which order? (first = first)")
    for card in found:
        player.in_play.append(card)
        player.turn_state.actions_played += 1
        print(f"{player.name} plays {card.name} (Golem).")
        if card.effect:
            card.effect(player, game)

Golem = Card(
    "Golem",
    cost=4,
    potion_cost=1,
    card_type=["Action"],
    description="Reveal cards from your deck until you reveal 2 Action cards other than Golems. Discard the other cards, then play the Action cards in either order.",
    effect=golem_effect,
    expansion="alchemy"
)
