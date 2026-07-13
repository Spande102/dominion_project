from card import Card

def thief_effect(player, game):
    for other in game.attack_targets(player):
        # Reveal the top 2 cards of the other player's deck
        revealed = other.draw_cards(2, return_card=True)
        if not revealed:
            print(f"{other.name} has no cards to reveal.")
            continue
        print(f"{other.name} revealed: {[card.name for card in revealed]}")

        treasures = [card for card in revealed if "Treasure" in card.card_type]
        if treasures:
            # The attacker chooses one revealed Treasure to trash
            if len(treasures) > 1:
                to_trash = player.choose_card_from(
                    treasures, f"Choose one of {other.name}'s Treasures to trash:", optional=False)
            else:
                to_trash = treasures[0]
            revealed.remove(to_trash)
            game.trash_pile.append(to_trash)
            print(f"{to_trash.name} from {other.name}'s deck is trashed.")

            # The attacker may gain the trashed card
            if player.confirm(f"Do you want to gain {to_trash.name}?"):
                game.trash_pile.remove(to_trash)
                player.discard_pile.append(to_trash)
                print(f"{player.name} gains {to_trash.name}.")

        # Discard the rest of the revealed cards
        other.discard_pile.extend(revealed)
        if revealed:
            print(f"{other.name} discards: {[card.name for card in revealed]}")


Thief = Card(
    "Thief",
    cost=4,
    card_type=['Action', 'Attack'],
    description="Each other player reveals the top 2 cards of their deck. If they revealed any Treasure cards, they trash one of them that you choose. You may gain any or all of these trashed cards. They discard the other revealed cards.",
    effect=thief_effect,
    expansion="base_1st_edition"
)
