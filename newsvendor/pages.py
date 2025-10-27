from otree.api import *
import time
from .models import *

class BackgroundForm(Page):
    form_model = 'player'  # Store responses in Player model fields (if needed)
    form_fields = []  # No need to bind fields here, as it is a background form

    def is_displayed(self):
        # Only show BackgroundForm in round 1
        return self.round_number == 1

    def vars_for_template(player: Player):
        # You can add additional logic to pass other variables if needed
        return {}

class Decision(Page):
    form_model = 'player'
    form_fields = ['order_qty']
    timeout_seconds = C.DECISION_TIMEOUT

    def vars_for_template(player: Player):
        is_practice = player.round_number <= C.PRACTICE_ROUNDS
        player.is_practice = is_practice
        player.participant.vars['t_start'] = time.time()

        # Get phi and alpha from session config
        phi = player.session.config.get('phi', C.PHI)
        alpha = player.session.config.get('alpha', C.ALPHA)

        return dict(
            price=C.PRICE, cost=C.COST, dmin=C.DEMAND_MIN, dmax=C.DEMAND_MAX,
            phi=phi, alpha=alpha, phi_pct=int(round(phi * 100)),
            is_practice=is_practice
        )

    def before_next_page(player: Player, timeout_happened):
        t0 = player.participant.vars.get('t_start')
        if t0:
            player.decision_time = time.time() - t0
        if timeout_happened:
            player.default_order_if_timeout()

def compute(group: Group):
    # ONE draw per pair per round
    group.set_demand_once()
    d = group.demand

    # Store same demand on both players
    for p in group.get_players():
        p.demand = d

    # Payoffs with spillover
    group.settle_spillover_and_payoffs()

    # Competitor comparisons
    p1, p2 = group.get_players()
    p1.competitor_profit = p2.profit
    p2.competitor_profit = p1.profit

    def pct(a, b):
        a = float(a or 0); b = float(b or 0)
        if b == 0:
            return 0.0 if a == 0 else 100.0
        return 100.0 * (a - b) / abs(b)

    p1.pct_vs_comp = pct(p1.profit, p1.competitor_profit)
    p2.pct_vs_comp = pct(p2.profit, p2.competitor_profit)

class ComputeRound(WaitPage):
    after_all_players_arrive = 'compute'

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        alpha = player.session.config.get('alpha', C.ALPHA)
        phi = player.session.config.get('phi', C.PHI)

        show_comp_profit = (alpha <= 0.5)
        show_pct_text = (alpha == 0)
        higher = 'higher' if player.pct_vs_comp >= 0 else 'lower'
        pct_abs = abs(round(player.pct_vs_comp, 1))

        return dict(
            alpha=alpha, phi=phi,
            q=player.order_qty, d=player.demand,
            sales=player.sales, unsold=player.unsold,
            profit=player.profit,
            comp_profit=player.competitor_profit,
            show_comp_profit=show_comp_profit,
            show_pct_text=show_pct_text,
            comparison_text=f'Your profit this round was {pct_abs}% {higher} than your competitor’s.'
        )

page_sequence = [BackgroundForm, Decision, ComputeRound, Results]
