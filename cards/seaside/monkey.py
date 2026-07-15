from card import Card

def monkey_effect(player, game):
    right = game.player_to_right(player)

    def listener(gainer, card):
        if gainer is right:
            player.draw_cards(1)
            print(f"{player.name} draws a card (Monkey watches {right.name}).")
    game.gain_listeners.append(listener)

    def next_turn(pl, g):
        if listener in g.gain_listeners:
            g.gain_listeners.remove(listener)
        pl.draw_cards(1)
        print(f"{pl.name} draws a card (Monkey).")
    player.add_duration("Monkey", next_turn)

Monkey = Card(
    "Monkey",
    cost=3,
    card_type=["Action", "Duration"],
    description="Until your next turn, when the player to your right gains a card, +1 Card. At the start of your next turn, +1 Card.",
    effect=monkey_effect,
    expansion="seaside"
)
