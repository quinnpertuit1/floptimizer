import json

from floptimizer.api_clients.abstract.resources import APIClient
from floptimizer.api_clients.dfs.draftkings.contest import Contest
from floptimizer.api_clients.dfs.draftkings.endpoints import Endpoints
from floptimizer.api_clients.dfs.draftkings.error import DKAPIError
from floptimizer.api_clients.dfs.draftkings.settings import DKSettings
from floptimizer.api_clients.dfs.draftkings.sport import Sport


class DKAPIClient(APIClient):

    def __init__(self, preloads=None):
        super(DKAPIClient, self).__init__()
        self._settings = DKSettings()
        self._sports = None
        self._preloads = self._check_preloads(preloads)
        self._endpoints = Endpoints()
        self.username = self._settings.username
        self.password = self._settings.password

        # Load current sports data
        self.sports

    def _check_preloads(self, preloads):
        try:
            assert(type(preloads) in [str, list] if preloads else True)
            if preloads:
                if type(preloads) == str:
                    preloads = [preloads, ]
                preloads = list(map(lambda x: str(x).lower(), preloads))
            return preloads

        except AssertionError:
            raise DKAPIError(
                ('Incorrect preload type. '
                 'Should be either string or list of strings.')
            )

    def authenticate(self):
        if self.username is None:
            self.username = input('Enter your username: ')
        if self.password is None:
            self.password = input('Enter your password: ')

        post_data = {
            "login": self.username,
            "password": self.password,
            "host": "api.draftkings.com",
            "challengeResponse": {
                "solution": "",
                "type": "Recaptcha"}
        }

        self._http_post(
            self._endpoints.authenticate_route,
            json=post_data,
            authenticating=True
        )

    def _json_to_list(self, data_route, data_key, data_type,
                      data=None, params=None, json=None):
        tmp = []
        json_data = self._http_get(data_route, data=data, params=params,
                                   json=json).get(data_key, False)
        if json_data is not None:
            for data in json_data:
                o = data_type(**data)
                tmp.append(o)
        else:
            raise DKAPIError('Error retrieving data.')
        return tmp

    def get_contest_details(self, contest):
        contest.details = self._http_get(
            self.get_contest_details_route.format(contest.id)
        )

    def get_contests(self, sport, refresh=False, config=None):
        if sport.contests is not None and refresh == False:
            if refresh:
                sport.contests = None
            if not sport.contests:
                sport._all_contests = self._json_to_list(
                    self._endpoints.get_sports_contests_route,
                    'Contests',
                    Contest,
                    params={'sport': sport.short_name, 'format': 'json'}
                )
                sport._filtered_contests = sport._all_contests[::]

    def get_draft_group(self, dgroup):
        return self._http_get(
            self._endpoints.get_draftgroup_info_route,
            path={'gid': dgroup}
        )

    def get_players_for_group(self, dgroup):
        return self._http_get(
            self._endpoints.get_players_for_group_route,
            params={'draftGroupId': dgroup}
        )

    def get_draftable_for_group(self, dgroup):
        return self._http_get(
            self._endpoints.get_draftable_for_group_json,
            path={'gid': dgroup}
        )

    def load_players_for_draft_group(self, dgroup):
        data = self.get_draftable_for_group(dgroup)
        if not data['draftables']:
            raise DKAPIError(
                'This draft group exists but does not have a player pool yet. '
                'This is usually because the contest is in a reservation only '
                'status.'
            )
            return
        sport = data['competitions'][0]['sport'].lower()
        for p in data['draftables']:
            getattr(self, sport).add_player(dgroup, p)

    def _get_contests_factory(self, sport):
        return lambda: self.get_contests(sport)

    def _get_sports(self):
        self._sports = []
        sports_json = self._http_get(
            self._endpoints.get_sports_route
        ).get(
            'sports', False
        )
        if sports_json:
            for sport_json in sports_json:
                s = Sport(**sport_json)
                setattr(self, s.short_name.lower(), s)
                setattr(
                    getattr(self, s.short_name.lower()),
                    'get_contests',
                    self._get_contests_factory(s)
                )
                if self._preloads is not None:
                    if s.short_name.lower() in self._preloads:
                        self.get_contests(s)
                self._sports.append(s)
        else:
            raise DKAPIError('Error retrieving currently supported sports.')
        return self._sports

    @property
    def sports(self, refresh=False):
        if self._sports is not None:
            if refresh == False:
                return self._sports
        return self._get_sports()
