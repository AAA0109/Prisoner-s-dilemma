from os import environ

SESSION_CONFIGS = [
    # dict(
    #     name='prisonerdilemma',
    #     display_name="Prisoner's Dilemma",
    #     num_demo_participants=4,
    #     app_sequence=['prisonerdilemma', 'question'],
    # ),
    dict(
        name='baseline',
        display_name="Prisoner's Dilemma (Baseline)",
        num_demo_participants=2,
        app_sequence=['baseline', 'question'],
    ),
    dict(
        name='opaque',
        display_name="Prisoner's Dilemma (Opaque)",
        num_demo_participants=2,
        app_sequence=['opaque', 'question'],
    ),
    dict(
        name='transparent',
        display_name="Prisoner's Dilemma (Transparent)",
        num_demo_participants=2,
        app_sequence=['transparent', 'question'],
    ),
    # dict(
    #     name='question',
    #     display_name="Questionnaire",
    #     num_demo_participants=20,
    #     app_sequence=['question'],
    # ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1.00, participation_fee=0.00, doc="")

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """
DEMO_PAGE_TITLE = "More demos of oTree (especially using live pages)"

SECRET_KEY = '4387860144726'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

PARTICIPANT_FIELDS = [
    'booking_time',
    'cards',
    'order',
    'reaction_times',
    'read_mind_in_eyes_score',
    'responses',
    'stimuli',
    'svo_angle',
    'svo_category',
]

SESSION_FIELDS = ['finished_p1_list', 'iowa_costs', 'wisconsin', 'intergenerational_history']