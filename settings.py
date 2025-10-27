from os import environ


SESSION_CONFIGS = [
    dict(
        name='NV_a1_phi03',
        display_name='Newsvendor (α=1, φ=0.3)',
        num_demo_participants=2,
        app_sequence=['newsvendor'],
        price=100, cost=60, dmin=50, dmax=150, phi=0.3, alpha=1.0,
        rounds=30, practice_rounds=0
    ),
    dict(
        name='NV_a1_phi06',
        display_name='Newsvendor (α=1, φ=0.6)',
        num_demo_participants=2,
        app_sequence=['newsvendor'],
        price=100, cost=60, dmin=50, dmax=150, phi=0.6, alpha=1.0,
        rounds=30, practice_rounds=0
    ),
    dict(
        name='NV_a05_phi03',
        display_name='Newsvendor (α=0.5, φ=0.3)',
        num_demo_participants=2,
        app_sequence=['newsvendor'],
        price=100, cost=60, dmin=50, dmax=150, phi=0.3, alpha=0.5,
        rounds=30, practice_rounds=0
    ),
    dict(
        name='NV_a05_phi06',
        display_name='Newsvendor (α=0.5, φ=0.6)',
        num_demo_participants=2,
        app_sequence=['newsvendor'],
        price=100, cost=60, dmin=50, dmax=150, phi=0.6, alpha=0.5,
        rounds=30, practice_rounds=0
    ),
    dict(
        name='NV_a0_phi03',
        display_name='Newsvendor (α=0, φ=0.3)',
        num_demo_participants=2,
        app_sequence=['newsvendor'],
        price=100, cost=60, dmin=50, dmax=150, phi=0.3, alpha=0.0,
        rounds=30, practice_rounds=0
    ),
    dict(
        name='NV_a0_phi06',
        display_name='Newsvendor (α=0, φ=0.6)',
        num_demo_participants=2,
        app_sequence=['newsvendor'],
        price=100, cost=60, dmin=50, dmax=150, phi=0.6, alpha=0.0,
        rounds=30, practice_rounds=0
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '3385855954303'

INSTALLED_APPS = ['otree']