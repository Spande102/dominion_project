from card import Card

def duke_vp(player):
    all_cards = player.deck + player.hand + player.discard_pile + player.in_play
    return sum(1 for card in all_cards if card.name == "Duchy")

Duke = Card(
    "Duke",
    cost = 5,
    card_type = "Victory",
    description = "Worth 1 VP per Duchy you have",
    expansion = "intrigue"
)
Duke.get_victory_points = duke_vp