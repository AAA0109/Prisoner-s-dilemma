from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'intergenerational'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    MULTIPLIER = 1.8
    MIN_AMOUNT = 2


class Subsession(BaseSubsession):
    locked = models.BooleanField(initial=False)
    cur_value = models.IntegerField(initial=100)
    generation = models.IntegerField(initial=0)


def creating_session(subsession: Subsession):
    session = subsession.session
    session.intergenerational_history = []


def group_by_arrival_time_method(subsession: Subsession, waiting_players):
    if subsession.locked:
        return
    if len(waiting_players) >= 1:
        return [waiting_players[0]]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    value0 = models.IntegerField()
    value1 = models.IntegerField()
    value2 = models.IntegerField()
    extracted = models.IntegerField(label="Amount to extract", min=0)


def extracted_max(player: Player):
    return player.value1 - C.MIN_AMOUNT


class GBAT(WaitPage):
    group_by_arrival_time = True
    body_text = "You are in the queue..."

    @staticmethod
    def after_all_players_arrive(group: Group):
        subsession = group.subsession
        subsession.locked = True
        subsession.generation += 1
        # actually just 1 player per group
        for player in group.get_players():
            player.value0 = subsession.cur_value
            player.value1 = int(player.value0 * C.MULTIPLIER)


class Extract(Page):
    form_model = 'player'
    form_fields = ['extracted']
    timeout_seconds = 3 * 60

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        subsession = player.subsession
        session = player.session

        player.value2 = player.value1 - player.extracted
        subsession.cur_value = player.value2
        session.intergenerational_history.append(
            dict(
                generation=subsession.generation,
                value0=player.value0,
                value1=player.value1,
                extracted=player.extracted,
                value2=player.value2,
            )
        )

        subsession.locked = False


class Results(Page):
    pass


page_sequence = [GBAT, Extract, Results]
