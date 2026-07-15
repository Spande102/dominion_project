from card import Card

def lurker_effect(player, game):
    player.actions += 1
    choice = player.choose_options(
        ["Trash an Action card from the Supply",
         "Gain an Action card from the trash"],
        "Lurker - choose one:")[0]

    if choice.startswith("Trash"):
        pile_name = player.choose_supply_pile(
            game, "Trash an Action card from the Supply:",
            predicate=lambda c: "Action" in c.card_type, optional=False)
        if pile_name and game.supply[pile_name]:
            card = game.supply[pile_name].pop()
            game.trash_pile.append(card)
            print(f"{player.name} trashes {card.name} from the Supply.")
    else:
        actions_in_trash = [c for c in game.trash_pile if "Action" in c.card_type]
        if not actions_in_trash:
            print("No Action cards in the trash.")
            return
        card = player.choose_card_from(
            actions_in_trash, "Gain an Action card from the trash:", optional=False)
        game.trash_pile.remove(card)
        player.discard_pile.append(card)
        print(f"{player.name} gains {card.name} from the trash.")

Lurker = Card(
    "Lurker",
    cost=2,
    card_type=["Action"],
    description="+1 Action. Choose one: Trash an Action card from the Supply, or gain an Action card from the trash.",
    effect=lurker_effect,
    expansion="intrigue"
)
