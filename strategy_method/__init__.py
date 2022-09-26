from otree.api import *

doc = """
Strategy method for ultimatum game.
"""


class C(BaseConstants):
    NAME_IN_URL = 'strategy_method'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    INSTRUCTIONS_FILE = __name__ + '/instructions.html'
    ENDOWMENT = cu(100)
    OFFER_CHOICES = currency_range(0, ENDOWMENT, 10)
    OFFER_CHOICES_COUNT = len(OFFER_CHOICES)

    POSSIBLE_ALLOCATIONS = []
    for OFFER in OFFER_CHOICES:
        POSSIBLE_ALLOCATIONS.append(dict(p1_amount=OFFER, p2_amount=ENDOWMENT - OFFER))


class Subsession(BaseSubsession):
    pass


def make_strategy_field(number):
    return models.BooleanField(
        label="Would you accept an offer of {}?".format(cu(number)),
        widget=widgets.RadioSelectHorizontal,
        # note to self: remove this once i release bugfix
        choices=[[False, 'No'], [True, 'Yes']],
    )


class Group(BaseGroup):
    amount_offered = models.CurrencyField(choices=C.OFFER_CHOICES,)
    offer_accepted = models.BooleanField()
    # another way to implement this game would be with an ExtraModel, instead of making
    # all these hardcoded fields.
    # that's what the choice_list app does.
    # that would be more flexible, but also more complex since you would have to implement the
    # formfields yourself with HTML and Javascript.
    # in this case, since the rules of the game are pretty simple,
    # and there are not too many fields,
    # just defining these hardcoded fields is fine.
    response_0 = make_strategy_field(0)
    response_10 = make_strategy_field(10)
    response_20 = make_strategy_field(20)
    response_30 = make_strategy_field(30)
    response_40 = make_strategy_field(40)
    response_50 = make_strategy_field(50)
    response_60 = make_strategy_field(60)
    response_70 = make_strategy_field(70)
    response_80 = make_strategy_field(80)
    response_90 = make_strategy_field(90)
    response_100 = make_strategy_field(100)


def set_payoffs(group: Group):
    p1, p2 = group.get_players()
    amount_offered = group.amount_offered
    group.offer_accepted = getattr(group, 'response_{}'.format(int(amount_offered)))
    if group.offer_accepted:
        p1.payoff = C.ENDOWMENT - amount_offered
        p2.payoff = amount_offered
    else:
        p1.payoff = 0
        p2.payoff = 0


class Player(BasePlayer):
    pass


class P1(Page):
    form_model = 'group'
    form_fields = ['amount_offered']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class P2(Page):
    form_model = 'group'
    form_fields = ['response_{}'.format(int(i)) for i in C.OFFER_CHOICES]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
    title_text = "Thank you"
    body_text = (
        "You can close this page. When the other player arrives, the payoff will be calculated."
    )


class Results(Page):
    pass


page_sequence = [
    P1,
    P2,
    ResultsWaitPage,
    Results,
]
