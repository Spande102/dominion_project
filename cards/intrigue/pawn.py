from card import Card

def pawn_effect(player, game):
    chosen = player.choose_options(
        ["+1 Card", "+1 Action", "+1 Buy", "+1 Coin"],
        "Pawn - choose two:", count=2)
    for option in chosen:
        if option == "+1 Card":
            player.draw_cards(1)
        elif option == "+1 Action":
            player.actions += 1
        elif option == "+1 Buy":
            player.buys += 1
        elif option == "+1 Coin":
            player.coins += 1
    print(f"{player.name} chooses {' and '.join(chosen)}.")

Pawn = Card(
    "Pawn",
    cost=2,
    card_type=["Action"],
    description="Choose two: +1 Card; +1 Action; +1 Buy; +1 Coin. The choices must be different.",
    effect=pawn_effect,
    expansion="intrigue"
)
