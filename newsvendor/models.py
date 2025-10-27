from otree.api import *
import random  # This line is missing in your current code
import math

class C(BaseConstants):
    NAME_IN_URL = 'newsvendor'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 30
    PRICE = 100
    COST = 60
    DEMAND_MIN = 50
    DEMAND_MAX = 150
    PHI = 0.3
    ALPHA = 1.0
    PRACTICE_ROUNDS = 0
    DECISION_TIMEOUT = 25

class Subsession(BaseSubsession):
    def creating_session(self):
        cfg = self.session.config
        C.PRICE = cfg.get('price', C.PRICE)
        C.COST = cfg.get('cost', C.COST)
        C.DEMAND_MIN = cfg.get('dmin', C.DEMAND_MIN)
        C.DEMAND_MAX = cfg.get('dmax', C.DEMAND_MAX)
        C.PHI = cfg.get('phi', C.PHI)
        C.ALPHA = cfg.get('alpha', C.ALPHA)
        C.PRACTICE_ROUNDS = cfg.get('practice_rounds', C.PRACTICE_ROUNDS)

class Group(BaseGroup):
    demand = models.IntegerField()

    def set_demand_once(self):
        self.demand = random.randint(C.DEMAND_MIN, C.DEMAND_MAX)

    def settle_spillover_and_payoffs(self):
        p1, p2 = self.get_players()
        d = self.demand
        phi = self.session.config.get('phi', C.PHI)

        unmet1 = max(0, d - p1.order_qty)
        unmet2 = max(0, d - p2.order_qty)

        spill_to_1 = math.floor(phi * unmet2)
        spill_to_2 = math.floor(phi * unmet1)

        p1.sales = min(p1.order_qty, d + spill_to_1)
        p2.sales = min(p2.order_qty, d + spill_to_2)

        p1.unsold = p1.order_qty - p1.sales
        p2.unsold = p2.order_qty - p2.sales
        p1.stockout = int(p1.sales == p1.order_qty)
        p2.stockout = int(p2.sales == p2.order_qty)

        p, c = C.PRICE, C.COST
        p1.profit = p * p1.sales - c * p1.order_qty
        p2.profit = p * p2.sales - c * p2.order_qty
        p1.payoff = p1.profit
        p2.payoff = p2.profit

class Player(BasePlayer):
    # Participant information fields
    age_group = models.StringField()
    education_background = models.StringField()
    prior_experience = models.StringField()
    risk_attitude = models.IntegerField()

    order_qty = models.IntegerField(label='Enter your order quantity', min=0)
    demand = models.IntegerField()
    sales = models.IntegerField()
    unsold = models.IntegerField()
    stockout = models.IntegerField()
    profit = models.CurrencyField()

    decision_time = models.FloatField()
    is_practice = models.BooleanField(initial=False)

    competitor_profit = models.CurrencyField()
    pct_vs_comp = models.FloatField()

    @staticmethod
    def q_star_uniform_critical_ratio():
        return 50 + 0.4 * (150 - 50)

    def default_order_if_timeout(self):
        if self.order_qty is None:
            self.order_qty = int(round(self.q_star_uniform_critical_ratio()))
