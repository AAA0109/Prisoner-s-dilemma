from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import itertools
import json

author = 'Victor van Pelt'

doc = """
Questionnaire
"""


class Constants(BaseConstants):
    name_in_url = 'Questionnaire'
    players_per_group = None
    surveys = ['1', '2', '3']
    num_rounds = len(surveys)
    StandardChoices=[
        [1, 'Disagree strongly'],
        [2, 'Disagree moderately'],
        [3, 'Disagree a little'],
        [4, 'Neither agree nor disagree'],
        [5, 'Agree a little'],
        [6, 'Agree moderately'],
        [7, 'Agree strongly'],
    ]

    #Survey1
    Survey1Choices=StandardChoices

    #Survey2
    Survey2Choices=StandardChoices

    #Survey3
    Survey3Choices=StandardChoices

class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                round_numbers = list(range(1, Constants.num_rounds + 1))
                random.shuffle(round_numbers)
                p.participant.vars['surveys_rounds'] = dict(zip(Constants.surveys, round_numbers))
                p.participant.vars['num_rounds'] = Constants.num_rounds

    # def creating_session(self):
    #    from .pages import initial_page_sequence
    #    aaa = [i.__name__.split('_') for i in initial_page_sequence]
    #    page_blocks = [list(group) for key, group in itertools.groupby(aaa, key=lambda x: x[0])]
    #    for p in self.get_players():
    #        pb = page_blocks.copy()
    #        random.shuffle(pb)
    #        level1 = list(itertools.chain.from_iterable(pb))
    #        level2 = ['_'.join(i) for i in level1]
    #        p.participant.vars['initial_page_sequence'] = json.dumps(level2)

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    #Demographics
    gender = models.IntegerField(
        label="Please select your gender.",
        choices=[
            [1, 'Male'],
            [2, 'Female'],
            [3, 'Other'],
            [4, 'I prefer not to say.'],
        ]
    )

    age = models.IntegerField(label="Please enter your age.", min=14, max=90, blank=True)

    studies = models.IntegerField(
        label="Please estimate how many studies you have participated in (excluding this study)",
        choices=[
            [1, 'Less than 5 studies'],
            [2, 'Between 5 and less than 10 studies.'],
            [3, 'between 10 and less than 15 studies.'],
            [4, '15 or more studies.'],
            [5, 'I prefer not to say.']
        ]
    )

    workexperience = models.IntegerField(
        label="Please indicate your work experience. All jobs count, including part-time and volunteer work.",
        choices=[
            [1, 'I do not have work experience.'],
            [2, 'Less than 1 year work experience.'],
            [3, 'Between 1 and less than 2 years of work experience'],
            [4, 'Between 2 and less than 3 years work experience.'],
            [5, 'Between 3 and less than 4 years work experience.'],
            [6, 'Between 4 and less than 5 years work experience.'],
            [7, '5 years or more work experience.'],
            [8, 'I prefer not to say.'],
        ]
    )

    degree = models.IntegerField(
        label="Please indicate the highest academic degree you have completed. If you are currently actively pursuing one, please select that academic degree.",
        choices=[
            [1, 'High school or lower'],
            [2, 'Bachelor degree'],
            [3, 'Master degree'],
            [4, 'PhD degree'],
            [5, 'MBA degree'],
            [6, 'Other'],
            [7, 'I prefer not to say.']
        ]
    )

    english = models.IntegerField(
        label="Please rate your English on a percentage scale between 0 and 100.",
        min=0,
        max=100,
        blank=True,
        initial=None
    )

    #Survey1
    item1A = models.IntegerField(
        label='Statement 1A',
        choices=Constants.Survey1Choices
    )
    item1B = models.IntegerField(
        label='Statement 1B',
        choices=Constants.Survey1Choices
    )
    item1C = models.IntegerField(
        label='Statement 1C',
        choices=Constants.Survey1Choices
    )
    item1D = models.IntegerField(
        label='Statement 1D',
        choices=Constants.Survey1Choices
    )
    item1E = models.IntegerField(
        label='Statement 1E',
        choices=Constants.Survey1Choices
    )
    item1F = models.IntegerField(
        label='Statement 1F',
        choices=Constants.Survey1Choices
    )
    item1G = models.IntegerField(
        label='Statement 1G',
        choices=Constants.Survey1Choices
    )
    item1H = models.IntegerField(
        label='Statement 1H',
        choices=Constants.Survey1Choices
    )

    #Survey2
    item2A = models.IntegerField(
        label='Statement 2A',
        choices=Constants.Survey2Choices
    )
    item2B = models.IntegerField(
        label='Statement 2B',
        choices=Constants.Survey2Choices
    )
    item2C = models.IntegerField(
        label='Statement 2C',
        choices=Constants.Survey2Choices
    )
    item2D = models.IntegerField(
        label='Statement 2D',
        choices=Constants.Survey2Choices
    )
    item2E = models.IntegerField(
        label='Statement 2E',
        choices=Constants.Survey2Choices
    )
    item2F = models.IntegerField(
        label='Statement 2F',
        choices=Constants.Survey2Choices
    )
    item2G = models.IntegerField(
        label='Statement 2G',
        choices=Constants.Survey2Choices
    )
    item2H = models.IntegerField(
        label='Statement 2H',
        choices=Constants.Survey2Choices
    )
    item2I = models.IntegerField(
        label='Statement 2I',
        choices=Constants.Survey2Choices
    )
    item2J = models.IntegerField(
        label='Statement 2J',
        choices=Constants.Survey2Choices
    )

    #Survey3
    item3A = models.IntegerField(
        label='Statement 3A',
        choices=Constants.Survey3Choices
    )
    item3B = models.IntegerField(
        label='Statement 3B',
        choices=Constants.Survey3Choices
    )
    item3C = models.IntegerField(
        label='Statement 3C',
        choices=Constants.Survey3Choices
    )
    item3D = models.IntegerField(
        label='Statement 3D',
        choices=Constants.Survey3Choices
    )
    item3E = models.IntegerField(
        label='Statement 3E',
        choices=Constants.Survey3Choices
    )
    item3F = models.IntegerField(
        label='Statement 3F',
        choices=Constants.Survey3Choices
    )
    item3G = models.IntegerField(
        label='Statement 3G',
        choices=Constants.Survey3Choices
    )
    item3H = models.IntegerField(
        label='Statement 3H',
        choices=Constants.Survey3Choices
    )
    item3I = models.IntegerField(
        label='Statement 3I',
        choices=Constants.Survey3Choices
    )
    item3J = models.IntegerField(
        label='Statement 3J',
        choices=Constants.Survey3Choices
    )