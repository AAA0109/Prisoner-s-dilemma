from otree.api import *

doc = """
Continuous-time public goods game with slider
"""


class C(BaseConstants):
    NAME_IN_URL = 'continuous_slider'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    MAX_CONTRIBUTION = cu(100)
    CHART_TEMPLATE = __name__ + '/chart.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    start_timestamp = models.IntegerField()


class Player(BasePlayer):
    pass


class Adjustment(ExtraModel):
    group = models.Link(Group)
    player = models.Link(Player)
    contribution = models.CurrencyField()
    seconds = models.IntegerField(doc="Timestamp (seconds since beginning of trading)")


class WaitToStart(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        import time

        group.start_timestamp = int(time.time())
        for p in group.get_players():
            Adjustment.create(
                player=p, group=group, contribution=C.MAX_CONTRIBUTION / 2, seconds=0,
            )


# PAGES
class MyPage(Page):
    timeout_seconds = 5 * 60

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group, max_contribution=C.MAX_CONTRIBUTION)

    @staticmethod
    def vars_for_template(player: Player):
        return dict(max_contribution=int(C.MAX_CONTRIBUTION))

    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        import time

        # print('data is', data)

        now_seconds = int(time.time() - group.start_timestamp)

        if 'contribution' in data:
            contribution = data['contribution']
            Adjustment.create(
                player=player, group=group, contribution=contribution, seconds=now_seconds,
            )

        highcharts_series = []
        for p in group.get_players():
            history = [[adj.seconds, adj.contribution] for adj in Adjustment.filter(player=p)]

            # this is optional. it allows the line
            # to go all the way to the right of the graph
            last_contribution = history[-1][1]
            history.append([now_seconds, last_contribution])

            series = dict(data=history, type='line', name='Player {}'.format(p.id_in_group))
            highcharts_series.append(series)
        return {0: dict(highcharts_series=highcharts_series)}


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        # to be filled in.
        # you should calculate some results here. maybe aggregate all the Adjustments,
        # take their weighted average, etc.
        # adjustments = Adjustment.filter(group=group)
        pass


class Results(Page):
    pass


page_sequence = [WaitToStart, MyPage, ResultsWaitPage, Results]
