import time

from otree.api import *


doc = """
Scheduling players to start at a certain time (part 1: grouping app)
"""


class C(BaseConstants):
    NAME_IN_URL = 'scheduling'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    GRACE_MINUTES = 5


class Subsession(BaseSubsession):
    pass


def group_by_arrival_time_method(subsession: Subsession, waiting_players):
    # the eligible players are the ones whose booking time has come.
    # they stay eligible for a few minutes.
    # players can also get grouped even if this is not their official time,
    # but they get lower priority than the grouped players.
    now = time.time()
    # filter out players who booked a later slot
    eligible_players = [p for p in waiting_players if p.participant.booking_time < now]
    expected_players = []
    # stand-by players are the ones whose time already passed, but they did not get grouped,
    # either because they arrived late and missed it, or not enough other people showed up
    standby_players = []
    for p in eligible_players:
        if p.participant.booking_time > now - C.GRACE_MINUTES * 60:
            expected_players.append(p)
        else:
            standby_players.append(p)
    prioritized_players = expected_players + standby_players
    if len(prioritized_players) >= C.PLAYERS_PER_GROUP:
        return prioritized_players[: C.PLAYERS_PER_GROUP]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class GroupingWaitPage(WaitPage):
    group_by_arrival_time = True


class MyPage(Page):
    pass


page_sequence = [GroupingWaitPage, MyPage]
