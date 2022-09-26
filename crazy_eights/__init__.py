from otree.api import *
import random
import json

doc = """
Card game (crazy eights)
"""

SUITS = 'SHDC'
NUMBERS = 'A23456789TJQK'
DECK = tuple([number + suit for number in NUMBERS for suit in SUITS])
NUMBERS_TO_CODEPOINTS = dict(zip(NUMBERS, '123456789ABDE'))
SUITS_TO_CODEPOINTS = dict(zip('SHDC', 'ABCD'))


class C(BaseConstants):
    NAME_IN_URL = 'crazy_eights'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    current_card = models.StringField(initial='')
    stock = models.LongStringField()
    whose_turn = models.IntegerField(initial=1)


class Player(BasePlayer):
    hand = models.LongStringField()
    is_winner = models.BooleanField(initial=False)


class WaitToPlay(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        players = group.get_players()
        deck = list(DECK)
        random.shuffle(deck)
        for p in players:
            p.hand = json.dumps(deck[:8])
            deck = deck[8:]
        group.stock = json.dumps(deck)


def is_legal(card, current_card):
    return (
        current_card == ''
        or card[0] == current_card[0]
        or card[1] == current_card[1]
        or card[0] == '8'
    )


def increment_turn(group: Group):
    group.whose_turn += 1
    if group.whose_turn > C.PLAYERS_PER_GROUP:
        group.whose_turn = 1


def live_method(player: Player, data):
    group = player.group
    my_id = player.id_in_group
    hand = json.loads(player.hand)

    current_card = group.current_card
    msg_type = data['type']

    if msg_type != 'load':
        if my_id != group.whose_turn:
            return {my_id: dict(type='error', msg='Not your turn')}

        if msg_type == 'move':
            card = data['move']
            if card in hand and is_legal(card, current_card):
                hand.remove(card)
                group.current_card = card
                if not hand:
                    player.is_winner = True
                    return {0: dict(finished=True)}
                player.hand = json.dumps(hand)
                increment_turn(group)

        if msg_type == 'stock':
            stock = json.loads(group.stock)
            if stock:
                card = stock.pop()
                group.stock = json.dumps(stock)
                player.hand = json.dumps(hand + [card])
            else:
                # if the stock is empty, just pass to the next player
                increment_turn(group)

    players = group.get_players()
    card_counts = [[p.id_in_group, len(json.loads(p.hand))] for p in players]
    return {
        p.id_in_group: dict(
            whose_turn=group.whose_turn,
            hand=json.loads(p.hand),
            starter=group.current_card,
            card_counts=card_counts,
        )
        for p in players
    }


class Play(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(
            NUMBERS_TO_CODEPOINTS=NUMBERS_TO_CODEPOINTS,
            SUITS_TO_CODEPOINTS=SUITS_TO_CODEPOINTS,
            my_id=player.id_in_group,
        )

    live_method = live_method


class Results(Page):
    pass


page_sequence = [WaitToPlay, Play, Results]
