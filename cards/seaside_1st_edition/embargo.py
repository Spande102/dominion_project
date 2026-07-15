from card import Card

def embargo_effect(player, game):
    player.coins += 2
    this = next((c for c in player.in_play if c.name == "Embargo"), None)
    if this:
        player.in_play.remove(this)
        game.trash_pile.append(this)
    pile_name = player.choose_supply_pile(
        game, "Put an Embargo token on a Supply pile:", optional=False)
    if pile_name:
        game.embargo_tokens[pile_name] = game.embargo_tokens.get(pile_name, 0) + 1
        print(f"Embargo token on {pile_name} "
              f"({game.embargo_tokens[pile_name]} total).")

Embargo = Card(
    "Embargo",
    cost=2,
    card_type=["Action"],
    description="+2 Coins. Trash this. Put an Embargo token on a Supply pile. (When a player buys a card from that pile, they gain a Curse per token on it.)",
    effect=embargo_effect,
    expansion="seaside_1st_edition"
)
