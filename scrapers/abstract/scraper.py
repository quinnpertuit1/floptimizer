from abc import ABC
from floptimizer.common.http import HTTPHandler
from bs4 import BeautifulSoup


class Scraper(ABC):

    def __init__(self):
        self.http = HTTPHandler()
