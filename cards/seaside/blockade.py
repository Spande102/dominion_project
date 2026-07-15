from card import Card

def blockade_effect(player, game):
    pile_name = player.choose_supply_pile(
        game, "Gain a card costing up to 4, setting it aside:",
        predicate=game.costs_at_most(4), optional=False)
    if not pile_name or not game.supply[pile_name]:
        return
    card = game.supply[pile_name].pop()
    player.set_aside.append(card)
    game.notify_gain(player, card)
    print(f"{player.name} sets aside a {card.name} (Blockade).")
    name = card.name

    def listener(gainer, gained):
        if gainer is not player and gained.name == name:
            if gainer.gain_card(game, game.find_supply_pile("Curse")):
                print(f"{gainer.name} gains a Curse (Blockade on {name}).")
    game.gain_listeners.append(listener)

    def next_turn(pl, g):
        if listener in g.gain_listeners:
            g.gain_listeners.remove(listener)
        if card in pl.set_aside:
            pl.set_aside.remove(card)
            pl.hand.append(card)
            print(f"{pl.name} takes the Blockade {card.name} into hand.")
    player.add_duration("Blockade", next_turn)

Blockade = Card(
    "Blockade",
    cost=4,
    card_type=["Action", "Duration", "Attack"],
    description="Gain a card costing up to 4, setting it aside. At the start of your next turn, put it into your hand. While it's set aside, when another player gains a copy of it on their turn, they gain a Curse.",
    effect=blockade_effect,
    expansion="seaside"
)
