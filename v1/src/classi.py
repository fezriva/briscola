# definisco classi: carta con specifiche che mi servono
# e giocatore che mi da la mano in partita e se e` umano o PC

class Carta:
    bri = 0
    curr = 0

    def __init__(self, n, s):
        self.num = n
        self.seme = s

        if self.num == 1:
            self.val = 11
        elif self.num == 3:
            self.val = 10
        elif self.num == 8:
            self.val = 2
        elif self.num == 9:
            self.val = 3
        elif self.num == 10:
            self.val = 4
        else:
            self.val = 0

    def cambia_briscola(self, s):
        self.bri = s

    def cambia_curr(self, s):
        self.curr = s


class Giocatore:

    starter = 0
    punti = 0

    def __init__(self, n):
        self.nome = n
        self.mano = []
        self.tavolo = []
        if self.nome.upper() == 'PC':
            self.ai = 1
        else:
            self.ai = 0

    def cambia_Punteggio(self, s, d):
        self.punti = self.punti + s + d

    def changeStarter(self, i):
        self.starter = i
