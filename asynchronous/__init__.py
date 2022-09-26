from otree.api import *


doc = """
Asynchronous 2-player sequential game (players can play at different times),
where we guarantee players never have to wait.
The example used is an ultimatum game.  
The first player who arrives is assigned to be P1.
If the next player arrives after P1 has made a decision, he will be paired with P1 and see P1's decision.
Otherwise, he will be P1 in a new group.
Worst-case scenario is that all players arrive around the same time, 
and therefore everyone gets assigned to be P1.

This game doesn't use oTree groups. 
Rather, it stores the partner's ID in a player field.
"""


class C(BaseConstants):
    NAME_IN_URL = 'asynchronous'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    session = subsession.session
    # queue of players who are finished.
    session.finished_p1_list = []


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    is_p1 = models.BooleanField()
    offer = models.CurrencyField(
        min=0,
        max=C.ENDOWMENT,
        label="What's your offer to Player 2?",
        doc="This field is only used if the player is P1",
    )
    partner_id = models.IntegerField(
        doc="This field is only used if the player is P2. It stores the ID of P1",
    )
    accepted = models.BooleanField(
        label="Do you accept Player 1's offer?", doc="This field is only used if the player is P2",
    )


class Intro(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # 'group' is not the 2-player group, but rather the default oTree
        # group of all players in the session.
        group = player.group

        session = player.session
        finished_p1_list = session.finished_p1_list
        # if someone already finished, assign the current player
        # to be P2
        if finished_p1_list:
            player.is_p1 = False
            player.partner_id = finished_p1_list.pop()
            p1 = group.get_player_by_id(player.partner_id)
            p1.partner_id = player.id_in_group
        else:
            player.is_p1 = True


class P1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.is_p1

    form_model = 'player'
    form_fields = ['offer']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        # indicate that the player has finished so that he can be paired
        # with the next p2.
        session.finished_p1_list.append(player.id_in_group)


class P1ThankYou(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.is_p1


class P2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return not player.is_p1

    form_model = 'player'
    form_fields = ['accepted']

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        p1 = group.get_player_by_id(player.partner_id)
        return dict(p1=p1)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.group
        p1 = group.get_player_by_id(player.partner_id)
        if player.accepted:
            player.payoff = p1.offer
            p1.payoff = C.ENDOWMENT - p1.offer
        else:
            player.payoff = 0
            p1.payoff = 0


class P2Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return not player.is_p1

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        p1 = group.get_player_by_id(player.partner_id)
        return dict(p1=p1)


page_sequence = [
    Intro,
    P1,
    P1ThankYou,
    P2,
    P2Results,
]
