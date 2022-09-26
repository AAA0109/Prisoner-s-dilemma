from otree.api import *


doc = """
Dollar auction
"""


class C(BaseConstants):
    NAME_IN_URL = 'dollar_auction'
    INSTRUCTIONS_TEMPLATE = 'dollar_auction/instructions.html'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    JACKPOT = 100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    top_bid = models.CurrencyField(initial=0)
    second_bid = models.CurrencyField(initial=0)

    top_bidder = models.IntegerField(initial=-1)
    second_bidder = models.IntegerField(initial=-1)

    auction_timeout = models.FloatField()


def get_state(group: Group):
    return dict(
        top_bid=group.top_bid,
        top_bidder=group.top_bidder,
        second_bid=group.second_bid,
        second_bidder=group.second_bidder,
    )


class Player(BasePlayer):
    is_top_bidder = models.BooleanField(initial=False)
    is_second_bidder = models.BooleanField(initial=False)


class Intro(Page):
    pass


class WaitToStart(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        import time

        group.auction_timeout = time.time() + 60


# PAGES
class Bid(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        import time

        group = player.group
        return group.auction_timeout - time.time()

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, bid):
        group = player.group
        my_id = player.id_in_group
        if bid:
            if bid > group.top_bid:
                group.second_bid = group.top_bid
                group.second_bidder = group.top_bidder
                group.top_bid = bid
                group.top_bidder = my_id
                return {0: dict(get_state(group), new_top_bid=True)}
        else:
            return {my_id: get_state(group)}


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        if group.top_bidder > 0:
            top_bidder = group.get_player_by_id(group.top_bidder)
            top_bidder.payoff = C.JACKPOT - group.top_bid
            top_bidder.is_top_bidder = True

        if group.second_bidder > 0:
            second_bidder = group.get_player_by_id(group.second_bidder)
            second_bidder.payoff = -group.second_bid
            second_bidder.is_second_bidder = True


class Results(Page):
    pass


page_sequence = [Intro, WaitToStart, Bid, ResultsWaitPage, Results]
