from floptimizer.api_clients.abstract.resources import APIError


class APIClientError(APIError):

    def __init__(self, message=None):
        super(APIClientError, self).__init__(message)
