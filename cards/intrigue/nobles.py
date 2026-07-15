from card import Card

def nobles_effect(player, game):
    choice = player.choose_options(
        ["+3 Cards", "+2 Actions"], "Nobles - choose one:")[0]
    if choice == "+3 Cards":
        player.draw_cards(3)
    else:
        player.actions += 2

def nobles_vp(player=None):
    return 2

Nobles = Card(
    "Nobles",
    cost=6,
    card_type=["Action", "Victory"],
    description="Choose one: +3 Cards; or +2 Actions. | 2 VP",
    effect=nobles_effect,
    expansion="intrigue"
)
Nobles.get_victory_points = nobles_vp
