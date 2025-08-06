from card import Card

def sentry_effect(player, game):
    # Look at top 2 cards
    top_cards = [player.draw_card() for _ in range(2)]
    top_cards = [card for card in top_cards if card is not None]

    if not top_cards:
        print("No cards to look at.")
        return

    print(f"You reveal: {[card.name for card in top_cards]}")

    # Trash step
    to_trash = input("Enter the names of cards to TRASH (comma-separated): ").strip().split(",")
    to_trash = [name.strip().lower() for name in to_trash]
    trashed = []

    for card in top_cards[:]:
        if card.name.lower() in to_trash:
            top_cards.remove(card)
            game.trash_pile.append(card)
            trashed.append(card.name)

    if trashed:
        print(f"You trashed: {trashed}")

    # Discard step
    to_discard = input("Enter names of cards to DISCARD (comma-separated): ").strip().split(",")
    to_discard = [name.strip().lower() for name in to_discard]
    discarded = []

    for card in top_cards[:]:
        if card.name.lower() in to_discard:
            top_cards.remove(card)
            player.discard_pile.append(card)
            discarded.append(card.name)

    if discarded:
        print(f"You discarded: {discarded}")

    # Put remaining back on top in chosen order
    if top_cards:
        print(f"Remaining cards to reorder: {[card.name for card in top_cards]}")
        order = input("Enter the names in desired top-to-bottom order (comma-separated): ").strip().split(",")
        ordered = []
        for name in order:
            match = next((c for c in top_cards if c.name.lower() == name.strip().lower()), None)
            if match:
                top_cards.remove(match)
                ordered.append(match)
        # Add any leftovers in original order
        ordered += top_cards
        for card in reversed(ordered):
            player.deck.insert(0, card)
        print(f"Top of deck is now: {[card.name for card in ordered]}")

Sentry = Card(
    "Sentry",
    cost=5,
    card_type=["Action"],
    description="Look at the top 2 cards of your deck. Trash and/or discard any number. Put the rest back in any order.",
    effect=sentry_effect,
    expansion="base"
)