from card import Card

def crystal_ball_effect(player, game):
    player.buys += 1
    top = player.draw_cards(1, return_card=True)
    if top:
        print(f"Top of your deck: {top.name}")
        # Simplification: the official "play it" option for Actions/Treasures
        # is not implemented.
        choice = player.choose_options(
            ["Put it back", "Discard it", "Trash it"], f"Crystal Ball - {top.name}:")[0]
        if choice == "Trash it":
            game.trash_pile.append(top)
            print(f"{player.name} trashes {top.name}.")
        elif choice == "Discard it":
            player.discard_pile.append(top)
            print(f"{player.name} discards {top.name}.")
        else:
            player.topdeck(top)
    return 1

Crystal_Ball = Card(
    "Crystal Ball",
    cost=5,
    card_type=["Treasure"],
    description="+1 Coin +1 Buy. Look at the top card of your deck. You may trash it, discard it, or put it back.",
    effect=crystal_ball_effect,
    expansion="prosperity"
)
