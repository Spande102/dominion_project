from card import Card

def kings_court_effect(player, game):
    action_cards = [c for c in player.hand if "Action" in c.card_type]
    if not action_cards:
        print("No Action cards to play with King's Court.")
        return
    chosen = player.choose_card_from(
        action_cards, "Choose an Action to play three times (0 to skip):")
    if chosen is None:
        return
    player.hand.remove(chosen)
    player.in_play.append(chosen)
    player.turn_state.actions_played += 3
    print(f"{player.name} plays {chosen.name} three times.")
    if chosen.effect:
        for _ in range(3):
            chosen.effect(player, game)

Kings_Court = Card(
    "King's Court",
    cost=7,
    card_type=["Action"],
    description="You may play an Action card from your hand three times.",
    effect=kings_court_effect,
    expansion="prosperity"
)
