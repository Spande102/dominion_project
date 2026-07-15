from card import Card

def ambassador_effect(player, game):
    if not player.hand:
        print("No cards in hand to reveal.")
        return
    revealed = player.choose_card_from(
        player.hand, "Reveal a card from your hand:", optional=False)
    copies = sum(1 for c in player.hand if c.name == revealed.name)
    pile_name = game.find_supply_pile(revealed.name)

    options = ["Return 0 copies", "Return 1 copy"]
    if copies >= 2:
        options.append("Return 2 copies")
    choice = player.choose_options(options, f"Return copies of {revealed.name} to the Supply:")[0]
    count = int(choice.split()[1])

    if pile_name is None and count > 0:
        print(f"{revealed.name} has no Supply pile - none returned.")
        count = 0
    for _ in range(count):
        copy = next(c for c in player.hand if c.name == revealed.name)
        player.hand.remove(copy)
        game.supply[pile_name].append(copy)
    if count:
        print(f"{player.name} returns {count} {revealed.name}(s) to the Supply.")

    for other in game.attack_targets(player):
        if pile_name and game.supply[pile_name]:
            if other.gain_card(game, pile_name):
                print(f"{other.name} gains a {revealed.name}.")

Ambassador = Card(
    "Ambassador",
    cost=3,
    card_type=["Action", "Attack"],
    description="Reveal a card from your hand. Return up to 2 copies of it from your hand to the Supply. Then each other player gains a copy of it.",
    effect=ambassador_effect,
    expansion="seaside_1st_edition"
)
