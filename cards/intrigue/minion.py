from card import Card

def minion_effect(player, game):
    player.actions += 1
    choice = player.choose_options(
        ["+2 Coins",
         "Discard your hand, +4 Cards, and each other player with 5+ cards discards and draws 4"],
        "Minion - choose one:")[0]

    if choice == "+2 Coins":
        player.coins += 2
        return

    targets = game.attack_targets(player)
    player.discard_pile.extend(player.hand)
    player.hand = []
    player.draw_cards(4)
    print(f"{player.name} discards their hand and draws 4.")
    for other in targets:
        if len(other.hand) >= 5:
            other.discard_pile.extend(other.hand)
            other.hand = []
            other.draw_cards(4)
            print(f"{other.name} discards their hand and draws 4.")

Minion = Card(
    "Minion",
    cost=5,
    card_type=["Action", "Attack"],
    description="+1 Action. Choose one: +2 Coins; or discard your hand, +4 Cards, and each other player with at least 5 cards in hand discards their hand and draws 4 cards.",
    effect=minion_effect,
    expansion="intrigue"
)
