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
        'item1A',
        'item1B',
        'item1C',
        'item1D',
        'item1E',
        'item1F',
        'item1G',
        'item1H'
    ]

    def is_displayed(self):
        return self.round_number == self.participant.vars['surveys_rounds']['1']

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

class Survey2(Page):
    form_model = 'player'
    form_fields = [
        'item2A',
        'item2B',
        'item2C',
        'item2D',
        'item2E',
        'item2F',
        'item2G',
        'item2H',
        'item2I',
        'item2J'
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
        'item3A',
        'item3B',
        'item3C',
        'item3D',
        'item3E',
        'item3F',
        'item3G',
        'item3H',
        'item3I',
        'item3J'
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
    # Survey1,
    # Survey2,
    # Survey3,
    Demographics
]

pages_per_round = len(page_sequence)
tot_pages = pages_per_round * Constants.num_rounds