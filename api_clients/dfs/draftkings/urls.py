
class Urls:

    def __init__(self):

        self._base_url = 'https://api.draftkings.com/'
        self._www_base_url = 'https://www.draftkings.com/'

        self.get_sports_path = (
            self._base_url + 'sites/US-DK/sports/v1/sports?format=json'
        )

        self.get_my_info_path = (
            self._base_url +
            'sites/US-DK/dashes/v1/dashes/siteNav/users/me.json'
            '?format=json&includeTickets=true'
        )

        self.get_sport_contests_path = (
            self._www_base_url + 'lobby/getcontests'
        )

        self.get_contests_details_format = (
            self._base_url + 'contests/v1/contests/{}?format=json'
        )

        self.authenticate_path = (
            self._base_url + 'users/v3/providers/draftkings/logins?format=json'
        )

        self.verify_location_path = (
            self._www_base_url + 'geocompliance/verifylocation'
        )

        self.account_path = (
            self._www_base_url + 'account'
        )

        self.addresses_path = (
            self._base_url + 'addresses/v1/users/'
            '{guid}/addresses?format=json&count=20'
        )

        self.withdrawal_path = (
            self._base_url + 'wallets/v1/users/'
            '{guid}/emailWithdrawals'
        )

        self.delete_withdrawal_path = (
            self._base_url + 'wallets/v1/withdrawals/'
            '{withdrawal_id}?format=json'
        )

        self.get_players_for_group_csv_path = (
            self._www_base_url + 'bulklineup/getdraftablecsv'
        )

        self.get_draftable_for_group_json_path = (
            self._base_url + 'draftgroups/v1/'
            'draftgroups/{gid}/draftables?format=json'
        )

        self.upload_file_path = (
            self._www_base_url + 'bulklineup/uploadfile'
        )

        self.get_my_lineups_path = (
            self._base_url + 'lineups/v1/users/'
            '{guid}/lineups?format=json&embed=entries'
        )

        self.get_players_for_group_json_path = (
            self._www_base_url + 'lineup/getplayersforcontestsignature'
        )

        self.get_draftgroup_info_path = (
            self._base_url + 'draftgroups/v1/{gid}?format=json'
        )

        self.get_contests_for_sport = (
            self._www_base_url + 'lobby/getcontests'
        )
