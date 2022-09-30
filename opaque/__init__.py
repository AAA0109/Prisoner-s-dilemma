from mimetypes import init
from otree.api import *
import random

doc = """
Prisoner's dilemma (Opaque)
"""

class C(BaseConstants):
    NAME_IN_URL = 'opaque'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    PAYOFFA = cu(2)
    PAYOFFB = cu(4)
    PAYOFFC = cu(6)
    PAYOFFD = cu(9)

    PAYOFF_MATRIX = {
        (True, True): (PAYOFFC, PAYOFFC),
        (True, False): (PAYOFFA, PAYOFFD),
        (False, True): (PAYOFFD, PAYOFFA),
        (False, False): (PAYOFFB, PAYOFFB),
    }

    INSTRUCTIONS_TEMPLATE = __name__ + '/instructions.html'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    first_player = models.IntegerField(initial=1)
    player_turn = models.IntegerField(initial=1)
    mode = models.IntegerField(initial=1)  # 0: baseline, 1: opaque, 2: transparent


class Player(BasePlayer):
    choice = models.LongStringField(initial='')
    other_choice = models.LongStringField(initial='')
    question_for_first = models.IntegerField(initial=-1)
    pass

class Game(ExtraModel):
    group = models.Link(Group)
    choice1 = models.CurrencyField()
    choice2 = models.CurrencyField()
    payoff1 = models.CurrencyField()
    payoff2 = models.CurrencyField()
    
def getChoiceFromBool(choice):
    if choice:
        return 'A'
    return 'B'

def live_method(player, data):
    group = player.group
    my_id = player.id_in_group

    [game] = Game.filter(group = group)

    if data['type'] == 'choice':
        choice_field = 'choice{}'.format(my_id)
        if 'answer' in data:
            player.question_for_first = data['answer']

        if my_id != group.player_turn:
            return
        group.player_turn = 3 - group.player_turn

        choice = data['choice']
        if getattr(game, choice_field) is not None:
            return
        setattr(game, choice_field, choice)
        player.choice = getChoiceFromBool(choice)
        player.get_others_in_group()[0].other_choice = getChoiceFromBool(choice)

        choices = (game.choice1, game.choice2)
        is_ready = None not in choices
        if is_ready:
            p1, p2 = group.get_players()
            [game.payoff1, game.payoff2] = C.PAYOFF_MATRIX[choices]
            p1.payoff += game.payoff1
            p2.payoff += game.payoff2

    return {
        1: dict(
            type = 'status',
            should_wait = group.player_turn != 1,
            other_result = game.choice2,
            finished = game.choice1 is not None and game.choice2 is not None
        ),
        2: dict(
            type = 'status',
            should_wait = group.player_turn != 2,
            other_result = game.choice1,
            finished = game.choice1 is not None and game.choice2 is not None
        )
    }

def live_turn_method(player, data):
    group = player.group
    my_id = player.id_in_group

    if data['type'] == 'init':
        if group.mode == -1:
            group.mode = random.choice([0, 1, 2])
        return { 0: dict( type='init', mode=group.mode ) }
    if data['type'] == 'turn':
        if (my_id != 1):
            return
        group.first_player = data['turn']
        group.player_turn = group.first_player
    return { 0: dict( type = 'finished' ) }

class WaitToStart(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        Game.create(group=group)

class Play(Page):
    form_model = 'player'
    live_method = live_method

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id = player.id_in_group, first_player = player.group.first_player, mode = player.group.mode)

class Turn(Page):
    live_method = live_turn_method
    def js_vars(player: Player):
        return dict(my_id = player.id_in_group)

class Results(Page):
    pass

page_sequence = [WaitToStart, Turn, Play, Results]