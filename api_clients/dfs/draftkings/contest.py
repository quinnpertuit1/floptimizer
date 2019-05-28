class Contest:

    def __init__(self, **kwargs):

        self.my_entry_count = kwargs.get('ec', None)
        self.multi_entry_count = kwargs.get('mec', None)
        self.crown_awards = kwargs.get('fpp', None)
        self.contest_name = kwargs.get('n', None)
        self.is_guaranteed = kwargs.get('attr', {}).get('IsGuaranteed', False)
        self.is_starred = kwargs.get('attr', {}).get('IsStarred', False)
        self.is_league = kwargs.get('attr', {}).get('League', False)
        self.is_steps = kwargs.get('attr', {}).get('IsSteps', False)
        self.is_double_up = kwargs.get('attr', {}).get('IsDoubleUp', False)
        self.is_fiftyfifty = kwargs.get('attr', {}).get('IsFiftyfifty', False)
        self.is_winner_take_all = kwargs.get('attr', {}).get('IsWinnerTakeAll', False)
        self.is_beginner = kwargs.get('attr', {}).get('IsBeginner', False)
        self.is_casual = kwargs.get('attr', {}).get('IsCasual', False)
        self.multiplier = kwargs.get('attr', {}).get('Multiplier', False)
        self.is_qualifier = kwargs.get('attr', {}).get('IsQualifier', False)
        self.is_combinable = kwargs.get('attr', {}).get('IsCombinable', False)
        self.is_headliner = kwargs.get('attr', {}).get('IsHeadliner', False)
        self.lobby_class = kwargs.get('attr', {}).get('LobbyClass', None)
        self.is_nighttime = kwargs.get('attr', {}).get('IsNighttime', False)
        self.number_entries = kwargs.get('nt', None)
        self.max_entries = kwargs.get('m', None)
        self.payout = kwargs.get('po', None)
        self.payout_denomination = kwargs.get('pd', None)
        self.start_date_string = kwargs.get('sdstring')
        self.start_date_epoch = int(kwargs.get('sd', '(0)').split('(')[1].split(')')[0])
        self.contest_id = kwargs.get('id', None)
        self.free_with_ticket = kwargs.get('fwt', None)
        self.is_owner = kwargs.get('isOwner', None)
        self.start_time_type = kwargs.get('startTimeType', None)
        self.game_type = kwargs.get('gameType', None)
        self.free_with_crowns = kwargs.get('freeWithCrowns', None)
        self.crown_cost = kwargs.get('crownAmount', None)
        self.entry_fee = kwargs.get('a', None)
        self.game_template = kwargs.get('tmpl', None)
        self.draft_group = kwargs.get('dg', None)

        # currently unknown attrs
        self.uc = kwargs.get('uc', None)
        self.s = kwargs.get('s', None)
        self.tix = kwargs.get('tix', None)
        self.pt = kwargs.get('pt', None)
        self.so = kwargs.get('so', None)
        self.ulc = kwargs.get('ulc', None)
        self.cs = kwargs.get('cs', None)
        self.ssd = kwargs.get('ssd', None)
        self.dgpo = kwargs.get('dgpo', None)
        self.cso = kwargs.get('cso', None)
        self.ir = kwargs.get('ir', None)
        self.rl = kwargs.get('rl', None)
        self.rlc = kwargs.get('rlc', None)
        self.rll = kwargs.get('rll', None)
        self.sa = kwargs.get('sa', None)

        self._details = None

        self.get_contest_details_route = kwargs.get(
            'getContestDetailsRoute',
            None
        )

    @property
    def details(self, data):
        return self._details

    @details.setter
    def details(self, data):
        self._details = data

    def _check_gte(self, val, eq, lt, gt):
        val = getattr(self, val)
        if eq:
            return val == eq
        if lt and gt:
            return gt < val < lt
        if lt:
            return val < lt
        if gt:
            return gt < val
        return True

    def _check_name(self, eq, contain):
        cn = self.contest_name.lower().strip()
        if eq:
            return cn == eq.lower().strip()
        if contain:
            return contain.lower().strip() in cn
        return True

    def _check_denom(self, denom):
        if denom:
            denoms = [
                x.lower().strip() for x in self.payout_denomination.keys()
            ]
            return denom.lower().strip() in denoms
        return True

    def _check_contest_id(self, contest_id):
        if contest_id:
            # throw type error on bad cast
            return int(contest_id) == self.contest_id
        return True

    def _check_game_type(self, g_type):
        if g_type:
            g_type = g_type.lower().strip()
            if type(g_type) == list:
                return self.game_type.lower().strip() in [
                    x.lower().strip() for x in g_type
                ]
            else:
                return self.game_type.lower().strip() == g_type
        return True

    def _check_game_template(self, template):
        if template:
            return int(self.game_template) == int(template)
        return True

    def _check_draft_group(self, group):
        if group:
            return int(self.draft_group) == int(group)
        return True

    def passes_filter(self, filter_params):
        gte_vals = [
            'my_entry_count',
            'multi_entry_count',
            'crown_awards',
            'number_entries',
            'max_entries',
            'payout',
            'start_date_epoch',
            'crown_cost',
            'entry_fee',
        ]
        for val in gte_vals:
            if not self._check_gte(
                val,
                filter_params.get('{}_eq'.format(val), None),
                filter_params.get('{}_lt'.format(val), None),
                filter_params.get('{}_gt'.format(val), None),
            ):
                return False

        if not self._check_name(
            filter_params.get('contest_name_eq', None),
            filter_params.get('contest_name_contains', None),
        ):
            return False

        if not self._check_denom(filter_params.get('payout_denomination', None)):
            return False

        if not self._check_contest_id(filter_params.get('contest_id', None)):
            return False

        if not self._check_game_type(filter_params.get('game_type', None)):
            return False

        if not self._check_game_template(filter_params.get('game_template', None)):
            return False

        if not self._check_draft_group(filter_params.get('draft_group', None)):
            return False

        return True

    def __str__(self):
        return '{}'.format(self.contest_name)

    def __repr__(self):
        return self.__str__()
