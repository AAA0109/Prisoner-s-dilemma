from datetime import datetime, timedelta
from otree.api import *
from scheduling_part1 import C as GroupingAppConstants

doc = """
Scheduling players to start at a certain time (part 0: booking app) 
"""


def round_up_minutes(dt: datetime, minutes_step: int):
    discard = timedelta(minutes=dt.minute % minutes_step, seconds=dt.second)
    dt -= discard
    dt += timedelta(minutes=minutes_step)
    return dt


class C(BaseConstants):
    NAME_IN_URL = 'scheduling_part0'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    BATCHES_PER_HOUR = 6
    NUM_BATCHES = 10
    FIRST_BATCH_DELAY_MINUTES = 0
    PLAYERS_PER_BATCH = GroupingAppConstants.PLAYERS_PER_GROUP


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class Batch(ExtraModel):
    subsession = models.Link(Subsession)
    time = models.FloatField()
    number = models.IntegerField()


class Slot(ExtraModel):
    subsession = models.Link(Subsession)
    batch = models.Link(Batch)
    player = models.Link(Player)


def creating_session(subsession: Subsession):
    minutes_step = int(60 / C.BATCHES_PER_HOUR)
    now = datetime.now()
    first_slot_time = round_up_minutes(
        now + timedelta(minutes=C.FIRST_BATCH_DELAY_MINUTES), minutes_step
    )
    for i in range(C.NUM_BATCHES):
        dt = first_slot_time + timedelta(minutes=minutes_step * i)
        batch = Batch.create(subsession=subsession, time=dt.timestamp(), number=i)
        for j in range(C.PLAYERS_PER_BATCH):
            Slot.create(subsession=subsession, batch=batch)


def live_booking(player: Player, data):
    """
    It doesn't matter whether we use group or subsession here,
    because players_per_group = None.
    """
    subsession = player.subsession
    msg_type = data['type']
    if msg_type == 'book' or msg_type == 'cancel':
        for slot in Slot.filter(player=player):
            slot.player = None
    if msg_type == 'book':
        [batch] = Batch.filter(number=data['batch_number'], subsession=subsession)
        free_slots = Slot.filter(batch=batch, player=None)
        if free_slots:
            free_slots[0].player = player
    batches_data = []
    batches = Batch.filter(subsession=subsession)
    for b in batches:
        slots = Slot.filter(batch=b, subsession=subsession)
        num_free_slots = 0
        player_ids = []
        for s in slots:
            if s.player:
                player_ids.append(s.player.id_in_group)
            else:
                num_free_slots += 1
        batches_data.append(
            dict(
                time=b.time, number=b.number, player_ids=player_ids, num_free_slots=num_free_slots,
            )
        )
    return {0: dict(batches=batches_data)}


class Booking(Page):
    live_method = live_booking

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def error_message(player: Player, values):
        if not Slot.filter(player=player):
            return "You have not made a booking yet"

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        [slot] = Slot.filter(player=player)
        participant.booking_time = slot.batch.time


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [Booking]
