from floptimizer.api_clients.dfs.draftkings.error import DKAPIError
from floptimizer.api_clients.dfs.draftkings.players import (
    NFLPlayer,
    MLBPlayer,
    NBAPlayer,
    GOLFPlayer,
    NHLPlayer,
    NASPlayer,
    AFLPlayer,
    CFBPlayer,
    SOCPlayer,
    CBBPlayer,
    TENPlayer,
    MMAPlayer,
    ELPlayer,
    LOLPlayer,
    CFLPlayer,
)


SPORT_CONFIGS = {
    'Football': {'SHORT_NAME': 'NFL', 'PLAYER_MODEL': NFLPlayer},
    'Baseball': {'SHORT_NAME': 'MLB', 'PLAYER_MODEL': MLBPlayer},
    'Basketball': {'SHORT_NAME': 'NBA', 'PLAYER_MODEL': NBAPlayer},
    'Golf': {'SHORT_NAME': 'GOLF', 'PLAYER_MODEL': GOLFPlayer},
    'Hockey': {'SHORT_NAME': 'NHL', 'PLAYER_MODEL': NHLPlayer},
    'Nascar': {'SHORT_NAME': 'NAS', 'PLAYER_MODEL': NASPlayer},
    'Arena Football League': {'SHORT_NAME': 'AFL', 'PLAYER_MODEL': AFLPlayer},
    'College Football': {'SHORT_NAME': 'CFB', 'PLAYER_MODEL': CFBPlayer},
    'Soccer': {'SHORT_NAME': 'SOC', 'PLAYER_MODEL': SOCPlayer},
    'College Basketball': {'SHORT_NAME': 'CBB', 'PLAYER_MODEL': CBBPlayer},
    'Tennis': {'SHORT_NAME': 'TEN', 'PLAYER_MODEL': TENPlayer},
    'Mixed Martial Arts': {'SHORT_NAME': 'MMA', 'PLAYER_MODEL': MMAPlayer},
    'EuroLeague Basketball': {'SHORT_NAME': 'EL', 'PLAYER_MODEL': ELPlayer},
    'League of Legends': {'SHORT_NAME': 'LOL', 'PLAYER_MODEL': LOLPlayer},
    'Canadian Football': {'SHORT_NAME': 'CFL', 'PLAYER_MODEL': CFLPlayer},
}


class Sport:

    def __init__(self, **kwargs):
        self.full_name = kwargs.get('fullName', None)
        self.sport_id = kwargs.get('sportId', None)
        self.sort_order = kwargs.get('sortOrder', None)
        self.has_public_contests = kwargs.get('hasPublicContests', None)
        self.is_enabled = kwargs.get('isEnabled', None)
        self._all_contests = None
        self._filtered_contests = None
        self.players = {}

        try:
            self.short_name = SPORT_CONFIGS[self.full_name]['SHORT_NAME']
            self.player_model = SPORT_CONFIGS[self.full_name]['PLAYER_MODEL']
        except KeyError:
            raise DKAPIError(
                'The retrieved {} sport does not have a short_name.'.format(
                    self.full_name
                )
            )
        self._contest_filters = kwargs.get('contest_config', {})

    def name(self):
        return self.full_name

    @property
    def id(self):
        return self.sport_id

    def is_active(self):
        return self.is_enabled

    @property
    def contests(self):
        if self._filtered_contests:
            return self._filtered_contests
        else:
            return []

    def _filter_contests(self):
        if not self._all_contests:
            raise DKAPIError(
                'Either no contests have been loaded yet, '
                'or there are no contests currently active. '
                'Try the .get_contests() method.'
            )
        self._filtered_contests = list(filter(
            lambda c: c.passes_filter(
                self._contest_filters,
            ),
            [c for c in self._all_contests]
        ))

    @property
    def all_contests(self):
        return self._all_contests

    @all_contests.setter
    def all_contests(self, contest_list):
        try:
            assert(isinstance(contest_list, list))
        except AssertionError:
            raise DKAPIError(
                'Contests attribute of Sport must be a list of type Contest'
            )
        self._all_contests = contest_list[::]
        self._filtered_contests = contest_list[::]
        if self.contest_filters:
            self._filter_contests()

    @property
    def contest_filters(self):
        return self._contest_filters

    @contest_filters.setter
    def contest_filters(self, filter_dict):
        self._contest_filters = filter_dict
        self._filter_contests()

    def get_attr_wrapper(self, attr, c_list):
        return list(set([getattr(c, attr) for c in c_list]))

    def get_game_types(self):
        return self.get_attr_wrapper('game_type', self._filtered_contests)

    def get_all_game_types(self):
        return self.get_attr_wrapper('game_type', self._all_contests)

    def get_draft_groups(self):
        return self.get_attr_wrapper('draft_group', self._filtered_contests)

    def get_all_draft_groups(self):
        return self.get_attr_wrapper('draft_group', self._all_contests)

    def get_payouts(self):
        return self.get_attr_wrapper('payout', self._filtered_contests)

    def get_all_payouts(self):
        return self.get_attr_wrapper('payout', self._all_contests)

    def add_player(self, dgroup, data):
        p = self.player_model(**data)
        if dgroup not in self.players:
            self.players[dgroup] = {}

        pos = p.position_map(p.roster_slot_id)
        if pos not in self.players[dgroup]:
            self.players[dgroup][pos] = []
        self.players[dgroup][pos].append(p)

    def __str__(self):
        return '{}'.format(self.full_name)

    def __repr__(self):
        return self.__str__()
