from floptimizer.common.http import MethodNotAllowed
from floptimizer.api_clients.abstract.resources import APIError

HTTP_METHODS = [
    'HEAD',
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
]


class APIMethod:

    def __init__(self, method='GET', required_data=[], required_params=[],
                 required_json=[], auth_required=True, return_json=True,
                 required_path=[]):
        method = method.upper()
        if method in HTTP_METHODS:
            self.method = method
        else:
            raise ValueError('Invalid HTTP method specified.')
        self.required_data = required_data
        self.required_params = required_params
        self.required_json = required_json
        self.auth_required = auth_required
        self.return_json = return_json
        self.required_path = required_path


class APIEndpoint:

    def __init__(self, route, methods=[APIMethod(), ]):
        if type(methods) != list:
            raise ValueError('Methods parameter must be of type list.')
        if not all([type(m) == APIMethod for m in methods]):
            raise ValueError('Methods list items must be of type APIMethod')

        self.allowed_methods = {}
        for m in methods:
            self.allowed_methods[m.method] = m
        self.methods = methods
        self.route = route

        if len(set(self.allowed_methods.keys())) != len(methods):
            raise ValueError('May only use each HTTP Method once.')

    def get_route(self, **kwargs):

        return self.route.format(**kwargs)

    def is_valid_request(self, method, data=None, params=None, p_json=None, path=None):
        method = method.upper()
        if method not in self.allowed_methods:
            raise MethodNotAllowed(
                'The method {} is not allowed for the route {}.\n'
                'Alowed method(s) are: {}'.format(
                    method, self.route, ', '.join(self.allowed_methods.keys())
                )
            )
            return False
        m = self.allowed_methods[method]

        if m.required_data:
            if data is None or not all(
                [x in data for x in m.required_data]
            ):
                raise APIError(
                    'Required data is missing. Required data includes:'
                    '{}. You provided {}.'.format(m.required_data, data.keys())
                )
                return False

        if m.required_params:
            if params is None or not all(
                [x in params.keys() for x in m.required_params]
            ):

                raise APIError(
                    'Required params are missing. Required params include: '
                    '{}. You provided {}.'.format(m.required_params, params.keys())
                )
                return False

        if m.required_json:
            if json is None or not all(
                [x in p_json for x in m.required_json]
            ):
                raise APIError(
                    'Required json is missing. Required json include: '
                    '{}. You provided {}.'.format(m.required_json, p_json.keys())
                )
                return False

        if m.required_path:
            if path is None or not all(
                [x in path for x in m.required_path]
            ):
                raise APIError(
                    'Required path is missing. Required path include: '
                    '{}. You provided {}.'.format(m.required_path, path)
                )
                return False

        return True

    # def get(self, )
