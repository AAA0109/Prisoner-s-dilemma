from os import environ

SESSION_CONFIGS = [
    dict(
        name='baseline',
        display_name="Prisoner's Dilemma (Baseline)",
        num_demo_participants=2,
        app_sequence=['prisonerdilemma', 'question'],
        mode=0,
        doc = """
        Prisoner's Dilemma (Baseline)
        """,
        completionlink='https://app.prolific.co/submissions/complete?cc=CKZZ522T'
    ),
    dict(
        name='opaque',
        display_name="Prisoner's Dilemma (Opaque)",
        num_demo_participants=2,
        app_sequence=['prisonerdilemma', 'question'],
        mode=1,
        doc = """
        Prisoner's Dilemma (Opaque)
        """,
        completionlink='https://app.prolific.co/submissions/complete?cc=CKZZ522T'
    ),
    dict(
        name='transparent',
        display_name="Prisoner's Dilemma (Transparent)",
        num_demo_participants=2,
        app_sequence=['prisonerdilemma', 'question'],
        mode=2,
        doc = """
        Prisoner's Dilemma (Transparent)
        """,
        completionlink='https://app.prolific.co/submissions/complete?cc=CKZZ522T'
    ),
]

ROOMS = [
    # dict(
    #     name='econ101',
    #     display_name='Econ 101 class',
    #     participant_label_file='_rooms/econ101.txt',
    # ),
    dict(name='experiment1', display_name='Room for Baseline'),
    dict(name='experiment2', display_name='Room for Opaque'),
    dict(name='experiment3', display_name='Room for Transparent'),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=0.6, participation_fee=0.00, doc="")

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """
DEMO_PAGE_TITLE = "More demos of oTree (especially using live pages)"

SECRET_KEY = '4387860144726'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

PARTICIPANT_FIELDS = [
    'choice',
    'other_choice',
    'start_time',
    'end_time',
    'total_spent',
    'finished'
]

SESSION_FIELDS = ['finished_p1_list', 'iowa_costs', 'wisconsin', 'intergenerational_history']