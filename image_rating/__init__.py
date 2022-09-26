from otree.api import *


doc = """
Rating images (WTP/willingness to pay)
"""


def read_csv():
    import csv

    f = open(__name__ + '/catalog.csv', encoding='utf-8-sig')
    rows = [row for row in csv.DictReader(f)]
    for row in rows:
        row['image_path'] = 'grocery/{}.png'.format(row['image_png'])

    return rows


class C(BaseConstants):
    NAME_IN_URL = 'image_rating'
    PLAYERS_PER_GROUP = None
    PRODUCTS = read_csv()
    NUM_ROUNDS = len(PRODUCTS)


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        img = get_current_product(p)
        p.sku = img['sku']


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sku = models.StringField()
    willingness_to_pay = models.CurrencyField(label="", min=0)


def get_current_product(player: Player):
    return C.PRODUCTS[player.round_number - 1]


class MyPage(Page):
    form_model = 'player'
    form_fields = ['willingness_to_pay']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(product=get_current_product(player))


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [MyPage, Results]
