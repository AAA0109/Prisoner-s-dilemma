from otree.api import *

doc = """
Game of Nim. Players take turns adding a number. First to 15 wins.
"""


class C(BaseConstants):
    NAME_IN_URL = 'nim'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    TARGET = 15


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    current_number = models.IntegerField(initial=1)
    whose_turn = models.IntegerField(initial=1)
    winner_id = models.IntegerField()
    game_over = models.BooleanField(initial=False)


class Player(BasePlayer):
    is_winner = models.BooleanField(initial=False)


# PAGES
class Game(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, number):
        group = player.group
        my_id = player.id_in_group
        other_id = 3 - my_id
        if (
            # if the number is non-null etc.
            number
            and number in [1, 2, 3]
            and group.whose_turn == my_id
            # if you're at 14, you can't choose 3.
            and group.current_number + number <= C.TARGET
        ):
            group.current_number += number
            news = dict(id_in_group=my_id, number=number)
            if group.current_number == C.TARGET:
                group.winner_id = player.id_in_group
                group.game_over = True
            else:
                group.whose_turn = other_id
        else:
            news = None

        return {
            0: dict(
                game_over=group.game_over,
                current_number=group.current_number,
                whose_turn=group.whose_turn,
                news=news,
            )
        }


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        winner = group.get_player_by_id(group.winner_id)
        winner.is_winner = True


class Results(Page):
    pass


page_sequence = [Game, ResultsWaitPage, Results]
