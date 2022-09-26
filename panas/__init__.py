from otree.api import *


doc = """
PANAS (positive and negative affect schedule)
"""


class C(BaseConstants):
    NAME_IN_URL = 'panas'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    FIELDS = [
        'interested',
        'distressed',
        'excited',
        'upset',
        'strong',
        'guilty',
        'scared',
        'hostile',
        'enthusiastic',
        'proud',
        'irritable',
        'alert',
        'ashamed',
        'inspired',
        'nervous',
        'determined',
        'attentive',
        'jittery',
        'active',
        'afraid',
    ]
    POSITIVE_FIELDS = [
        'interested',
        'excited',
        'strong',
        'enthusiastic',
        'proud',
        'alert',
        'inspired',
        'determined',
        'attentive',
        'active',
    ]
    NEGATIVE_FIELDS = [
        'distressed',
        'upset',
        'guilty',
        'scared',
        'hostile',
        'irritable',
        'ashamed',
        'nervous',
        'jittery',
        'afraid',
    ]

    # make sure each field is counted exactly once
    assert sorted(FIELDS) == sorted(POSITIVE_FIELDS + NEGATIVE_FIELDS)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_q(label):
    return models.IntegerField(label=label, choices=[1, 2, 3, 4, 5], widget=widgets.RadioSelect)


class Player(BasePlayer):
    interested = make_q('Interested')
    distressed = make_q('Distressed')
    excited = make_q('Excited')
    upset = make_q('Upset')
    strong = make_q('Strong')
    guilty = make_q('Guilty')
    scared = make_q('Scared')
    hostile = make_q('Hostile')
    enthusiastic = make_q('Enthusiastic')
    proud = make_q('Proud')
    irritable = make_q('Irritable')
    alert = make_q('Alert')
    ashamed = make_q('Ashamed')
    inspired = make_q('Inspired')
    nervous = make_q('Nervous')
    determined = make_q('Determined')
    attentive = make_q('Attentive')
    jittery = make_q('Jittery')
    active = make_q('Active')
    afraid = make_q('Afraid')

    positive_affect_score = models.IntegerField()
    negative_affect_score = models.IntegerField()


# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = C.FIELDS

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.positive_affect_score = sum(getattr(player, f) for f in C.POSITIVE_FIELDS)
        player.negative_affect_score = sum(getattr(player, f) for f in C.NEGATIVE_FIELDS)


class Results(Page):
    pass


page_sequence = [Survey, Results]
