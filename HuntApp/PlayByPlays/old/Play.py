import PlayAction


class Play:
    def __init__(self, PlayActions, quarter, time, score, distance_feet):
        self._PlayActions = None
        self.PlayActions = PlayActions
        self.quarter = quarter
        self.time = time
        self.score = score
        self.distance_feet = distance_feet

    @property
    def PlayActions(self):
        return self._PlayActions

    @PlayActions.setter
    def PlayActions(self, p):
        if isinstance(p, list):
            for player in p:
                assert isinstance(
                    player, PlayAction
                ), "PlayActions must be set using a Action object or a list of PlayActions"
            self._PlayActions = p
        elif isinstance(p, PlayAction):
            self._PlayActions = [p]
        else:
            raise TypeError(
                "PlayActions must be set using a Action object or a list of PlayActions"
            )

    @property
    def points(self):
        for action in self._PlayActions:
            if action.action in [
                PlayAction.DUNK_MAKE,
                PlayAction.LAYUP_MAKE,
                PlayAction.TWO_POINT_JUMPSHOT_MAKE,
            ]:
                return 2
            elif action.action in [PlayAction.THREE_POINT_JUMPSHOT_MAKE]:
                return 3
            elif action.action in [PlayAction.FREE_THROW_MAKE]:
                return 1
            else:
                continue
        return 0

    @property
    def points_of_team(self, team):
        for action in self._PlayActions:
            if (
                action.action
                in [
                    PlayAction.DUNK_MAKE,
                    PlayAction.LAYUP_MAKE,
                    PlayAction.TWO_POINT_JUMPSHOT_MAKE,
                ]
                and action.player[0].team == team
            ):
                return 2
            elif (
                action.action in [PlayAction.THREE_POINT_JUMPSHOT_MAKE]
                and action.player[0].team == team
            ):
                return 3
            elif (
                action.action in [PlayAction.FREE_THROW_MAKE]
                and action.player[0].team == team
            ):
                return 1
            else:
                continue
        return 0

    def __str__(self):  # TEST with feet
        action_str_list = []
        for action in self.PlayActions:
            action_str_list.append(str(action))
        return "\n".join(action_str_list) + " " + str(self.__dict__)

    def __iter__(self):
        for action in self.PlayActions:
            yield str(action)

    @property
    def players(self):  # Players involved in a play
        player_list = []
        for action in self._PlayActions:
            if not action.player is None:
                for player in action.player:
                    if not player in player_list:
                        player_list.append(player)

        return player_list

    @property
    def teams(self):  # Involves both teams or just the one?
        team_list = []
        for action in self._PlayActions:
            for team in action.teams:
                if not team in team_list:
                    team_list.append(team)

        return team_list
