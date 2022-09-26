from otree.api import *
import time

doc = """
Reach a consensus with your group before your payoffs shrink to 0.
Similar to the "Endgame" segment of the British game show "Divided": https://www.youtube.com/watch?v=8k8ETko16tQ
"""


class C(BaseConstants):
    NAME_IN_URL = 'fast_consensus'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1

    RANKS = [
        dict(number=1, payoff=cu(800), label="Gold"),
        dict(number=2, payoff=cu(300), label="Silver"),
        dict(number=3, payoff=cu(100), label="Bronze"),
    ]
    TIMEOUT_SECONDS = 60 * 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    deadline = models.FloatField()
    reached_consensus = models.BooleanField(initial=False)
    fraction_of_original = models.FloatField()


def seconds_left(group: Group):
    return group.deadline - time.time()


class Player(BasePlayer):
    proposed_rank = models.IntegerField()
    final_rank = models.IntegerField()
    rank_label = models.StringField()


# PAGES
class WaitToStart(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.deadline = time.time() + C.TIMEOUT_SECONDS


class Negotiate(Page):
    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        players = group.get_players()

        if group.reached_consensus:
            return {0: dict(finished=True)}

        if 'proposed_rank' in data:
            rank = data['proposed_rank']
            player.proposed_rank = rank
            if set(p.field_maybe_none('proposed_rank') for p in players) == set(
                d['number'] for d in C.RANKS
            ):
                payoffs = {d['number']: d['payoff'] for d in C.RANKS}
                labels = {d['number']: d['label'] for d in C.RANKS}
                fraction_of_original = round(seconds_left(group) / C.TIMEOUT_SECONDS, 4)
                group.fraction_of_original = fraction_of_original
                group.reached_consensus = True
                for p in players:
                    p.final_rank = p.proposed_rank
                    p.rank_label = labels[p.final_rank]
                    p.payoff = payoffs[p.final_rank] * fraction_of_original
                return {0: dict(finished=True)}

        return {
            0: dict(ranks=[[p.id_in_group, p.field_maybe_none('proposed_rank')] for p in players])
        }

    @staticmethod
    def js_vars(player: Player):
        group = player.group
        return dict(
            my_id=player.id_in_group,
            deadline=group.deadline,
            RANKS=C.RANKS,
            TIMEOUT_SECONDS=C.TIMEOUT_SECONDS,
        )

    @staticmethod
    def get_timeout_seconds(player: Player):
        import time

        group = player.group
        return group.deadline - time.time()


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [WaitToStart, Negotiate, ResultsWaitPage, Results]
