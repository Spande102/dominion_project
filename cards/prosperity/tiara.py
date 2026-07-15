from card import Card

def tiara_effect(player, game):
    player.buys += 1
    # The topdeck-gained-cards option is handled in Game.resolve_on_buy
    # (simplified: buys only, not all gains).
    treasures = [c for c in player.hand if "Treasure" in c.card_type]
    if treasures:
        card = player.choose_card_from(
            treasures, "You may play a Treasure from your hand twice:")
        if card:
            player.hand.remove(card)
            player.in_play.append(card)
            for _ in range(2):
                value = card.effect(player, game) if card.effect else 0
                player.coins += value or 0
            print(f"{player.name} plays {card.name} twice (coins={player.coins}).")
    return 0

Tiara = Card(
    "Tiara",
    cost=4,
    card_type=["Treasure"],
    description="+1 Buy. This turn, when you gain a card, you may put it onto your deck. You may play a Treasure from your hand twice.",
    effect=tiara_effect,
    expansion="prosperity"
)
