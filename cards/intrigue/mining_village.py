from card import Card

def mining_village_effect(player, game):
    player.draw_cards(1)
    player.actions += 2
    if player.confirm("Trash Mining Village for +2 Coins?"):
        trashed = player.trash_card("Mining Village", game, zone="in_play")
        if trashed:
            player.coins += 2

Mining_Village = Card(
    "Mining Village",
    cost=4,
    card_type=["Action"],
    description="+1 Card +2 Actions. You may trash this for +2 Coins.",
    effect=mining_village_effect,
    expansion="intrigue"
)
