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
    surveys = ['1', '2', '3', '4']
    num_rounds = len(surveys)
    # Choices=[
    #     [1, 'Disagree strongly'],
    #     [2, 'Disagree moderately'],
    #     [3, 'Disagree a little'],
    #     [4, 'Neither agree nor disagree'],
    #     [5, 'Agree a little'],
    #     [6, 'Agree moderately'],
    #     [7, 'Agree strongly'],
    # ]
    Choices = [1, 2, 3, 4, 5]

class Subsession(BaseSubsession):
    pass
    # def creating_session(self):
    #     if self.round_number == 1:
    #         for p in self.get_players():
    #             round_numbers = list(range(3, Constants.num_rounds + 3))
                # p.participant.vars['surveys_rounds'] = dict(zip(Constants.surveys, round_numbers))
                # p.participant.vars['final'] = Constants.num_rounds + 3
                # p.participant.vars['demographics'] = 2
                # print(p.participant.vars)

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

    age = models.IntegerField(label="Please enter your age.", min=14, max=125, blank=True)

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

    risk_attitude = models.IntegerField(
        label="How willing are you in general to take risks on a scale from 0 (not willing to take risks at all) to 10 "
              "(highly willing to take risks)?",
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal
    )
    trust_degree = models.IntegerField(
        label="How much do you in general trust other people on a scale from 0 (I don’t trust other people at all) to "
              "10 (I fully trust other people)?",
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal
    )
    bat_ball = models.IntegerField(
        label="A bat and a ball cost 1.10 dollars in total. The bat costs 1.00 dollar more than the ball. How much "
              "does the ball cost? Your answer (in cents) e.g. $100 = 10000 cents:",
        min=0
    )
    machine_widget = models.IntegerField(
        label="If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 "
              "widgets? Your answer (in minutes):",
        min=0
    )
    lake_lily_pad = models.IntegerField(
        label="In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 48 days for "
              "the patch to cover the entire lake, how long would it take for the patch to cover half of the lake? "
              "Your answer (in number of days):",
        min=0
    )

    mach_1 = models.IntegerField(
        label = "It’s not wise to tell your secrets.",
        choices=Constants.Choices,
    )
    mach_2 = models.IntegerField(
        label="I like to use clever manipulation to get my way.",
        choices=Constants.Choices,
    )
    mach_3 = models.IntegerField(
        label="Whatever it takes, you must get the important people on your side.",
        choices=Constants.Choices,
    )
    mach_4 = models.IntegerField(
        label="Avoid direct conflict with others because they maybe useful in the future.",
        choices=Constants.Choices,
    )
    mach_5 = models.IntegerField(
        label="It’s wise to keep track of information that you can use against people later.",
        choices=Constants.Choices,
    )
    mach_6 = models.IntegerField(
        label="You should wait for the right time to get back at people.",
        choices=Constants.Choices,
    )
    mach_7 = models.IntegerField(
        label="there are things you should hide from other people to preserve your reputation.",
        choices=Constants.Choices,
    )
    mach_8 = models.IntegerField(
        label="Make sure your plans benefit yourself, not others.",
        choices=Constants.Choices,
    )
    mach_9 = models.IntegerField(
        label="Most people can be manipulated.",
        choices=Constants.Choices,
    )
    narc_1 = models.IntegerField(
        label="People see me as a natural leader.",
        choices=Constants.Choices,
    )
    narc_2 = models.IntegerField(
        label="I hate being the center of attention",
        choices=Constants.Choices,
    )
    narc_3 = models.IntegerField(
        label="Many group activities tend to be dull without me.",
        choices=Constants.Choices,
    )
    narc_4 = models.IntegerField(
        label="I know that I am special because everyone keeps telling me so.",
        choices=Constants.Choices,
    )
    narc_5 = models.IntegerField(
        label="I like to get acquainted with important people.",
        choices=Constants.Choices,
    )
    narc_6 = models.IntegerField(
        label="I feel embarrassed if someone compliments me.",
        choices=Constants.Choices,
    )
    narc_7 = models.IntegerField(
        label="I have been compared to famous people.",
        choices=Constants.Choices,
    )
    narc_8 = models.IntegerField(
        label="I am an average person.",
        choices=Constants.Choices,
    )
    narc_9 = models.IntegerField(
        label="I insist on getting the respect I deserve.",
        choices=Constants.Choices,
    )
    psych_1 = models.IntegerField(
        label="I like to get revenge on authorities.",
        choices=Constants.Choices,
    )
    psych_2 = models.IntegerField(
        label="I avoid dangerous situations.",
        choices=Constants.Choices,
    )
    psych_3 = models.IntegerField(
        label="Payback needs to be quick and nasty",
        choices=Constants.Choices,
    )
    psych_4 = models.IntegerField(
        label="People often say I’m out of control.",
        choices=Constants.Choices,
    )
    psych_5 = models.IntegerField(
        label="It’s true that I can be mean to others",
        choices=Constants.Choices,
    )
    psych_6 = models.IntegerField(
        label="People who mess with me always regret it",
        choices=Constants.Choices,
    )
    psych_7 = models.IntegerField(
        label="I have never gotten into trouble with the law.",
        choices=Constants.Choices,
    )
    psych_8 = models.IntegerField(
        label="I enjoy having sex with people I hardly know",
        choices=Constants.Choices,
    )
    psych_9 = models.IntegerField(
        label="I’ll say anything to get what I want",
        choices=Constants.Choices,
    )