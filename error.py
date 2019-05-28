
class FloptimizerError(Exception):

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        msg = 'No message given' if self.message is None else self.message
        return '{}'.format(msg)
