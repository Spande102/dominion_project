from card import Card

def courtier_effect(player, game):
    if not player.hand:
        print("No cards in hand to reveal.")
        return
    revealed = player.choose_card_from(
        player.hand, "Reveal a card from your hand:", optional=False)
    count = min(len(revealed.card_type), 4)
    print(f"{player.name} reveals {revealed.name} ({count} type(s)).")

    chosen = player.choose_options(
        ["+3 Coins", "+1 Action", "+1 Buy", "Gain a Gold"],
        f"Courtier - choose {count} different:", count=count)
    for option in chosen:
        if option == "+1 Action":
            player.actions += 1
        elif option == "+1 Buy":
            player.buys += 1
        elif option == "+3 Coins":
            player.coins += 3
        elif option == "Gain a Gold":
            gained = player.gain_card(game, game.find_supply_pile("Gold"))
            if gained:
                print(f"{player.name} gains a Gold.")

Courtier = Card(
    "Courtier",
    cost=5,
    card_type=["Action"],
    description="Reveal a card from your hand. For each type it has (Action, Attack, etc.), choose one: +1 Action; or +1 Buy; or +3 Coins; or gain a Gold. The choices must be different.",
    effect=courtier_effect,
    expansion="intrigue"
)
