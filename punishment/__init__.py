from otree.api import *


doc = """
Public goods with punishment, roughly based on Fehr & Gaechter 2000. 
"""


class C(BaseConstants):
    NAME_IN_URL = 'punishment'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 3
    ENDOWMENT = cu(20)
    MULTIPLIER = 1.6
    MAX_PUNISHMENT = 10
    PUNISHMENT_SCHEDULE = {
        0: 0,
        1: 1,
        2: 2,
        3: 4,
        4: 6,
        5: 9,
        6: 12,
        7: 16,
        8: 20,
        9: 25,
        10: 30,
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


def make_punishment_field(id_in_group):
    return models.IntegerField(
        min=0, max=C.MAX_PUNISHMENT, label="Punishment to player {}".format(id_in_group)
    )


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=C.ENDOWMENT, label="How much will you contribute?"
    )
    punish_p1 = make_punishment_field(1)
    punish_p2 = make_punishment_field(2)
    punish_p3 = make_punishment_field(3)
    punish_p4 = make_punishment_field(4)
    cost_of_punishing = models.CurrencyField()
    punishment_received = models.CurrencyField()


def get_self_field(player: Player):
    return 'punish_p{}'.format(player.id_in_group)


def punishment_fields(player: Player):
    return ['punish_p{}'.format(p.id_in_group) for p in player.get_others_in_group()]


def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP

    for p in players:
        payoff_before_punishment = C.ENDOWMENT - p.contribution + group.individual_share
        self_field = get_self_field(p)
        punishments_received = [getattr(other, self_field) for other in p.get_others_in_group()]
        p.punishment_received = min(10, sum(punishments_received))
        punishments_sent = [getattr(p, field) for field in punishment_fields(p)]
        p.cost_of_punishing = sum(C.PUNISHMENT_SCHEDULE[points] for points in punishments_sent)
        p.payoff = payoff_before_punishment * (1 - p.punishment_received / 10) - p.cost_of_punishing


# PAGES
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class WaitPage1(WaitPage):
    pass


class Punish(Page):
    form_model = 'player'
    get_form_fields = punishment_fields

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            other_players=player.get_others_in_group(), schedule=C.PUNISHMENT_SCHEDULE.items(),
        )


class WaitPage2(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


page_sequence = [
    Contribute,
    WaitPage1,
    Punish,
    WaitPage2,
    Results,
]
