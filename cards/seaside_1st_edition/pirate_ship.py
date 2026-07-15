from card import Card

def pirate_ship_effect(player, game):
    choice = player.choose_options(
        ["Attack: each other player reveals top 2, trashes a Treasure you choose",
         f"+1 Coin per Coin token ({player.pirate_ship_tokens})"],
        "Pirate Ship - choose one:")[0]

    if choice.startswith("+1 Coin"):
        player.coins += player.pirate_ship_tokens
        print(f"{player.name} gets +{player.pirate_ship_tokens} Coins.")
        return

    trashed_any = False
    for other in game.attack_targets(player):
        revealed = other.draw_cards(2, return_card=True)
        if not revealed:
            continue
        print(f"{other.name} reveals: {[c.name for c in revealed]}")
        treasures = [c for c in revealed if "Treasure" in c.card_type]
        if treasures:
            if len(treasures) > 1:
                to_trash = player.choose_card_from(
                    treasures, f"Choose {other.name}'s Treasure to trash:", optional=False)
            else:
                to_trash = treasures[0]
            revealed.remove(to_trash)
            game.trash_pile.append(to_trash)
            trashed_any = True
            print(f"{other.name}'s {to_trash.name} is trashed.")
        other.discard_pile.extend(revealed)
    if trashed_any:
        player.pirate_ship_tokens += 1
        print(f"{player.name} takes a Coin token ({player.pirate_ship_tokens} total).")

Pirate_Ship = Card(
    "Pirate Ship",
    cost=4,
    card_type=["Action", "Attack"],
    description="Choose one: Each other player reveals the top 2 cards of their deck, trashes one Treasure you choose, and discards the rest; if anyone trashed a Treasure, you take a Coin token. Or: +1 Coin per Coin token you've taken with Pirate Ships.",
    effect=pirate_ship_effect,
    expansion="seaside_1st_edition"
)
