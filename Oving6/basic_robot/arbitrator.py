import random
__author__ = "Axel Harstad"


class Arbitrator:
    def __init__(self, bbcon, stochastic=False):
        self.bbcon = bbcon
        self.stochastic = stochastic

    def choose_action(self):
        # Sjekker active_behaviors
        # Velger en vinner
        weight = -1
        #winner = self.bbcon.active_behaviors[0]
        winner = None
        # Her velges handlingen med størst vekt
        #if not self.stochastic:

        for behavior in self.bbcon.behaviors:
            if behavior.active_flag:
                print(behavior)
                if behavior.weight > weight:
                    weight = behavior.weight
                    winner = behavior
        # Her velges handlingen noe tilfeldig
        # Større vekt gir større sannsynlighet for å bli valgt
        #else:
        #    intervals = []
        #    pre_int_end = 0
        #    for behavior in self.bbcon.active_behaviors:
        #        this_int_end = pre_int_end + behavior.weight
        #        intervals.append(this_int_end)
        #        pre_int_end = this_int_end
        #    limit = intervals[-1]
        #    random_decimal = random.randint(0, limit*100)/100
        #    for i in range(len(intervals)):
        #        if random_decimal < intervals[i]:
        #            winner = self.bbcon.active_behaviors[i]

        # Sjekker til slutt om den vinnende behavioren kommer med en forespørsel om å stoppe roboten fullstendig

        if winner is None or winner.halt_request:
            return ['S', 0], True
        return winner.motor_recommendation, False
