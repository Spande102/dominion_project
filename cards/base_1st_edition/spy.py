from card import Card

def spy_effect(player, game):
    player.draw_cards(1)
    player.actions += 1

    # Each player (including the Spy's owner) reveals their top card;
    # the attacker decides whether it is discarded or put back.
    targets = [player] + game.attack_targets(player)
    for target_player in targets:
        revealed_card = target_player.draw_cards(1, return_card=True)
        if not revealed_card:
            print(f"{target_player.name} has no cards to reveal.")
            continue

        print(f"{target_player.name} revealed {revealed_card.name}.")
        if player.confirm(f"Discard {target_player.name}'s revealed card ({revealed_card.name})?"):
            target_player.discard_pile.append(revealed_card)
            print(f"{target_player.name}'s card was discarded.")
        else:
            target_player.topdeck(revealed_card)
            print(f"{target_player.name}'s card remains on top of their deck.")


Spy = Card(
    "Spy",
    cost=4,
    card_type=['Action', 'Attack'],
    description="+1 Card +1 Action. Each player (including you) reveals the top card of their deck and either discards it or puts it back, your choice.",
    effect=spy_effect,
    expansion="base_1st_edition"
)
