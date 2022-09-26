from otree.api import *

doc = """
Choice list (Holt/Laury, risk preferences, price list, equivalence test, etc)
"""


class C(BaseConstants):
    NAME_IN_URL = 'choice_list'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    TABLE_TEMPLATE = __name__ + '/table.html'


def read_csv():
    import csv
    import random

    f = open(__name__ + '/stimuli.csv', encoding='utf-8-sig')
    rows = list(csv.DictReader(f))

    random.shuffle(rows)
    return rows


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        stimuli = read_csv()
        for stim in stimuli:
            # In python, ** unpacks a dict.
            Trial.create(player=p, **stim)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    chose_lottery = models.BooleanField()
    won_lottery = models.BooleanField()


class Trial(ExtraModel):
    player = models.Link(Player)
    sure_payoff = models.CurrencyField()
    lottery_high = models.CurrencyField()
    lottery_low = models.CurrencyField()
    probability_percent = models.IntegerField()
    chose_lottery = models.BooleanField()
    is_selected = models.BooleanField(initial=False)


# PAGES
class Stimuli(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(trials=Trial.filter(player=player), is_results=False)

    @staticmethod
    def live_method(player: Player, data):
        # In this case, Trial.filter() will return a list with just 1 item.
        # so we use python 'iterable unpacking' to assign that single item
        # to the variable 'trial'.
        [trial] = Trial.filter(player=player, id=data['trial_id'])
        trial.chose_lottery = data['chose_lottery']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random

        # if your page has a timeout, you would need to adjust this code.
        trials = Trial.filter(player=player)
        selected_trial = random.choice(trials)
        selected_trial.is_selected = True
        player.chose_lottery = selected_trial.chose_lottery
        if player.chose_lottery:
            player.won_lottery = selected_trial.probability_percent > (random.random() * 100)
            if player.won_lottery:
                payoff = selected_trial.lottery_high
            else:
                payoff = selected_trial.lottery_low
        else:
            payoff = selected_trial.sure_payoff
        player.payoff = payoff


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        trials = Trial.filter(player=player, is_selected=True)
        return dict(trials=trials, is_results=True)


page_sequence = [Stimuli, Results]
