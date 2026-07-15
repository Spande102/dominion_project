from card import Card

def corsair_effect(player, game):
    player.coins += 2
    targets = game.attack_targets(player)
    hit = set()

    def listener(p, card):
        if p in targets and card.name in ("Silver", "Gold"):
            key = (id(p), p.turns_taken)
            if key not in hit:
                hit.add(key)
                if card in p.in_play:
                    p.in_play.remove(card)
                    game.trash_pile.append(card)
                    print(f"{p.name} trashes the played {card.name} (Corsair).")
    game.treasure_play_listeners.append(listener)

    def next_turn(pl, g):
        if listener in g.treasure_play_listeners:
            g.treasure_play_listeners.remove(listener)
        pl.coins += 2
        print(f"{pl.name} gets +2 Coins (Corsair).")
    player.add_duration("Corsair", next_turn)

Corsair = Card(
    "Corsair",
    cost=5,
    card_type=["Action", "Duration", "Attack"],
    description="+2 Coins. At the start of your next turn, +2 Coins. Until then, each other player trashes the first Silver or Gold they play each turn.",
    effect=corsair_effect,
    expansion="seaside"
)
