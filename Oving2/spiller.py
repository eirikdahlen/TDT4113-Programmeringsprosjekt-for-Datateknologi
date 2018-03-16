import random
import matplotlib.pyplot as plt

class Spiller:

    MULIGE_VALG = {0: 'stein', 1: 'saks', 2: 'papir'}
    resultater = {}
    beats_whomstvdvst = {0: 2, 1: 0, 2: 1}

    def __init__(self, playerName):
        self.name = playerName
        Spiller.resultater[self] = []

    def velg_aksjon(self):
        return

    def motta_resultat(self, motstander, trekk):
        Spiller.resultater[motstander].append(trekk)

    def oppgi_navn(self):
        return self.__class__.__name__

    def __str__(self):
        return self.name

#----------------------------------------------------------------------------------------

class Action:

    def __init__(self, valg):
        self.valg = valg

    def __eq__(self, other):
        return self.valg == other.valg

    def __gt__(self, other):
        BEATS = {0: 2, 1: 0, 2: 1}
        return BEATS[self.valg] != other.valg

    def __str__(self):
        return Spiller.MULIGE_VALG[self.valg]

    def __repr__(self):
        return Spiller.MULIGE_VALG[self.valg]

    def getAction(self):
        return self.valg

#----------------------------------------------------------------------------------------

class TilfeldigSpiller(Spiller):

    def __init__(self, playerName):
        Spiller.__init__(self, playerName)

    def velg_aksjon(self, a):
        return Action(random.randint(0,2))

#----------------------------------------------------------------------------------------

class SekvensiellSpiller(Spiller):

    def __init__(self, playerName):
        Spiller.__init__(self, playerName)
        self.seq_count = 0

    def velg_aksjon(self, a):
        i = self.seq_count % 3
        valg = Action(i)
        self.seq_count += 1
        return valg

#----------------------------------------------------------------------------------------

class MestVanligSpiller(Spiller):

    def __init__(self, playerName):
        Spiller.__init__(self, playerName)

    def velg_aksjon(self, motstander):
        #Liste med trekkene denne motstanderen har brukt
        aksjon = Spiller.resultater[motstander]
        if len(aksjon) == 0:
            return Action(random.randint(0,2))
        stein = aksjon.count(Action(0))
        saks = aksjon.count(Action(1))
        papir = aksjon.count(Action(2))
        list = [stein, saks, papir]
        most_common = list.index(max(list))
        return Action(self.beats_whomstvdvst[most_common])

#----------------------------------------------------------------------------------------

class HistoriskSpiller(Spiller):

    def __init__(self, playerName, husk):
        Spiller.__init__(self, playerName)
        self.husk = husk

    def velg_aksjon(self, motstander):
        aksjon = Spiller.resultater[motstander]
        if len(aksjon) < self.husk:
            return Action(random.randint(0,2))
        last_actions = aksjon[-self.husk:]
        score = [0, 0, 0]
        for i in range(len(aksjon) - 1 - len(last_actions), -1, -1):
            if aksjon[i] == last_actions[-1]:
                if i - len(last_actions) < 0:
                    break
                seq = aksjon[i - len(last_actions) + 1:i+1]
                if seq != last_actions:
                    break
                score[aksjon[i+1].getAction()] += 1
        if max(score) < 1:
            return Action(random.randint(0,2))
        most_common = score.index(max(score))
        return Action(self.beats_whomstvdvst[most_common])

#----------------------------------------------------------------------------------------

class EnkeltSpill:

    def __init__(self, spiller1, spiller2):
        self.spiller1 = spiller1
        self.spiller2 = spiller2
        self.points1 = 0
        self.points2 = 0

    def play(self):
        self.move1 = self.spiller1.velg_aksjon(self.spiller2)
        self.move2 = self.spiller2.velg_aksjon(self.spiller1)
        if self.move1 == self.move2:
            self.points1, self.points2 = 0.5, 0.5
        elif self.move1 > self.move2:
            self.points1, self.points2 = 1, 0
        else:
            self.points2, self.points1 = 1, 0

        self.spiller1.motta_resultat(self.spiller2, self.move2)
        self.spiller2.motta_resultat(self.spiller1, self.move1)

    def winner(self):
        if self.points1 == self.points2:
            return 'Ingen'
        elif self.points1 > self.points2:
            return self.spiller1
        else: return self.spiller2

    def getScore(self): return [self.points1,self.points2]

    def __str__(self):
        return str(self.spiller1) + ": " + str(self.move1) + ". " + str(self.spiller2) + " : " + \
               str(self.move2) + " --> " + str(self.winner()) + " vinner"

#----------------------------------------------------------------------------------------

class MangeSpill:

    def __init__(self, spiller1, spiller2, antall_spill):
        self.s1 = spiller1
        self.s2 = spiller2
        self.antall_spill = antall_spill

    def arranger_enkeltspill(self):
        return EnkeltSpill(self.s1, self.s2)

    def arranger_turnering(self):
        tot_s1 = 0
        tot_s2 = 0
        gevinst_s1 = []
        x_akse = []
        count = 0
        for x in range(0,self.antall_spill):
            enkel = self.arranger_enkeltspill()
            enkel.play()
            score = enkel.getScore()
            tot_s1 += score[0]
            tot_s2 += score[1]

            ##PYPLOT##
            count+=1
            x_akse.append(count)
            gevinst_s1.append(tot_s1/count)

            print(enkel)

        ##PYPLOT##
        plt.plot(x_akse,gevinst_s1)
        plt.axis([0,self.antall_spill,0,1])
        plt.grid(True)
        plt.axhline(y=0.5,linewidth=0.5, color="r")
        plt.xlabel("Antall Spill")
        plt.ylabel("Gevinstprosent: " + str(self.s1))
        plt.show()

        print("\nTotal score i turneringen:\n" + str(self.s1) + ": " + str(tot_s1) + " poeng" +
              "\n" + str(self.s2) + ": " + str(tot_s2) + " poeng")



def main():

    player1 = input("Velg spillertype for spiller1: Historiker, MestVanlig, Sekvensiell eller Tilfeldig: ")
    player2 = input("Velg spillertype for spiller2: Historiker, MestVanlig, Sekvensiell eller Tilfeldig: ")

    if player1 == "Historiker":
        husk = int(input("Du har valgt Historiker, hvor mange trekk skal huskes?"))
        s1 = HistoriskSpiller("HistoriskSpiller", husk)
    elif player1 == "MestVanlig":
        s1 = MestVanligSpiller("MestVanligSpiller")
    elif player1 == "Sekvensiell":
        s1 = SekvensiellSpiller("SekvensiellSpiller")
    elif player1 == "Tilfeldig":
        s1 = TilfeldigSpiller("TilfeldigSpiller")

    if player2 == "Historiker":
        husk = int(input("Du har valgt Historiker, hvor mange trekk skal huskes?"))
        s2 = HistoriskSpiller("HistoriskSpiller", husk)
    elif player2 == "MestVanlig":
        s2 = MestVanligSpiller("MestVanligSpiller")
    elif player2 == "Sekvensiell":
        s2 = SekvensiellSpiller("SekvensiellSpiller")
    elif player2 == "Tilfeldig":
        s2 = TilfeldigSpiller("TilfeldigSpiller")
    spill = int(input("Hvor mange spill? "))

    mange = MangeSpill(s1,s2,spill)
    mange.arranger_turnering()


main()












