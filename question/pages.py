from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Player
import random
import json

def progress(p):
    curpageindex = page_sequence.index(type(p))+1
    progress = int(((p.round_number-1)*pages_per_round+curpageindex)/tot_pages*100)
    return progress

class Introduction(Page):
    pass
    # def is_displayed(self):
    #     return self.round_number == 1

class Survey1(Page):
    form_model = 'player'
    form_fields = [
        'risk_attitude',
        'trust_degree',
        'bat_ball',
        'machine_widget',
        'lake_lily_pad',
        'give_up',
        'share_others',
        'lost_way',
        'punish_unfair'
    ]

    # def is_displayed(self):
    #     return self.round_number == self.participant.vars['surveys_rounds']['1']

    def get_form_fields(self):
        fields = self.form_fields
        return fields

    def vars_for_template(self):
        return {
            'progress': progress(self)
        }

class Survey2(Page):
    form_model = 'player'
    form_fields = [
        'mach_1',
        'mach_2',
        'mach_3',
        'mach_4',
        'mach_5',
        'mach_6',
        'mach_7',
        'mach_8',
        'mach_9'
    ]

    # def is_displayed(self):
    #     return self.round_number == self.participant.vars['surveys_rounds']['2']

    def get_form_fields(self):
        fields = self.form_fields
        # random.shuffle(fields)
        return fields

    def vars_for_template(self):
        return {
            'progress': progress(self)
        }

class Survey3(Page):
    form_model = 'player'
    form_fields = [
        'narc_1',
        'narc_2',
        'narc_3',
        'narc_4',
        'narc_5',
        'narc_6',
        'narc_7',
        'narc_8',
        'narc_9'
    ]

    # def is_displayed(self):
    #     return self.round_number == self.participant.vars['surveys_rounds']['3']

    def get_form_fields(self):
        fields = self.form_fields
        # random.shuffle(fields)
        return fields

    def vars_for_template(self):
        return {
            'progress': progress(self)
        }

class Survey4(Page):
    form_model = 'player'
    form_fields = [
        'psych_1',
        'psych_2',
        'psych_3',
        'psych_4',
        'psych_5',
        'psych_6',
        'psych_7',
        'psych_8',
        'psych_9'
    ]

    # def is_displayed(self):
    #     return self.round_number == self.participant.vars['surveys_rounds']['4']

    def get_form_fields(self):
        fields = self.form_fields
        # random.shuffle(fields)
        return fields

    def vars_for_template(self):
        return {
            'progress': progress(self)
        }

class Demographics(Page):
    form_model = 'player'
    form_fields = ['gender', 'age']

    # def is_displayed(self):
    #     return self.round_number == self.participant.vars['demographics']

    def get_form_fields(self):
        fields = self.form_fields
        # random.shuffle(fields)
        return fields

    def vars_for_template(self):
        return {
            'progress': progress(self)
        }

class Final(Page):
    # def is_displayed(self):
    #     return self.round_number == self.participant.vars['final']
    def vars_for_template(player):
        participant = player.participant
        print(participant)
        
        return dict(
            choice = participant.choice,
            other_choice = participant.other_choice,
        )
class Payment(Page):
    def before_next_page(self):
        self.prolific_id = self.participant.label
        self. participant.finished = True    
    def js_vars(player):
        return dict(
            completionlink=
              player.subsession.session.config['completionlink']
        )


page_sequence = [
    Introduction,
    Demographics,
    Survey1,
    Survey2,
    Survey3,
    Survey4,
    Final,
    Payment
]

pages_per_round = len(page_sequence)
tot_pages = pages_per_round