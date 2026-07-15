from card import Card

def mill_effect(player, game):
    player.draw_cards(1)
    player.actions += 1
    if len(player.hand) >= 2 and player.confirm("Discard 2 cards for +2 Coins?"):
        to_discard = player.choose_cards_from(
            player.hand, "Choose 2 cards to discard:", min_count=2, max_count=2)
        for card in to_discard:
            player.hand.remove(card)
            player.discard_pile.append(card)
        player.coins += 2
        print(f"{player.name} discards 2 cards for +2 Coins.")

def mill_vp(player=None):
    return 1

Mill = Card(
    "Mill",
    cost=4,
    card_type=["Action", "Victory"],
    description="+1 Card +1 Action. You may discard 2 cards, for +2 Coins. | 1 VP",
    effect=mill_effect,
    expansion="intrigue"
)
Mill.get_victory_points = mill_vp
