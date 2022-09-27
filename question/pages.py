from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
import json

def progress(p):
    curpageindex = page_sequence.index(type(p))+1
    progress = ((p.round_number-1)*pages_per_round+curpageindex)/tot_pages*100
    return progress

class Introduction(Page):

    def is_displayed(self):
        return self.round_number == 1

    #def vars_for_template(self):
    #    curpageindex = page_sequence.index(type(self)) - 1
    #    progress = curpageindex / tot_pages * 100
    #    return {
    #        'progress': progress
    #    }

class Survey1(Page):
    form_model = 'player'
    form_fields = [
        'risk_attitude',
        'trust_degree',
        'bat_ball',
        'machine_widget',
        'lake_lily_pad',
    ]

    def is_displayed(self):
        return self.round_number == self.participant.vars['surveys_rounds']['1']

    def get_form_fields(self):
        fields = self.form_fields
        # random.shuffle(fields)
        return fields

#    def progress(self):
#        curpageindex = json.loads(self.participant.vars.get('initial_page_sequence')).index(str(self.__class__.__name__)) + 1
#        progress = curpageindex / tot_pages * 100
#        return progress

    def vars_for_template(self):
        #curpageindex = page_sequence.index(type(self)) - 1
        #progress = curpageindex / len(page_sequence) * 100
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

    def is_displayed(self):
        return self.round_number == self.participant.vars['surveys_rounds']['2']

    def get_form_fields(self):
        fields = self.form_fields
        random.shuffle(fields)
        return fields

#    def progress(self):
#        curpageindex = json.loads(self.participant.vars.get('initial_page_sequence')).index(str(self.__class__.__name__)) + 1
#        progress = curpageindex / tot_pages * 100
#        return progress

    def vars_for_template(self):
        #curpageindex = page_sequence.index(type(self)) - 1
        #progress = curpageindex / len(page_sequence) * 100
        return {
            'progress': progress(self)
        }

class Survey3(Page):
    form_model = 'player'
    form_fields = [
        'narc_2',
        'narc_3',
        'narc_4',
        'narc_5',
        'narc_6',
        'narc_7',
        'narc_8',
        'narc_9'
    ]

    def is_displayed(self):
        return self.round_number == self.participant.vars['surveys_rounds']['3']

    def get_form_fields(self):
        fields = self.form_fields
        random.shuffle(fields)
        return fields

    def vars_for_template(self):
        #curpageindex = page_sequence.index(type(self)) - 1
        #progress = curpageindex / len(page_sequence) * 100
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

    def is_displayed(self):
        return self.round_number == self.participant.vars['surveys_rounds']['4']

    def get_form_fields(self):
        fields = self.form_fields
        random.shuffle(fields)
        return fields

    def vars_for_template(self):
        #curpageindex = page_sequence.index(type(self)) - 1
        #progress = curpageindex / len(page_sequence) * 100
        return {
            'progress': progress(self)
        }

class Demographics(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'studies', 'workexperience', 'degree', 'english']

    def is_displayed(self):
        return self.round_number == self.participant.vars['num_rounds']

    def get_form_fields(self):
        fields = self.form_fields
        random.shuffle(fields)
        return fields

#    def progress(self):
#            curpageindex = page_sequence.index(type(self))
#            progress = curpageindex / tot_pages * 100
#            return progress

    def vars_for_template(self):
        #curpageindex = page_sequence.index(type(self)) - 1
        #progress = curpageindex / len(page_sequence) * 100
        return {
            'progress': progress(self)
        }


page_sequence = [
    Introduction,
    Demographics,
    Survey1,
    Survey2,
    Survey3,
    Survey4
]

pages_per_round = len(page_sequence)
tot_pages = pages_per_round * Constants.num_rounds