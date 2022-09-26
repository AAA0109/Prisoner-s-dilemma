from otree.api import *
import random

doc = """
Supergames of an indefinitely repeated prisoner's dilemma
"""


class C(BaseConstants):
    NAME_IN_URL = 'supergames_indefinite'
    PLAYERS_PER_GROUP = 2

    # this is the number of supergames
    NUM_ROUNDS = 5
    STOPPING_PROBABILITY = 0.2

    PAYOFFA = cu(300)
    PAYOFFB = cu(200)
    PAYOFFC = cu(100)
    PAYOFFD = cu(0)

    # True is cooperate, False is defect
    PAYOFF_MATRIX = {
        (True, True): (PAYOFFB, PAYOFFB),
        (True, False): (PAYOFFD, PAYOFFA),
        (False, True): (PAYOFFA, PAYOFFD),
        (False, False): (PAYOFFC, PAYOFFC),
    }

    INSTRUCTIONS_TEMPLATE = __name__ + '/instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    iteration = models.IntegerField(initial=0)
    finished_sg = models.BooleanField(initial=False)


def live_method(player, data):
    group = player.group
    my_id = player.id_in_group

    if group.finished_sg:
        return {my_id: dict(finished_sg=True)}

    [game] = Game.filter(group=group, iteration=group.iteration)

    coop_field = 'coop{}'.format(my_id)

    if 'coop' in data:
        coop = data['coop']
        if getattr(game, coop_field) is not None:
            return
        setattr(game, coop_field, coop)

        coops = (game.coop1, game.coop2)
        is_ready = None not in coops
        if is_ready:
            p1, p2 = group.get_players()
            [game.payoff1, game.payoff2] = C.PAYOFF_MATRIX[coops]
            p1.payoff += game.payoff1
            p2.payoff += game.payoff2

            game.has_results = True
            group.iteration += 1

            # random stopping rule
            if random.random() < C.STOPPING_PROBABILITY:
                group.finished_sg = True
                return {0: dict(finished_sg=True)}

            Game.create(group=group, iteration=group.iteration)

            return {
                0: dict(should_wait=False, last_results=to_dict(game), iteration=group.iteration)
            }
    i_decided = getattr(game, coop_field) is not None
    if group.iteration > 0:
        [prev_game] = Game.filter(group=group, iteration=group.iteration - 1)
        last_results = to_dict(prev_game)
    else:
        last_results = None
    return {
        my_id: dict(
            should_wait=i_decided and not game.has_results,
            last_results=last_results,
            iteration=group.iteration,
        )
    }


class Game(ExtraModel):
    group = models.Link(Group)
    iteration = models.IntegerField()
    coop1 = models.CurrencyField()
    coop2 = models.CurrencyField()
    payoff1 = models.CurrencyField()
    payoff2 = models.CurrencyField()
    has_results = models.BooleanField(initial=False)


def to_dict(game: Game):
    return dict(payoffs=[game.payoff1, game.payoff2], coops=[game.coop1, game.coop2])


class Player(BasePlayer):
    iteration = models.IntegerField(initial=0)


class WaitToStart(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        # make the first one
        Game.create(group=group, iteration=group.iteration)


class Play(Page):
    form_model = 'player'
    live_method = live_method

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)


class Results(Page):
    pass


page_sequence = [WaitToStart, Play, Results]
