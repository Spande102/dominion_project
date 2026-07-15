from card import Card

def scrying_pool_effect(player, game):
    player.actions += 1
    # Spy part: each player (you first) reveals their top card; you choose
    # discard or put back
    targets = [player] + game.attack_targets(player)
    for target in targets:
        revealed = target.draw_cards(1, return_card=True)
        if not revealed:
            continue
        print(f"{target.name} reveals {revealed.name}.")
        if player.confirm(f"Discard {target.name}'s revealed {revealed.name}?"):
            target.discard_pile.append(revealed)
        else:
            target.topdeck(revealed)

    # Then reveal cards from your deck until a non-Action; take them all
    taken = []
    while True:
        card = player.draw_cards(1, return_card=True)
        if card is None:
            break
        taken.append(card)
        if "Action" not in card.card_type:
            break
    player.hand.extend(taken)
    if taken:
        print(f"{player.name} takes into hand: {[c.name for c in taken]}")

Scrying_Pool = Card(
    "Scrying Pool",
    cost=2,
    potion_cost=1,
    card_type=["Action", "Attack"],
    description="+1 Action. Each player (including you) reveals the top card of their deck and either discards it or puts it back, your choice. Then reveal cards from your deck until revealing one that isn't an Action. Put all of those revealed cards into your hand.",
    effect=scrying_pool_effect,
    expansion="alchemy"
)
