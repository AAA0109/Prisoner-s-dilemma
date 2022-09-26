from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'image_annotation'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    decision = models.StringField(
        widget=widgets.RadioSelect,
        label="Based on this chart, what country would you say is the best to live in?",
        choices=['USA', 'Switzerland', 'Australia', 'Canada', 'Other'],
    )
    annotations = models.LongStringField()
    image_path = models.StringField()


class Annotation(ExtraModel):
    player = models.Link(Player)
    image_name = models.StringField()
    text = models.StringField()
    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()


class Decide(Page):
    form_model = 'player'
    form_fields = ['decision', 'annotations']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import json

        annos = json.loads(player.annotations)
        for anno in annos:
            geometry = anno['shapes'][0]['geometry']
            image_name = anno['src'].split('/')[-1]
            Annotation.create(player=player, image_name=image_name, text=anno['text'], **geometry)
        # here we delete the annotations JSON to reduce bloat in the data export.
        # but you can remove this line if you want e.g. to re-display the annotations
        # on a separate page.
        player.annotations = ''


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(annotations=Annotation.filter(player=player))


page_sequence = [
    Decide,
    Results,
]


def custom_export(players):
    yield [
        'session_code',
        'participant_code',
        'image_name',
        'text',
        'x',
        'y',
        'width',
        'height',
    ]
    for p in players:
        pp = p.participant
        session_code = pp.session.code
        for anno in Annotation.filter(player=p):
            yield [
                session_code,
                pp.code,
                anno.image_name,
                anno.text,
                anno.x,
                anno.y,
                anno.width,
                anno.height,
            ]
