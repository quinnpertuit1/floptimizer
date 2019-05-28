from abc import ABC, abstractmethod


class Player(ABC):

    def __init__(self, *args, **kwargs):
        self.competition = kwargs.get('competition', None)
        self.display_name = kwargs.get('displayName', None)
        self.draft_alerts = kwargs.get('draftAlerts', None)
        self.draft_stat_attributes = kwargs.get('draftStatAttributes', None)
        self.draftable_id = kwargs.get('draftableId', None)
        self.first_name = kwargs.get('firstName', None)
        self.is_disabled = kwargs.get('isDisabled', None)
        self.is_swappable = kwargs.get('isSwappable', None)
        self.last_name = kwargs.get('lastName', None)
        self.news_status = kwargs.get('newsStatus', None)
        self.player_attributes = kwargs.get('playerAttributes', None)
        self.player_game_attributes = kwargs.get('playerGameAttributes', None)
        self.player_game_hash = kwargs.get('playerGameHash', None)
        self.player_id = kwargs.get('playerId', None)
        self.position = kwargs.get('position', None)
        self.roster_slot_id = kwargs.get('rosterSlotId', None)
        self.salary = kwargs.get('salary', 0)
        self.short_name = kwargs.get('shortName', None)
        self.status = kwargs.get('status', None)
        self.team_abbreviation = kwargs.get('teamAbbreviation', None)
        self.team_id = kwargs.get('teamId', None)
        self.ppg_id = None
        self.ppg = self.get_ppg()
        self.projection = 0

    def position_map(self, pos=None):
        return self.pos_map[pos] if pos is not None else self.pos_map

    def get_ppg(self):
        for att in self.draft_stat_attributes:
            if att['id'] == self.ppg_id:
                return att['val']

    def __str__(self):
        return '{}'.format(self.display_name)

    def __repr__(self):
        return self.__str__()


class NFLPlayer(Player):

    def __init__(self, **kwargs):
        super(NFLPlayer, self).__init__(kwargs)


class MLBPlayer(Player):

    def __init__(self, **kwargs):
        super(MLBPlayer, self).__init__(**kwargs)
        self.in_starting_lineup = False
        self.ppg_id = 408
        self.pos_map = {
            110: 'P',       # classic
            111: 'C',       # classic
            112: '1B',      # classic
            113: '2B',      # classic
            114: '3B',      # classic
            115: 'SS',      # classic
            116: 'OF',      # classic
            278: 'T1',      # tiers
            279: 'T2',      # tiers
            280: 'T3',      # tiers
            281: 'T4',      # tiers
            282: 'T5',      # tiers
            283: 'T6',      # tiers
            573: 'C',       # showdown
            574: 'UTIL',    # showdown
        }
        for att in self.player_game_attributes:
            if att['id'] == 130:
                self.in_starting_lineup = att['value']
            elif att['id'] == 112:
                self.opp_pitcher = att['value']


class NBAPlayer(Player):

    def __init__(self, *args, **kwargs):
        super(NBAPlayer, self).__init__(*args, **kwargs)
        self.ppg_id = 219
        self.position_map = {
            415: 'T1',      # tiers
            416: 'T2',      # tiers
            417: 'T3',      # tiers
            418: 'T4',      # tiers
            419: 'T5',      # tiers
            420: 'T6',      # tiers
            458: 'PG',      # classic
            459: 'SG',      # classic
            460: 'SF',      # classic
            461: 'PF',      # classic
            462: 'C',       # classic
            463: 'G',       # classic
            464: 'F',       # classic
            465: 'UTIL',    # classic
            475: 'C',       # showdown captain mode
            476: 'UTIL',    # showdown captain mode
            569: 'C',       # in-game showdown (h2)
            570: 'UTIL',    # in-game showdown (h2)
            571: 'C',       # in-game showdown (q4)
            572: 'UTIL',    # in-game showdown (q4)
        }


class GOLFPlayer(Player):

    def __init__(self, **kwargs):
        super(GOLFPlayer, self).__init__()
        self.ppg_id = 795
        self.position_map = {
            118: 'G',
        }


class NHLPlayer(Player):

    def __init__(self, **kwargs):
        super(NHLPlayer, self).__init__()
        self.position_map = {
            483: 'FLEX',  # showdown
        }


class NASPlayer(Player):

    def __init__(self, **kwargs):
        super(NASPlayer, self).__init__()
        self.position_map = {
            92: 'D',  # showdown
        }


class AFLPlayer(Player):

    def __init__(self, **kwargs):
        super(AFLPlayer, self).__init__()


class CFBPlayer(Player):

    def __init__(self, **kwargs):
        super(CFBPlayer, self).__init__()


class SOCPlayer(Player):

    def __init__(self, **kwargs):
        super(SOCPlayer, self).__init__()
        self.position_map = {
            119: 'GK',
            120: 'D',
            121: 'M',
            122: 'F',
            123: 'UTIL',
        }


class CBBPlayer(Player):

    def __init__(self, **kwargs):
        super(CBBPlayer, self).__init__()


class TENPlayer(Player):

    def __init__(self, **kwargs):
        super(TENPlayer, self).__init__()
        self.position_map = {
            492: 'P',  # showdown
        }


class MMAPlayer(Player):

    def __init__(self, **kwargs):
        super(MMAPlayer, self).__init__()
        self.position_map = {
            129: 'F',
        }


class ELPlayer(Player):

    def __init__(self, **kwargs):
        super(ELPlayer, self).__init__()


class LOLPlayer(Player):

    def __init__(self, **kwargs):
        super(LOLPlayer, self).__init__()
        self.position_map = {
            559: 'FLEX',
            560: 'TOP',
            561: 'JNG',
            562: 'MID',
            563: 'ADC',
            564: 'SUC',
            565: 'TEAM',
        }


class CFLPlayer(Player):

    def __init__(self, **kwargs):
        super(CFLPlayer, self).__init__()
