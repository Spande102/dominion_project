from card import Card

def swindler_effect(player, game):
    player.coins += 2
    for other in game.attack_targets(player):
        top = other.draw_cards(1, return_card=True)
        if not top:
            print(f"{other.name} has no cards to reveal.")
            continue
        game.trash_pile.append(top)
        print(f"{other.name} trashes {top.name} from the top of their deck.")

        cost = game.card_cost(top)
        pile_name = player.choose_supply_pile(
            game, f"Choose a card costing {cost} for {other.name} to gain:",
            predicate=lambda c: game.card_cost(c) == cost, optional=False)
        gained = other.gain_card(game, pile_name)
        if gained:
            print(f"{other.name} gains {gained.name}.")

Swindler = Card(
    "Swindler",
    cost=3,
    card_type=["Action", "Attack"],
    description="+2 Coins. Each other player trashes the top card of their deck and gains a card with the same cost that you choose.",
    effect=swindler_effect,
    expansion="intrigue"
)
