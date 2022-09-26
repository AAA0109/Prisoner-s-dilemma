from otree.api import *

doc = """
Go/No-go
"""


class C(BaseConstants):
    NAME_IN_URL = 'go_no_go'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    RED_IMAGES = [0, 4, 8, 17]
    NUM_IMAGES = 10  # actually there are 20 images but we just show 10 for brevity


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        participant = p.participant
        image_ids = generate_ordering()
        for stim in image_ids:
            is_red = stim in C.RED_IMAGES
            Trial.create(player=p, image_id=stim, is_red=is_red)

        participant.reaction_times = []


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    num_completed = models.IntegerField(initial=0)
    num_errors = models.IntegerField(initial=0)
    avg_reaction_ms = models.FloatField()


def get_current_trial(player: Player):
    return Trial.filter(player=player, is_error=None)[0]


def is_finished(player: Player):
    return player.num_completed == C.NUM_IMAGES


class Trial(ExtraModel):
    player = models.Link(Player)
    reaction_ms = models.IntegerField()
    image_id = models.IntegerField()
    is_red = models.BooleanField()
    is_error = models.BooleanField()
    pressed = models.BooleanField()


def generate_ordering():
    import random

    numbers = list(range(C.NUM_IMAGES))
    random.shuffle(numbers)
    return numbers


# PAGES
class Introduction(Page):
    pass


class Task(Page):
    @staticmethod
    def live_method(player: Player, data):
        participant = player.participant
        if 'pressed' in data:
            trial = get_current_trial(player)
            # this is necessary because the timeout will cause duplicates to be sent
            if data['image_id'] != trial.image_id:
                return
            trial.is_error = trial.is_red == data['pressed']
            if trial.is_error:
                feedback = '✗'
                player.num_errors += 1
            else:
                feedback = '✓'
                if not trial.is_red:
                    trial.reaction_ms = data['answered_timestamp'] - data['displayed_timestamp']
                    participant.reaction_times.append(trial.reaction_ms)
            player.num_completed += 1
        else:
            feedback = ''

        if is_finished(player):
            return {player.id_in_group: dict(is_finished=True)}

        trial = get_current_trial(player)
        return {
            player.id_in_group: dict(image_id=trial.image_id, feedback=feedback, trialId=trial.id)
        }

    @staticmethod
    def vars_for_template(player: Player):
        image_paths = [
            'go_no_go/{}.png'.format(image_id) for image_id in range(C.NUM_IMAGES)
        ]

        return dict(image_paths=image_paths)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import statistics

        # if the participant never pressed, this list will be empty
        if participant.reaction_times:
            avg_reaction = statistics.mean(participant.reaction_times)
            player.avg_reaction_ms = int(avg_reaction)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(avg_reaction_ms=player.field_maybe_none('avg_reaction_ms'))


page_sequence = [Introduction, Task, Results]
