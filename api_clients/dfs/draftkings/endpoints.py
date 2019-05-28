from .urls import Urls
from floptimizer.api_clients.common import APIMethod, APIEndpoint


class Endpoints:

    def __init__(self):

        self.urls = Urls()

        self.get_sports_route = APIEndpoint(
            self.urls.get_sports_path,
            [APIMethod(auth_required=False), ],
        )

        self.get_my_info_route = APIEndpoint(
            self.urls.get_my_info_path,
            [APIMethod(auth_required=False), ]
        )

        self.get_contest_details_route = APIEndpoint(
            self.urls.get_contests_details_format,
            [APIMethod(required_data=['sport', ], auth_required=False), ]
        )

        self.authenticate_route = APIEndpoint(
            self.urls.authenticate_path,
            [APIMethod(
                method='POST',
                required_params=[
                    'login', 'password', 'host',
                    {'challengeResponse': ['solution', 'type']}
                ],
            ), ]
        )

        # self.get_my_addresses = APIEndpoint(
        #    self.urls.addresses_path,
        # )

        # self.withdraw = APIEndpoint(
        #    self.urls.withdrawal_path,
        #    ['POST', ],
        #    True
        # )

        # self.cancel_withdrawal = APIEndpoint(
        #    self.urls.delete_withdrawal_path,
        #    ['DELETE', ],
        #    True
        # )

        self.get_players_for_group_csv = APIEndpoint(
            self.urls.get_players_for_group_csv_path,
            [APIMethod(
                method='POST',
                required_data=['draftGroupId'],
                auth_required=False,
            ), ]
        )

        self.get_draftable_for_group_json = APIEndpoint(
            self.urls.get_draftable_for_group_json_path,
            [APIMethod(
                required_path=['gid'],
                auth_required=False,
            ), ]
        )

        self.upload_csv = APIEndpoint(
            self.urls.upload_file_path,
            [APIMethod(
                method='POST',
                required_params=['fileUplaod']
            ), ]
        )

        self.get_my_lineups = APIEndpoint(
            self.urls.get_my_lineups_path,
            [APIMethod(), ],
        )

        self.get_players_for_group_route = APIEndpoint(
            self.urls.get_players_for_group_json_path,
            [APIMethod(required_params=['draftGroupId', ], auth_required=False)],
        )

        self.get_draftgroup_info_route = APIEndpoint(
            self.urls.get_draftgroup_info_path,
            [APIMethod(
                required_path=['gid'],
                auth_required=False,
            ), ]
        )

        self.account_route = APIEndpoint(
            self.urls.account_path,
            [APIMethod(), ]
        )

        self.get_sports_contests_route = APIEndpoint(
            self.urls.get_contests_for_sport,
            [APIMethod(required_params=['sport', ], auth_required=False)]
        )
