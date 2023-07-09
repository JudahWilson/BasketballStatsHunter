from Instance_Player_Game import Instance_Player_Game

class Action():
    # Every play type
    # - the name must be the same as the value
    # - there must not be any other static attributes than play types
    
    #region "Actions"
    ASSIST = 'ASSIST'
    BLOCK = 'BLOCK'
    BLOCKING_FOUL_COMMIT = 'BLOCKING_FOUL_COMMIT'
    BLOCKING_FOUL_DRAW = 'BLOCKING_FOUL_DRAW'
    DEFENSIVE_REBOUND = 'DEFENSIVE_REBOUND'
    DEFENSIVE_REBOUND_BY_TEAM = 'DEFENSIVE_REBOUND_BY_TEAM'
    DUNK_MAKE = 'DUNK_MAKE'
    DUNK_MISS = 'DUNK_MISS'
    ENTER_THE_GAME = 'ENTER_THE_GAME'
    FLAGRANT_FOUL_TYPE_1_DRAW = 'FLAGRANT_FOUL_TYPE_1_DRAW'
    FLAGRANT_FOUL_TYPE_1 = 'FLAGRANT_FOUL_TYPE_1'
    FREE_THROW_MAKE = 'FREE_THROW_MAKE'
    FREE_THROW_MISS = 'FREE_THROW_MISS'
    FULL_TIMEOUT = 'FULL_TIMEOUT'
    HOOK_SHOT_MISS = 'HOOK_SHOT_MISS'
    HOOK_SHOT_MAKE = 'HOOK_SHOT_MAKE'
    INSTANT_REPLY = 'INSTANT_REPLY'
    INSTANT_REPLY_RULING_DOES_NOT_STAND = 'INSTANT_REPLY_RULING_DOES_NOT_STAND'
    INSTANT_REPLY_RULING_STANDS = 'INSTANT_REPLY_RULING_STANDS'
    JUMP_BALL = 'JUMP_BALL'
    GAIN_POSSESION_JUMP_BALL = 'GAIN_POSSESION_JUMP_BALL'
    KICK_BALL = 'KICK_BALL'
    LAYUP_MAKE = 'LAYUP_MAKE'
    LAYUP_MISS = 'LAYUP_MISS'
    LEAVE_THE_GAME = 'LEAVE_THE_GAME'
    LOOSE_BALL_FOUL_COMMIT = 'LOOSE_BALL_FOUL_COMMIT'
    LOOSE_BALL_FOUL_DRAW = 'LOOSE_BALL_FOUL_DRAW'
    OFFENSIVE_FOUL_COMMIT = 'OFFENSIVE_FOUL_COMMIT'
    OFFENSIVE_FOUL_DRAW = 'OFFENSIVE_FOUL_DRAW'
    OFFENSIVE_REBOUND = 'OFFENSIVE_REBOUND'
    OFFENSIVE_REBOUND_BY_TEAM = 'OFFENSIVE_REBOUND_BY_TEAM'
    PERSONAL_FOUL_COMMIT = 'PERSONAL_FOUL_COMMIT'
    PERSONAL_FOUL_DRAW = 'PERSONAL_FOUL_DRAW'
    SHOOTING_FOUL_COMMIT = 'SHOOTING_FOUL_COMMIT'
    SHOOTING_FOUL_DRAW = 'SHOOTING_FOUL_DRAW'
    STEAL = 'STEAL'
    TECHNICAL_FOUL = 'TECHNICAL_FOUL'
    THREE_POINT_JUMPSHOT_MAKE = 'THREE_POINT_JUMPSHOT_MAKE'
    THREE_POINT_JUMPSHOT_MISS = 'THREE_POINT_JUMPSHOT_MISS'
    TURNOVER_BAD_PASS = 'TURNOVER_BAD_PASS'
    TURNOVER_LOST_BALL = 'TURNOVER_LOST_BALL'
    TURNOVER_SHOT_CLOCK_VIOLATION = 'TURNOVER_SHOT_CLOCK_VIOLATION'
    TWENTY_SECOND_TIMEOUT = 'TWENTY_SECOND_TIMEOUT'
    TWO_POINT_JUMPSHOT_MAKE = 'TWO_POINT_JUMPSHOT_MAKE'
    TWO_POINT_JUMPSHOT_MISS = 'TWO_POINT_JUMPSHOT_MISS'
    #endregion
    
    def all_action_types():
        """A list of all established actions involved in a play

        Returns:
            list: all possible actions
        """
        return [value for attr, value in Action.__dict__.items() if not callable(value) and not attr.startswith("__") and not isinstance(value, property)]
    
    def __init__(self, action, players=None, team=None, feet=None):
        self._players = None
        self.team = team
        self.players = players
        self.action = action
        self.feet = feet

    def __str__(self):
        str_players = []
        if self.players:
            for player in self.players:
                str_players.append(str(player))
            string = " & ".join(str_players) + ' ' + self.action
            if self.feet:
                string += ' at ' + str(self.feet) + ' feet'
        elif not self.team is None:
            string = str(self.team) + ' ' + self.action
        else:
            string = 'Error processing as string ' + str(self.__dict__)

        return string

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, p):
        if p is None:
            self._players = None
        elif isinstance(p, list):
            for player in p:
                assert (isinstance(player, Instance_Player_Game)), "players must be set using a Player object or a list of Players"
            self._players = p
        elif isinstance(p, Instance_Player_Game):
            self._players = [p]
        else:
            raise TypeError("players must be set using a Player object or a list of Players")