from card import Card

def saboteur_effect(player, game):
    for other in game.attack_targets(player):
        revealed_junk = []
        found = None
        while True:
            card = other.draw_cards(1, return_card=True)
            if card is None:
                break
            if game.card_cost(card) >= 3:
                found = card
                break
            revealed_junk.append(card)
        other.discard_pile.extend(revealed_junk)

        if not found:
            print(f"{other.name} reveals their whole deck with nothing costing 3 or more.")
            continue

        game.trash_pile.append(found)
        print(f"{other.name} trashes {found.name}.")
        max_cost = game.card_cost(found) - 2
        pile_name = other.choose_supply_pile(
            game, f"{other.name}, you may gain a card costing up to {max_cost}:",
            predicate=lambda c: game.card_cost(c) <= max_cost, optional=True)
        gained = other.gain_card(game, pile_name)
        if gained:
            print(f"{other.name} gains {gained.name}.")

Saboteur = Card(
    "Saboteur",
    cost=5,
    card_type=["Action", "Attack"],
    description="Each other player reveals cards from the top of their deck until revealing one costing 3 or more. They trash that card and may gain a card costing at most 2 less than it. They discard the other revealed cards.",
    effect=saboteur_effect,
    expansion="intrigue_1st_edition"
)
