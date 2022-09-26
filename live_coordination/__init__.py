from otree.api import *


doc = """
Live coordination (voting with chat/negotiation)
"""


class C(BaseConstants):
    NAME_IN_URL = 'live_coordination'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 1
    MAX_POINTS = 5
    CHOICES = [0, 1, 2, 3, 4, 5]
    MAJORITY = int(PLAYERS_PER_GROUP / 2) + 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    contribution = models.CurrencyField()


class Player(BasePlayer):
    vote = models.IntegerField()


# PAGES
class Coordinate(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, data):
        group = player.group

        if 'vote' in data:
            try:
                vote = int(data['vote'])
            except Exception:
                print('Invalid message received', data)
                return
            if not vote in C.CHOICES:
                print('Invalid message received', data)
                return
            player.vote = vote
        players = group.get_players()

        tallies = {vote: 0 for vote in C.CHOICES}
        votes = []
        for p in players:
            vote = p.field_maybe_none('vote')
            if vote is not None:
                tallies[vote] += 1
                if tallies[vote] >= C.MAJORITY:
                    group.contribution = vote
                    return {0: dict(finished=True)}
            votes.append([p.id_in_group, vote])

        # if you don't want to show who voted, use 'tallies' instead of 'votes'.
        return {0: dict(votes=votes, tallies=tallies)}

    @staticmethod
    def is_displayed(player: Player):
        """Skip this page if a deal has already been made"""
        group = player.group
        contribution = group.field_maybe_none('contribution')
        return contribution is None

    @staticmethod
    def error_message(player: Player, values):
        group = player.group
        # anti-cheating measure
        if group.field_maybe_none('contribution') is None:
            return "Not done with this page"


class Results(Page):
    pass


page_sequence = [Coordinate, Results]
