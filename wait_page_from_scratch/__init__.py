from otree.api import *
from json import dumps as json_dumps, loads as json_loads

doc = """
Wait page implemented from scratch, using live pages.
"""


class C(BaseConstants):
    NAME_IN_URL = 'wait_page_from_scratch'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # json fields
    wait_for_ids = models.LongStringField(initial='[]')
    arrived_ids = models.LongStringField(initial='[]')


def unarrived_players(group: Group):
    return set(json_loads(group.wait_for_ids)) - set(json_loads(group.arrived_ids))


class Player(BasePlayer):
    pass


class Intro(Page):
    pass


def wait_page_live_method(player: Player, data):
    group = player.group

    arrived_ids_set = set(json_loads(group.arrived_ids))
    arrived_ids_set.add(player.id_in_subsession)
    group.arrived_ids = json_dumps(list(arrived_ids_set))

    if not unarrived_players(group):
        return {0: dict(finished=True)}


class ScratchWaitPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        # first time
        if not json_loads(group.wait_for_ids):
            wait_for_ids = [p.id_in_subsession for p in group.get_players()]
            group.wait_for_ids = json_dumps(wait_for_ids)
        return unarrived_players(group)

    @staticmethod
    def live_method(player: Player, data):
        if data.get('type') == 'wait_page':
            return wait_page_live_method(player, data)

    @staticmethod
    def error_message(player: Player, values):
        group = player.group
        if unarrived_players(group):
            return "Wait page not finished"


class Results(Page):
    pass


page_sequence = [Intro, ScratchWaitPage, Results]
