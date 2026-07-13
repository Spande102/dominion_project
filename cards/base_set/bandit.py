from card import Card

def bandit_effect(player, game):
    # Gain a Gold
    gold = player.gain_card(game, game.find_supply_pile("Gold"))
    if gold:
        print(f"{player.name} gains a Gold.")
    else:
        print("No Golds left to gain.")

    # Attack other players
    for other_player in game.attack_targets(player):
        # Reveal top 2 cards
        revealed = other_player.draw_cards(2, return_card=True)
        if not revealed:
            print(f"{other_player.name} has no cards to reveal.")
            continue
        print(f"{other_player.name} reveals: {[card.name for card in revealed]}")

        # Find non-Copper Treasures; the attacked player chooses which one to trash
        treasures = [card for card in revealed if "Treasure" in card.card_type and card.name != "Copper"]
        if treasures:
            if len(treasures) > 1:
                to_trash = other_player.choose_card_from(
                    treasures, f"{other_player.name}, choose a Treasure to trash:", optional=False)
            else:
                to_trash = treasures[0]
            revealed.remove(to_trash)
            game.trash_pile.append(to_trash)
            print(f"{other_player.name} trashes {to_trash.name}.")

        # Discard the rest
        for card in revealed:
            other_player.discard_pile.append(card)
            print(f"{other_player.name} discards {card.name}.")

Bandit = Card(
    "Bandit",
    cost=5,
    card_type=["Action", "Attack"],
    description="Gain a Gold. Each other player reveals the top 2 cards of their deck, trashes a non-Copper Treasure among them, and discards the rest.",
    effect=bandit_effect,
    expansion="base"
)