from pathlib import Path
from otree.api import *

doc = """
Stroop test. 
"""


def get_permutations():
    colors = C.COLORS

    idx = 0
    items = []
    for decoy_text in colors:
        for color in colors:
            items.append(
                dict(
                    decoy_text=decoy_text,
                    color=color,
                    image_id=idx,
                    is_congruent=decoy_text == color,
                )
            )
            idx += 1
    return items


def randomize_order():
    import random

    permutations = get_permutations()
    random.shuffle(permutations)
    return permutations


class C(BaseConstants):
    NAME_IN_URL = 'stroop'
    INSTRUCTIONS_TEMPLATE = 'stroop/instructions.html'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    COLORS = ['red', 'yellow', 'blue', 'green']
    COLOR_KEYS = [('r', 'red'), ('y', 'yellow'), ('b', 'blue'), ('g', 'green')]
    NUM_TRIALS = len(COLORS) * len(COLORS)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    num_completed = models.IntegerField(initial=0)
    num_correct = models.IntegerField(initial=0)
    avg_congruent = models.FloatField()
    avg_incongruent = models.FloatField()
    incongruent_minus_congruent = models.FloatField()
    num_page_loads = models.IntegerField(
        initial=0,
        doc="""If more than 1, indicates that the user reloaded the page.
        This could change the interpretation of the timestamps.""",
    )


class Trial(ExtraModel):
    player = models.Link(Player)
    image_id = models.IntegerField()
    decoy_text = models.StringField()
    color = models.StringField()
    is_correct = models.BooleanField()
    is_congruent = models.BooleanField()
    reaction_ms = models.IntegerField()


def get_current_trial(player: Player):
    return Trial.filter(player=player, is_correct=None)[0]


def is_finished(player: Player):
    return player.num_completed == C.NUM_TRIALS


# FUNCTIONS
def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        for permutation in randomize_order():
            Trial.create(player=p, **permutation)


def live_method(player: Player, data):

    if data:
        if is_finished(player):
            return
        trial = get_current_trial(player)

        # guard against double-clicks
        if data['image_id'] != trial.image_id:
            return

        displayed_timestamp = data['displayed_timestamp']
        answered_timestamp = data['answered_timestamp']
        trial.submission = data['submission']

        trial.is_correct = trial.submission == trial.color
        trial.reaction_ms = answered_timestamp - displayed_timestamp

        if trial.is_correct:
            player.num_correct += 1
            feedback = '✓'
        else:
            feedback = '✗'
        player.num_completed += 1

    else:
        feedback = ''

    if is_finished(player):
        return {player.id_in_group: dict(is_finished=True)}

    payload = dict(feedback=feedback, image_id=get_current_trial(player).image_id)
    return {player.id_in_group: payload}


# PAGES
class Introduction(Page):
    pass


class Task(Page):
    live_method = live_method

    @staticmethod
    def vars_for_template(player: Player):
        player.num_page_loads += 1

        image_paths = ['stroop/{}.png'.format(i) for i in range(C.NUM_TRIALS)]
        return dict(image_paths=image_paths)

    @staticmethod
    def js_vars(player: Player):
        return dict(color_keys=dict(C.COLOR_KEYS))

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        from statistics import mean

        congruent_times = []
        incongruent_times = []
        for trial in Trial.filter(player=player):
            if trial.is_congruent:
                lst = congruent_times
            else:
                lst = incongruent_times
            lst.append(trial.reaction_ms)

        player.avg_congruent = int(mean(congruent_times))
        player.avg_incongruent = int(mean(incongruent_times))
        player.incongruent_minus_congruent = player.avg_incongruent - player.avg_congruent


class Results(Page):
    pass


page_sequence = [Introduction, Task, Results]
