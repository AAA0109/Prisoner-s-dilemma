import random

from otree.api import *

from . import rand_functions

doc = """
This app is a demonstration of different ordering of stimuli, 
such as multiple blocks, randomization between blocks,
randomization within blocks, and alternating blocks.
"""


class C(BaseConstants):
    NAME_IN_URL = 'randomize_stimuli'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    num_completed = models.IntegerField(initial=0)
    ordering_description = models.StringField()
    num_trials = models.IntegerField()
    num_page_loads = models.IntegerField(
        initial=0,
        doc="""If more than 1, indicates that the user reloaded the page.
        This complicates the interpretation of the timestamps.""",
    )


class Trial(ExtraModel):
    player = models.Link(Player)
    optionA = models.StringField()
    optionB = models.StringField()
    optionC = models.StringField()
    choice = models.StringField()
    block = models.StringField()
    is_intro = models.BooleanField(initial=False)


def to_dict(trial: Trial):
    return dict(
        optionA=trial.optionA,
        optionB=trial.optionB,
        optionC=trial.optionC,
        is_intro=trial.is_intro,
        block=trial.block,
        id=trial.id,
    )


def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        ordering_function = random.choice(
            [
                rand_functions.multiple_blocks,
                rand_functions.randomize_blocks,
                rand_functions.randomize_within_blocks,
                rand_functions.randomize_merged,
                rand_functions.alternate_blocks,
            ]
        )
        # see the other python file in this folder.
        # you can substitute one of the other randomization functions,
        # like randomize_within_blocks, etc.
        trials = ordering_function()
        player.num_trials = len(trials)

        for trial in ordering_function():
            # "**" unpacks a dict
            Trial.create(**trial, player=player)

        # you can delete this; it's just for the demo.
        player.ordering_description = ordering_function.__doc__


def is_finished(player: Player):
    return player.num_completed >= player.num_trials


def get_current_trial(player: Player):
    return Trial.filter(player=player, choice=None)[0]


# PAGES
class Stimuli(Page):
    @staticmethod
    def vars_for_template(player: Player):
        player.num_page_loads += 1

    @staticmethod
    def live_method(player: Player, data):
        my_id = player.id_in_group

        if 'response' in data:
            if is_finished(player):
                return
            trial = get_current_trial(player)
            # prevent double clicks
            if data['trialId'] != trial.id:
                return
            trial.choice = data['response']
            player.num_completed += 1

        if is_finished(player):
            return {my_id: dict(is_finished=True)}

        trial = get_current_trial(player)
        payload = dict(stimulus=to_dict(trial))
        return {my_id: payload}


class Intro(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(doc=doc)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(trials=Trial.filter(player=player))


page_sequence = [Intro, Stimuli, Results]
