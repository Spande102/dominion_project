from card import Card

def replace_effect(player, game):
    if not player.hand:
        print("No cards in hand to trash.")
        return
    to_trash = player.choose_card_from(
        player.hand, "Choose a card to trash:", optional=False)
    player.hand.remove(to_trash)
    game.trash_pile.append(to_trash)
    print(f"{player.name} trashes {to_trash.name}.")

    max_cost = game.card_cost(to_trash) + 2
    pile_name = player.choose_supply_pile(
        game, f"Gain a card costing up to {max_cost}:",
        predicate=lambda c: game.card_cost(c) <= max_cost, optional=False)
    if not pile_name:
        return
    top = game.supply[pile_name][0]
    onto_deck = "Action" in top.card_type or "Treasure" in top.card_type
    gained = player.gain_card(game, pile_name, destination='deck' if onto_deck else 'discard')
    if not gained:
        return
    print(f"{player.name} gains {gained.name}" + (" onto their deck." if onto_deck else "."))
    if "Victory" in gained.card_type:
        for other in game.attack_targets(player):
            curse = other.gain_card(game, game.find_supply_pile("Curse"))
            if curse:
                print(f"{other.name} gains a Curse.")

Replace = Card(
    "Replace",
    cost=5,
    card_type=["Action", "Attack"],
    description="Trash a card from your hand. Gain a card costing up to 2 more than it. If the gained card is an Action or Treasure, put it onto your deck; if it's a Victory card, each other player gains a Curse.",
    effect=replace_effect,
    expansion="intrigue"
)
