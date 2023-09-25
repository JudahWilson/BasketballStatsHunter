from Game import Game
from Action import Action

game = Game('https://www.basketball-reference.com/boxscores/pbp/202104210DAL.html')

import pyperclip
pyperclip.copy(str(game))
print(game)

# for play in game.plays:
#     print(play)
#     for player in play.players:
#         if not player is None:
#             pass
#             #print(player.player_id)
#     print('--')

# db.connection.close()
breakpoint()
breakpoint()