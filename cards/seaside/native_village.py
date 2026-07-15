from card import Card

def native_village_effect(player, game):
    player.actions += 2
    choice = player.choose_options(
        ["Put the top card of your deck on your Native Village mat",
         "Put all cards from your mat into your hand"],
        "Native Village - choose one:")[0]
    if choice.startswith("Put the top"):
        card = player.draw_cards(1, return_card=True)
        if card:
            player.native_village_mat.append(card)
            print(f"{player.name}'s mat now holds {len(player.native_village_mat)} card(s).")
    else:
        player.hand.extend(player.native_village_mat)
        print(f"{player.name} takes {len(player.native_village_mat)} card(s) from the mat.")
        player.native_village_mat = []

Native_Village = Card(
    "Native Village",
    cost=2,
    card_type=["Action"],
    description="+2 Actions. Choose one: Put the top card of your deck face down on your Native Village mat; or put all the cards from your mat into your hand.",
    effect=native_village_effect,
    expansion="seaside"
)
