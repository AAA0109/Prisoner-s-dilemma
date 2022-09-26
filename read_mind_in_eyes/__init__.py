from otree.api import *


doc = """
Reading the Mind in the Eyes Test (Baron-Cohen et al. 2001).
See here: http://socialintelligence.labinthewild.org/mite/
"""


def read_csv():
    import csv

    f = open(__name__ + '/stimuli.csv', encoding='utf-8-sig')
    rows = [row for row in csv.DictReader(f)]
    for row in rows:
        row['image_path'] = 'read_mind_in_eyes/{}.png'.format(row['image'])

    return {row['image']: row for row in rows}


class C(BaseConstants):
    NAME_IN_URL = 'read_mind_in_eyes'
    PLAYERS_PER_GROUP = None
    IMAGES = read_csv()
    NUM_ROUNDS = len(IMAGES)
    INSTRUCTIONS_TEMPLATE = __name__ + '/instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    choice = models.StringField(
        label="What emotion are the eyes showing?", widget=widgets.RadioSelect
    )
    is_correct = models.BooleanField()


def choice_choices(player: Player):
    trial = get_current_trial(player)
    return [
        ['A', trial['A']],
        ['B', trial['B']],
        ['C', trial['C']],
        ['D', trial['D']],
    ]


def get_current_trial(player: Player):
    if player.round_number == 1:
        image_name = 'practice'
    else:
        image_name = str(player.round_number - 1)
    return C.IMAGES[image_name]


class Play(Page):
    form_model = 'player'
    form_fields = ['choice']

    @staticmethod
    def vars_for_template(player: Player):
        trial = get_current_trial(player)
        return dict(image_path=trial['image_path'], is_practice=player.round_number == 1)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        trial = get_current_trial(player)
        player.is_correct = player.choice == trial['solution']


class PracticeFeedback(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant

        score = sum(p.is_correct for p in player.in_rounds(2, C.NUM_ROUNDS))
        participant.read_mind_in_eyes_score = score

        return dict(score=score)


page_sequence = [Play, PracticeFeedback, Results]
