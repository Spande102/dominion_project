from card import Card

def venture_effect(player, game):
    revealed = []
    treasure = None
    while True:
        card = player.draw_cards(1, return_card=True)
        if card is None:
            break
        if "Treasure" in card.card_type:
            treasure = card
            break
        revealed.append(card)
    player.discard_pile.extend(revealed)
    if treasure:
        print(f"Venture reveals and plays {treasure.name}.")
        player.hand.append(treasure)
        player.play_treasure(treasure, game)
    return 1

Venture = Card(
    "Venture",
    cost=5,
    card_type=["Treasure"],
    description="+1 Coin. Reveal cards from your deck until you reveal a Treasure. Discard the other revealed cards. Play that Treasure.",
    effect=venture_effect,
    expansion="prosperity_1st_edition"
)
