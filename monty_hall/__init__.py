from otree.api import *

doc = """
Monty Hall problem
"""


class C(BaseConstants):
    NAME_IN_URL = 'monty_hall'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    door_first_chosen = models.IntegerField(choices=[1, 2, 3])
    door_revealed = models.IntegerField()
    door_not_revealed = models.IntegerField()
    door_finally_chosen = models.IntegerField()
    door_with_prize = models.IntegerField()
    is_winner = models.BooleanField()


def door_finally_chosen_choices(player: Player):
    return [player.door_first_chosen, player.door_not_revealed]


class Decide1(Page):
    form_model = 'player'
    form_fields = ['door_first_chosen']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random

        other_doors = [1, 2, 3]
        other_doors.remove(player.door_first_chosen)
        random.shuffle(other_doors)

        player.door_with_prize = random.choice([1, 2, 3])
        other_doors.sort(key=lambda door: door == player.door_with_prize)
        [player.door_revealed, player.door_not_revealed] = other_doors


class Decide2(Page):
    form_model = 'player'
    form_fields = ['door_finally_chosen']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.is_winner = player.door_finally_chosen == player.door_with_prize


class Results(Page):
    pass


page_sequence = [Decide1, Decide2, Results]
