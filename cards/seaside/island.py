from card import Card

def island_effect(player, game):
    this = next((c for c in player.in_play if c.name == "Island"), None)
    if this:
        player.in_play.remove(this)
        player.island_mat.append(this)
    if player.hand:
        card = player.choose_card_from(
            player.hand, "Put a card from your hand on the Island mat:", optional=False)
        player.hand.remove(card)
        player.island_mat.append(card)
        print(f"{player.name} sets aside {card.name} on the Island mat.")

def island_vp(player=None):
    return 2

Island = Card(
    "Island",
    cost=4,
    card_type=["Action", "Victory"],
    description="Put this and a card from your hand onto your Island mat (set aside until end of game). | 2 VP",
    effect=island_effect,
    expansion="seaside"
)
Island.get_victory_points = island_vp
