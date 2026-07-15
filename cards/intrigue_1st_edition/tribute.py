from card import Card

def tribute_effect(player, game):
    left = game.player_to_left(player)
    revealed = left.draw_cards(2, return_card=True)
    if not revealed:
        print(f"{left.name} has no cards to reveal.")
        return
    left.discard_pile.extend(revealed)
    print(f"{left.name} reveals and discards: {[c.name for c in revealed]}")

    seen_names = set()
    for card in revealed:
        if card.name in seen_names:
            continue  # only differently named cards give bonuses
        seen_names.add(card.name)
        if "Action" in card.card_type:
            player.actions += 2
        if "Treasure" in card.card_type:
            player.coins += 2
        if "Victory" in card.card_type:
            player.draw_cards(2)

Tribute = Card(
    "Tribute",
    cost=5,
    card_type=["Action"],
    description="The player to your left reveals then discards the top 2 cards of their deck. For each differently named card revealed, if it is an Action card, +2 Actions; Treasure card, +2 Coins; Victory card, +2 Cards.",
    effect=tribute_effect,
    expansion="intrigue_1st_edition"
)
