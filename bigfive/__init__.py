from otree.api import *

doc = """Big 5 personality test"""


class C(BaseConstants):
    NAME_IN_URL = 'bigfive'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_q(label):
    return models.IntegerField(label=label, choices=[1, 2, 3, 4, 5], widget=widgets.RadioSelect)


class Player(BasePlayer):
    q1 = make_q('is reserved')
    q2 = make_q('is generally trusting')
    q3 = make_q('tends to be lazy')
    q4 = make_q('is relaxed, handles stress well')
    q5 = make_q('has few artistic interests')
    q6 = make_q('is outgoing, sociable')
    q7 = make_q('tends to find fault with others')
    q8 = make_q('does a thorough job')
    q9 = make_q('gets nervous easily')
    q10 = make_q('has an active imagination')

    extraversion = models.FloatField()
    agreeableness = models.FloatField()
    conscientiousness = models.FloatField()
    neuroticism = models.FloatField()
    openness = models.FloatField()


def combine_score(positive, negative):
    return 3 + (positive - negative) / 2


class Survey(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.extraversion = combine_score(player.q6, player.q1)
        player.agreeableness = combine_score(player.q2, player.q7)
        player.conscientiousness = combine_score(player.q8, player.q3)
        player.neuroticism = combine_score(player.q9, player.q4)
        player.openness = combine_score(player.q10, player.q5)


class Results(Page):
    pass


page_sequence = [Survey, Results]
