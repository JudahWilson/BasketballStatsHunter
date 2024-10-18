import PlayByPlays.GamePlayer as GamePlayer

ACTIONS = {
    "ASSIST": 1,
    "BLOCK": 2,
    "BLOCKING_FOUL_COMMIT": 3,
    "BLOCKING_FOUL_DRAW": 4,
    "DEFENSIVE_REBOUND": 5,
    "DEFENSIVE_REBOUND_BY_TEAM": 6,
    "DUNK_MAKE": 7,
    "DUNK_MISS": 8,
    "ENTER_THE_GAME": 9,
    "FLAGRANT_FOUL_TYPE_1_DRAW": 10,
    "FLAGRANT_FOUL_TYPE_1": 11,
    "FREE_THROW_MAKE": 12,
    "FREE_THROW_MISS": 13,
    "FULL_TIMEOUT": 14,
    "HOOK_SHOT_MISS": 15,
    "HOOK_SHOT_MAKE": 16,
    "INSTANT_REPLY": 17,
    "INSTANT_REPLY_RULING_DOES_NOT_STAND": 18,
    "INSTANT_REPLY_RULING_STANDS": 19,
    "JUMP_BALL": 20,
    "GAIN_POSSESION_JUMP_BALL": 21,
    "KICK_BALL": 22,
    "LAYUP_MAKE": 23,
    "LAYUP_MISS": 24,
    "LEAVE_THE_GAME": 25,
    "LOOSE_BALL_FOUL_COMMIT": 26,
    "LOOSE_BALL_FOUL_DRAW": 27,
    "OFFENSIVE_FOUL_COMMIT": 28,
    "OFFENSIVE_FOUL_DRAW": 29,
    "OFFENSIVE_REBOUND": 30,
    "OFFENSIVE_REBOUND_BY_TEAM": 31,
    "PERSONAL_FOUL_COMMIT": 32,
    "PERSONAL_FOUL_DRAW": 33,
    "SHOOTING_FOUL_COMMIT": 34,
    "SHOOTING_FOUL_DRAW": 35,
    "STEAL": 36,
    "TECHNICAL_FOUL": 37,
    "THREE_POINT_JUMPSHOT_MAKE": 38,
    "THREE_POINT_JUMPSHOT_MISS": 39,
    "TURNOVER_BAD_PASS": 40,
    "TURNOVER_LOST_BALL": 41,
    "TURNOVER_SHOT_CLOCK_VIOLATION": 42,
    "TWENTY_SECOND_TIMEOUT": 43,
    "TWO_POINT_JUMPSHOT_MAKE": 44,
    "TWO_POINT_JUMPSHOT_MISS": 45,
}


class PlayAction:
    # Every play type
    # - the name must be the same as the value
    # - there must not be any other static attributes than play types

    # region "Actions"
    ASSIST = "ASSIST"
    BLOCK = "BLOCK"
    BLOCKING_FOUL_COMMIT = "BLOCKING_FOUL_COMMIT"
    BLOCKING_FOUL_DRAW = "BLOCKING_FOUL_DRAW"
    DEFENSIVE_REBOUND = "DEFENSIVE_REBOUND"
    DEFENSIVE_REBOUND_BY_TEAM = "DEFENSIVE_REBOUND_BY_TEAM"
    DUNK_MAKE = "DUNK_MAKE"
    DUNK_MISS = "DUNK_MISS"
    ENTER_THE_GAME = "ENTER_THE_GAME"
    FLAGRANT_FOUL_TYPE_1_DRAW = "FLAGRANT_FOUL_TYPE_1_DRAW"
    FLAGRANT_FOUL_TYPE_1 = "FLAGRANT_FOUL_TYPE_1"
    FREE_THROW_MAKE = "FREE_THROW_MAKE"
    FREE_THROW_MISS = "FREE_THROW_MISS"
    FULL_TIMEOUT = "FULL_TIMEOUT"
    HOOK_SHOT_MISS = "HOOK_SHOT_MISS"
    HOOK_SHOT_MAKE = "HOOK_SHOT_MAKE"
    INSTANT_REPLY = "INSTANT_REPLY"
    INSTANT_REPLY_RULING_DOES_NOT_STAND = "INSTANT_REPLY_RULING_DOES_NOT_STAND"
    INSTANT_REPLY_RULING_STANDS = "INSTANT_REPLY_RULING_STANDS"
    JUMP_BALL = "JUMP_BALL"
    GAIN_POSSESION_JUMP_BALL = "GAIN_POSSESION_JUMP_BALL"
    KICK_BALL = "KICK_BALL"
    LAYUP_MAKE = "LAYUP_MAKE"
    LAYUP_MISS = "LAYUP_MISS"
    LEAVE_THE_GAME = "LEAVE_THE_GAME"
    LOOSE_BALL_FOUL_COMMIT = "LOOSE_BALL_FOUL_COMMIT"
    LOOSE_BALL_FOUL_DRAW = "LOOSE_BALL_FOUL_DRAW"
    OFFENSIVE_FOUL_COMMIT = "OFFENSIVE_FOUL_COMMIT"
    OFFENSIVE_FOUL_DRAW = "OFFENSIVE_FOUL_DRAW"
    OFFENSIVE_REBOUND = "OFFENSIVE_REBOUND"
    OFFENSIVE_REBOUND_BY_TEAM = "OFFENSIVE_REBOUND_BY_TEAM"
    PERSONAL_FOUL_COMMIT = "PERSONAL_FOUL_COMMIT"
    PERSONAL_FOUL_DRAW = "PERSONAL_FOUL_DRAW"
    SHOOTING_FOUL_COMMIT = "SHOOTING_FOUL_COMMIT"
    SHOOTING_FOUL_DRAW = "SHOOTING_FOUL_DRAW"
    STEAL = "STEAL"
    TECHNICAL_FOUL = "TECHNICAL_FOUL"
    THREE_POINT_JUMPSHOT_MAKE = "THREE_POINT_JUMPSHOT_MAKE"
    THREE_POINT_JUMPSHOT_MISS = "THREE_POINT_JUMPSHOT_MISS"
    TURNOVER_BAD_PASS = "TURNOVER_BAD_PASS"
    TURNOVER_LOST_BALL = "TURNOVER_LOST_BALL"
    TURNOVER_SHOT_CLOCK_VIOLATION = "TURNOVER_SHOT_CLOCK_VIOLATION"
    TWENTY_SECOND_TIMEOUT = "TWENTY_SECOND_TIMEOUT"
    TWO_POINT_JUMPSHOT_MAKE = "TWO_POINT_JUMPSHOT_MAKE"
    TWO_POINT_JUMPSHOT_MISS = "TWO_POINT_JUMPSHOT_MISS"
    # endregion

    def __init__(self, action, player=None, team=None, distance_feet=None):
        self._player = None

        self.team = team
        self.player = player
        self.action = action
        self.distance_feet = distance_feet
        
        # DB fields, not initialized yet 
        self.player_br_id = None
        self.team_br_id = None
        self.action_code = None
        
    def __str__(self):
        if self.player:
            string = str(self.player) + " " + self.action
            if self.distance_feet:
                string += " at " + str(self.distance_feet) + " feet"
        elif not self.team is None:
            string = str(self.team) + " " + self.action
        else:
            string = "Error processing as string " + str(self.__dict__)

        return string

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, p):
        if p is None:
            self._player = None
        elif isinstance(p, GamePlayer):
            self._player = p
            self.player_br_id = p.player_br_id
        else:
            raise TypeError(
                "player must be set using a Player object"
            )
