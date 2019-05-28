from abc import ABC, abstractmethod
from floptimizer.error import FloptimizerError
from floptimizer.common.http import HTTPHandler
import json


class APIError(FloptimizerError):

    def __init__(self, message=None):
        super(APIError, self).__init__(message)


class APIClient(ABC):

    def __init__(self):
        self.http = HTTPHandler()
        self.last_response = None
        self.authenticated = False

    @abstractmethod
    def authenticate(self):
        raise NotImplementedError

    def _request_wrapper(self, *args, **kwargs):
        http_method = args[0]
        api_endpoint = args[1]
        data = kwargs.get('data', None)
        params = kwargs.get('params', None)
        p_json = kwargs.get('json', None)
        path = kwargs.pop('path', {})

        if api_endpoint.is_valid_request(http_method, data, params, p_json, path):
            api_method = api_endpoint.allowed_methods[http_method]
            if api_method.auth_required:
                kwargs['auth_required'] = True
                authenticating = kwargs.pop('authenticating', False)

                if self.authenticated == False and not authenticating:
                    self.authenticate()

            r = self.http.do_request(
                http_method,
                api_endpoint.get_route(**path),
                **kwargs
            )
            self.last_response = r

            if api_method.return_json:
                try:
                    return json.loads(r.content)
                except ValueError:
                    raise APIError(
                        ('Error decoding json response. Check this last_response'
                         'for more information.')
                    )
            else:
                return r.content
        return None

    def _http_head(self, route, **kwargs):
        return self._request_wrapper("HEAD", route, kwargs)

    def _http_get(self, route, **kwargs):
        return self._request_wrapper("GET", route, **kwargs)

    def _http_post(self, route, **kwargs):
        return self._request_wrapper("POST", route, **kwargs)

    def _http_put(self, route, **kwargs):
        return self._request_wrapper("PUT", route, **kwargs)

    def _http_patch(self, route, **kwargs):
        return self._request_wrapper("PATCH", route, **kwargs)

    def _http_delete(self, route, **kwargs):
        return self._request_wrapper("DELETE", route, **kwargs)

    def _http_options(self, route, **kwargs):
        return self._request_wrapper("OPTIONS", route, **kwargs)
