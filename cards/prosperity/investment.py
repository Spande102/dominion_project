from card import Card

def investment_effect(player, game):
    if player.hand:
        card = player.choose_card_from(player.hand, "Trash a card from your hand:", optional=False)
        player.hand.remove(card)
        game.trash_pile.append(card)
        print(f"{player.name} trashes {card.name}.")

    choice = player.choose_options(
        ["+1 Coin", "Trash this for +1 VP per differently named Treasure you have"],
        "Investment - choose one:")[0]
    if choice == "+1 Coin":
        player.coins += 1
    else:
        this = next((c for c in player.in_play if c.name == "Investment"), None)
        if this:
            player.in_play.remove(this)
            game.trash_pile.append(this)
        names = {c.name for c in player.all_cards() if "Treasure" in c.card_type}
        player.victory_tokens += len(names)
        print(f"{player.name} trashes Investment for +{len(names)} VP.")

Investment = Card(
    "Investment",
    cost=4,
    card_type=["Action"],
    description="Trash a card from your hand. Choose one: +1 Coin; or trash this, and if you did, +1 VP per differently named Treasure you have.",
    effect=investment_effect,
    expansion="prosperity"
)
