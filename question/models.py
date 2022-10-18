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
    bat_ball = models.FloatField(
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
    give_up = models.IntegerField(
        label="In comparison to others, are you a person who is generally willing to give up something today to "
              "benefit from that in the future or are you not willing to do so?",
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal
    )
    share_others = models.IntegerField(
        label="How do you assess your willingness to share with others without expecting anything in return "
              "when it comes to charity?",
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal
    )
    lost_way = models.StringField(
        label="Imagine the following situation: you are shopping in an unfamiliar city and realize you lost your way. "
              "You ask a stranger for directions. The stranger offers to take you with their car to your destination. "
              "The ride takes about 20 minutes and costs the stranger about 20 Euro in total. The stranger does not want money for it. "
              "You carry six bottles of wine with you. The cheapest bottle costs 5 Euro, the most expensive one 30 Euro. "
              "You decide to give one of the bottles to the stranger as a thank-you gift. Which bottle do you give?",
        choices=['5 Euro', '10 Euro', '15 Euro', '20 Euro', '25 Euro', '30 Euro'],
        widget=widgets.RadioSelectHorizontal
    )
    punish_unfair = models.IntegerField(
        label="4.	How do you see yourself: Are you a person who is generally willing to punish unfair behaviour even if this is costly?",
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal
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
        label="I hate being the center of attention.",
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
        label="Payback needs to be quick and nasty.",
        choices=Constants.Choices,
    )
    psych_4 = models.IntegerField(
        label="People often say I’m out of control.",
        choices=Constants.Choices,
    )
    psych_5 = models.IntegerField(
        label="It’s true that I can be mean to others.",
        choices=Constants.Choices,
    )
    psych_6 = models.IntegerField(
        label="People who mess with me always regret it.",
        choices=Constants.Choices,
    )
    psych_7 = models.IntegerField(
        label="I have never gotten into trouble with the law.",
        choices=Constants.Choices,
    )
    psych_8 = models.IntegerField(
        label="I enjoy having sex with people I hardly know.",
        choices=Constants.Choices,
    )
    psych_9 = models.IntegerField(
        label="I’ll say anything to get what I want.",
        choices=Constants.Choices,
    )