from card import Card

def great_hall_effect(player, game):
    player.draw_cards(1)
    player.actions += 1

def great_hall_vp(player=None):
    return 1

Great_Hall = Card(
    "Great Hall",
    cost=3,
    card_type=["Action", "Victory"],
    description="+1 Card +1 Action. | 1 VP",
    effect=great_hall_effect,
    expansion="intrigue_1st_edition"
)
Great_Hall.get_victory_points = great_hall_vp
