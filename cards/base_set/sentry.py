from card import Card

def sentry_effect(player, game):
    player.draw_cards(1)
    player.actions += 1

    # Look at top 2 cards
    top_cards = player.draw_cards(2, return_card=True)
    if not top_cards:
        print("No cards to look at.")
        return

    print(f"You reveal: {[card.name for card in top_cards]}")

    # Trash step
    to_trash = player.choose_cards_from(top_cards, "Choose cards to TRASH:")
    for card in to_trash:
        top_cards.remove(card)
        game.trash_pile.append(card)
    if to_trash:
        print(f"You trashed: {[card.name for card in to_trash]}")

    # Discard step
    if top_cards:
        to_discard = player.choose_cards_from(top_cards, "Choose cards to DISCARD:")
        for card in to_discard:
            top_cards.remove(card)
            player.discard_pile.append(card)
        if to_discard:
            print(f"You discarded: {[card.name for card in to_discard]}")

    # Put remaining back on top in chosen order
    if top_cards:
        ordered = player.order_cards(top_cards, "Put the rest back on your deck (first = top):")
        # Top of deck is the end of the deck list, so append in reverse order
        for card in reversed(ordered):
            player.topdeck(card)
        print(f"Top of deck is now: {[card.name for card in ordered]}")

Sentry = Card(
    "Sentry",
    cost=5,
    card_type=["Action"],
    description="+1 Card +1 Action. Look at the top 2 cards of your deck. Trash and/or discard any number. Put the rest back in any order.",
    effect=sentry_effect,
    expansion="base"
)
