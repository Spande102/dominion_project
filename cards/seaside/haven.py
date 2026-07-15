from card import Card

def haven_effect(player, game):
    player.draw_cards(1)
    player.actions += 1
    if not player.hand:
        return
    card = player.choose_card_from(
        player.hand, "Set aside a card (to your hand next turn):", optional=False)
    player.hand.remove(card)
    player.set_aside.append(card)

    def next_turn(pl, g):
        if card in pl.set_aside:
            pl.set_aside.remove(card)
            pl.hand.append(card)
            print(f"{pl.name} takes the Haven card into hand.")
    player.add_duration("Haven", next_turn)

Haven = Card(
    "Haven",
    cost=2,
    card_type=["Action", "Duration"],
    description="+1 Card +1 Action. Set aside a card from your hand face down. At the start of your next turn, put it into your hand.",
    effect=haven_effect,
    expansion="seaside"
)
