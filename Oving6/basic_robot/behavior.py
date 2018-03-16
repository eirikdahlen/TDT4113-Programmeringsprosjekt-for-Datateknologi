
class Behavior:
    # Superklasse for behaviors
    # Hovedoppgave:
    #   - sjekke om behavior er aktiv eller deaktiv
    #   - produsere motor-anbefalinger
    #   - oppdatere match-degree
    #   - OBS: ikke kommunisere direkte med andre behaviors!

    def __init__(self, bbcon, priority):
        self.bbcon = bbcon  # peker til kontrolleren som bruker denne behavioren
        self.sensor = None  # sensoren som brukes settes av den enkelte behavioren
        self.motor_recommendation = []  # liste med anbefalinger for denne behavioren, en per motob
        self.active_flag = False  # indikerer om behavioren er aktiv eller inaktiv
        self.halt_request = False  # noen behaviors kan be om at roboten stopper all aktivitet
        self.priority = priority  # en statisk, predefinert verdi som indikerer viktigheten av denne behavioren
        self.match_degree = 0  # in range (0,1)
        self.weight = self.priority * self.match_degree


    # hver behavior har egne tester for bli aktiv eller inaktiv
    def consider_activation(self):
        return


    def update(self):
        # oppdaterer aktivitet-statusen til behavioren
        if self.active_flag:
            self.active_flag = not self.consider_deactivation()
        else:
            self.active_flag = self.consider_activation()
        if self.active_flag:
            self.sense_and_act()
            self.weight = self.priority * self.match_degree # oppdaterer vekten til behavioren

    def sense_and_act(self):
        #  hver behavior bruker sensob til å produsere motor-anbefalinger (og stopp-forespørsler)
        return
