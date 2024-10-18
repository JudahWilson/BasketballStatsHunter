from PlayByPlays.Game import Game
from PlayByPlays.PlayAction import PlayAction


game = Game("202104210DAL")
game.init_plays()

print(game)

for play in game.plays:
    print(play)
    for player in play.players:
        if not player is None:
            pass
            # print(player.player_id)
    print("--")


breakpoint()
breakpoint()
