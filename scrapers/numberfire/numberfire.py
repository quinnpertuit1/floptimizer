from floptimizer.scrapers.abstract.scraper import Scraper

NUMBERFIRE_CONFIG = {
    'nfl': {
        'base_route': 'nfl/',
    },
    'nba': {
        'base_route': 'nba/',
    },
    'mlb': {
        'base_route': 'mlb/',
    },
    'nhl': {
        'base_route': 'nhl/',
    },
    'golf': {
        'base_route': 'golf/',
    },
    'nas': {
        'base_route': 'nascar/',
    },
    'cfb': {
        'base_route': 'ncaaf/',
    },
    'cbb': {
        'base_route': 'ncaab/',
    },
}


class NumberfireSport:

    def __init__(self, base_url, name, **kwargs):
        self.name = name
        self.base_path = base_url + kwargs.get('base_route', None)

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return self.__str__()


class Numberfire(Scraper):

    def __init__(self):
        self.base_url = 'https://www.numberfire.com/'
        self.current_url = None
        self.dfs_sites = {
            'fanduel': 3,
            'draftkings': 4,
            'yahoo': 13
        }
        self._sports = []
        self.load_sports()

    def load_sports(self):
        for sport in NUMBERFIRE_CONFIG:
            s = NumberfireSport(self.base_url, sport, **NUMBERFIRE_CONFIG[sport])
            setattr(self, sport, s)
            self._sports.append(s)

    @property
    def sports(self):
        return self._sports
