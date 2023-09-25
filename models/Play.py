from Action import Action

class Play():
    def __init__(self, actions, quarter, time, score):
        self._actions = None
        self.actions = actions
        self.quarter = quarter
        self.time = time
        self.score = score

    @property
    def actions(self):
        return self._actions

    @actions.setter
    def actions(self, p):
        if isinstance(p, list):
            for player in p:
                assert (isinstance(player, Action)), "actions must be set using a Action object or a list of Actions"
            self._actions = p
        elif isinstance(p, Action):
            self._actions = [p]
        else:
            raise TypeError("actions must be set using a Action object or a list of actions")

    @property
    def points(self):
        for action in self._actions:
            if action.action in [Action.DUNK_MAKE, Action.LAYUP_MAKE, Action.TWO_POINT_JUMPSHOT_MAKE]:
                return 2
            elif action.action in [Action.THREE_POINT_JUMPSHOT_MAKE]:
                return 3
            elif action.action in [Action.FREE_THROW_MAKE]:
                return 1
            else:
                continue
        return 0

    @property
    def points_of_team(self, team):
        for action in self._actions:
            if action.action in [Action.DUNK_MAKE, Action.LAYUP_MAKE, Action.TWO_POINT_JUMPSHOT_MAKE] \
                    and action.players[0].team == team:
                return 2
            elif action.action in [Action.THREE_POINT_JUMPSHOT_MAKE] \
                    and action.players[0].team == team:
                return 3
            elif action.action in [Action.FREE_THROW_MAKE] \
                    and action.players[0].team == team:
                return 1
            else:
                continue
        return 0

    def __str__(self):  # TEST with feet
        action_str_list = []
        for action in self.actions:
            action_str_list.append(str(action))
        return '\n'.join(action_str_list) + ' ' + str(self.__dict__)
    
    def __iter__(self):
        for action in self.actions:
            yield str(action)

    @property
    def players(self):  # Players involved in a play
        player_list = []
        for action in self._actions:
            if not action.players is None:
                for player in action.players:
                    if not player in player_list:
                        player_list.append(player)

        return player_list

    @property
    def teams(self):  # Involves both teams or just the one?
        team_list = []
        for action in self._actions:
            for team in action.teams:
                if not team in team_list:
                    team_list.append(team)

        return team_list