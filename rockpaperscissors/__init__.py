from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'rockpaperscissors'
    HISTORY_TEMPLATE = 'rockpaperscissors/history.html'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    CHOICES = ['Rock', 'Paper', 'Scissors']


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    is_draw = models.BooleanField()


class Player(BasePlayer):
    hand = models.StringField(choices=C.CHOICES)
    opponent_hand = models.StringField()
    result = models.StringField()


def set_winner(player: Player):
    [opponent] = player.get_others_in_group()
    if player.hand == opponent.hand:
        player.result = 'Draw'
    elif player.hand + opponent.hand in 'ScissorsPaperRockScissors':
        player.result = 'Win'
    else:
        player.result = 'Loss'
    player.opponent_hand = opponent.hand


class Shoot(Page):
    form_model = 'player'
    form_fields = ['hand']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(past_players=player.in_previous_rounds())


class WaitForOther(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            set_winner(p)


class FinalResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return dict(past_players=player.in_all_rounds())



page_sequence = [Shoot, WaitForOther, FinalResults]
