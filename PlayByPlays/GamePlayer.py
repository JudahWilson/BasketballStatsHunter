class GamePlayer:
    def __init__(self, url_or_br_id: str):
        if url_or_br_id.startswith("https"):
            self.player_br_id = url_or_br_id.split("/")[-1].replace(".html", "")
        else:
            self.player_br_id = url_or_br_id

    def __str__(self):
        # return self.firstname + ' ' + self.lastname
        return self.player_br_id
