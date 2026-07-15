from card import Card

def masquerade_effect(player, game):
    player.draw_cards(2)

    # Each player with cards in hand picks one, then all are passed left
    # simultaneously (players with empty hands are skipped). Not an Attack,
    # so Moat does not apply.
    participants = [p for p in game.players if p.hand]
    if len(participants) > 1:
        passed = []
        for p in participants:
            card = p.choose_card_from(
                p.hand, f"{p.name}, choose a card to pass to your left:", optional=False)
            p.hand.remove(card)
            passed.append(card)
        for i, p in enumerate(participants):
            received = passed[i - 1] if i > 0 else passed[-1]
            # participant i receives from the participant to their right (i-1)
            p.hand.append(received)
            print(f"{p.name} receives a card.")

    # Then you may trash a card from your hand
    if player.hand:
        card = player.choose_card_from(
            player.hand, "You may trash a card from your hand:", optional=True)
        if card:
            player.hand.remove(card)
            game.trash_pile.append(card)
            print(f"{player.name} trashes {card.name}.")

Masquerade = Card(
    "Masquerade",
    cost=3,
    card_type=["Action"],
    description="+2 Cards. Each player with any cards in hand passes one to the next such player to their left, at once. Then you may trash a card from your hand.",
    effect=masquerade_effect,
    expansion="intrigue"
)
