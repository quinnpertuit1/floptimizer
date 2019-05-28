import requests
from floptimizer.error import FloptimizerError


class HTTPHandler:

    def __init__(self):
        self.session = None

    def do_request(self, method, url, **kwargs):
        auth_required = kwargs.get('auth_required', False)
        if auth_required:
            del kwargs['auth_required']
            if self.session is None:
                self.create_session()
            return self.session.request(method, url, **kwargs)
        else:
            if self.session:
                return self.session.request(method, url, **kwargs)
            else:
                return requests.request(method, url, **kwargs)

    def create_session(self):
        self.session = requests.Session()

    def destroy_session(self):
        self.session = None


class MethodNotAllowed(FloptimizerError):
    pass
