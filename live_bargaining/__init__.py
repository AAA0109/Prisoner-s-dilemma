from otree.api import *


doc = """
For oTree beginners, it would be simpler to implement this as a discrete-time game 
by using multiple rounds, e.g. 10 rounds, where in each round both players can make a new proposal,
or accept the value from the previous round.

However, the discrete-time version has more limitations
(fixed communication structure, limited number of iterations).

Also, the continuous-time version works smoother & faster, 
and is less resource-intensive since it all takes place in 1 page.
"""


class C(BaseConstants):
    NAME_IN_URL = 'live_bargaining'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    SELLER_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    deal_price = models.CurrencyField()
    is_finished = models.BooleanField(initial=False)


class Player(BasePlayer):
    amount_proposed = models.IntegerField()
    amount_accepted = models.IntegerField()


class Bargain(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_role=player.get_others_in_group()[0].role)

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, data):

        group = player.group
        [other] = player.get_others_in_group()

        if 'amount' in data:
            try:
                amount = int(data['amount'])
            except Exception:
                print('Invalid message received', data)
                return
            if data['type'] == 'accept':
                if amount == other.amount_proposed:
                    player.amount_accepted = amount
                    group.deal_price = amount
                    group.is_finished = True
                    return {0: dict(finished=True)}
            if data['type'] == 'propose':
                player.amount_proposed = amount

        proposals = []
        for p in [player, other]:
            amount_proposed = p.field_maybe_none('amount_proposed')
            if amount_proposed is not None:
                proposals.append([p.id_in_group, amount_proposed])
        return {0: dict(proposals=proposals)}

    @staticmethod
    def error_message(player: Player, values):
        group = player.group
        if not group.is_finished:
            return "Game not finished yet"

    @staticmethod
    def is_displayed(player: Player):
        """Skip this page if a deal has already been made"""
        group = player.group
        deal_price = group.field_maybe_none('deal_price')
        return deal_price is None


class Results(Page):
    pass


page_sequence = [Bargain, Results]
