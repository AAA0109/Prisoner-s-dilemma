import csv
import math

from otree.api import *

doc = """
Social Value Orientation (Murphy et al)
"""


def read_csv():
    with open('svo/SVO.csv', encoding='utf-8-sig') as f:
        return [
            dict(
                round_number=int(row['round_number']),
                to_self=int(row['to_self']),
                to_other=int(row['to_other']),
            )
            for row in csv.DictReader(f)
        ]


def group_rows():
    from collections import defaultdict

    d = defaultdict(list)
    for row in read_csv():
        round_number = row['round_number']
        d[round_number].append(row)
    return d


class C(BaseConstants):
    NAME_IN_URL = 'svo'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 15  # change to 15 for the full task
    CHART_TEMPLATE = 'svo/chart.html'
    INSTRUCTIONS_TEMPLATE = 'svo/instructions.html'
    ROWS = group_rows()


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    choice = models.IntegerField(choices=list(range(9)))
    angle = models.FloatField()
    category = models.StringField()


def assign_category(angle):
    if angle > 57.15:
        return 'Altruistic'
    if angle > 22.45:
        return 'Prosocial'
    if angle > -12.04:
        return 'Individualistic'
    return 'Competitive'


class Decide(Page):
    form_model = 'player'
    form_fields = ['choice']

    @staticmethod
    def js_vars(player: Player):
        return dict(rows=C.ROWS[player.round_number])


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant

        to_self_total = 0
        to_other_total = 0
        for p in player.in_all_rounds():
            row = C.ROWS[p.round_number][p.choice]
            to_self_total += row['to_self']
            to_other_total += row['to_other']

        avg_self = to_self_total / C.NUM_ROUNDS
        avg_other = to_other_total / C.NUM_ROUNDS
        radians = math.atan((avg_other - 50) / (avg_self - 50))
        participant.svo_angle = round(math.degrees(radians), 2)
        participant.svo_category = assign_category(participant.svo_angle)


page_sequence = [Decide, Results]
