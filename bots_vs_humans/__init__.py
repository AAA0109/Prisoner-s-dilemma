from otree.api import *

doc = """
Humans vs. bots.

This is a public goods game where you play against 2 bots.
The bots use a tit-for-tat strategy with some random noise.

Note: this doesn't use oTree test bots, but rather an ExtraModel.
It's simply a single-player game where random calculations are done on the server.
You never need to open any links for the bots. 
"""


class C(BaseConstants):
    NAME_IN_URL = 'bots_vs_humans'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5
    ENDOWMENT = cu(100)
    MULTIPLIER = 1.8
    MAX_NOISE = 10
    BOTS_PER_GROUP = 2
    AGENTS_PER_GROUP = BOTS_PER_GROUP + 1


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        for i in range(C.BOTS_PER_GROUP):
            MyBot.create(player=p, agent_id=i + 1)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    contrib = models.CurrencyField(
        min=0, max=C.ENDOWMENT, label="How much will you contribute?"
    )

    agent_id = models.IntegerField(initial=1)
    group_total_contrib = models.CurrencyField()
    group_individual_share = models.CurrencyField()


class MyBot(ExtraModel):
    player = models.Link(Player)

    # these fields should match what's defined on the Player, so that you can
    # loop over player and bot instances interchangeably.
    contrib = models.CurrencyField(
        min=0, max=C.ENDOWMENT, label="How much will you contribute?"
    )
    payoff = models.CurrencyField()
    # replacement for id_in_group
    agent_id = models.IntegerField()


def generate_contrib(mean):
    import random

    contrib = mean + random.randint(-C.MAX_NOISE, C.MAX_NOISE)
    # constrain it between 0 and endowment
    return max(0, min(contrib, C.ENDOWMENT))


def get_agents(player: Player):
    """'Agent' means either a bot or a human. This gets the user plus all bots"""
    return [player] + MyBot.filter(player=player)


# FUNCTIONS
def set_payoffs(player: Player):
    bots = MyBot.filter(player=player)

    if player.round_number == 1:
        mean = C.ENDOWMENT / 2
    else:
        # tit-for-tat strategy based on last round actions.
        prev_player = player.in_round(player.round_number - 1)
        mean = prev_player.contrib
    for bot in bots:
        bot.contrib = generate_contrib(mean)
    agents = bots + [player]
    contribs = [p.contrib for p in agents]
    player.group_total_contrib = sum(contribs)
    player.group_individual_share = (
        player.group_total_contrib * C.MULTIPLIER / C.AGENTS_PER_GROUP
    )

    for ag in agents:
        ag.payoff = C.ENDOWMENT - ag.contrib + player.group_individual_share


# PAGES
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contrib']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        set_payoffs(player)


class WaitForBots(Page):
    """
    This is just for show, to make it feel more realistic.
    Also, note it's a Page, not a WaitPage.
    Removing this page won't affect functionality.
    """

    @staticmethod
    def get_timeout_seconds(player: Player):
        import random

        return random.randint(1, 5)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(agents=get_agents(player))


page_sequence = [Contribute, WaitForBots, Results]
