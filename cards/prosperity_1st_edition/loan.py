from card import Card

def loan_effect(player, game):
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
        print(f"Loan reveals {treasure.name}.")
        if player.confirm(f"Trash the revealed {treasure.name}? (otherwise discard it)"):
            game.trash_pile.append(treasure)
            print(f"{player.name} trashes {treasure.name}.")
        else:
            player.discard_pile.append(treasure)
    return 1

Loan = Card(
    "Loan",
    cost=3,
    card_type=["Treasure"],
    description="+1 Coin. Reveal cards from your deck until you reveal a Treasure. Discard it or trash it. Discard the other revealed cards.",
    effect=loan_effect,
    expansion="prosperity_1st_edition"
)
