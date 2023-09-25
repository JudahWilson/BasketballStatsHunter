class Instance_Player_Game():
    def __init__(self, url):
        self.player_id = url.split('/')[-1].replace('.html', '')
        self.team_id = ''
        self.game_id = ''

    def __str__(self):
        # return self.firstname + ' ' + self.lastname
        return self.player_id