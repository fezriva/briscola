from classi import *
from random import *
from AIscripted import *


#creo il mazzo

def nuovoMazzo():
    quadri = [Carta(i+1, 'Quadri') for i in range(10)]
    picche = [Carta(i+1, 'Picche') for i in range(10)]
    cuori = [Carta(i+1, 'Cuori') for i in range(10)]
    fiori = [Carta(i+1, 'Fiori') for i in range(10)]

    mazzo = quadri + picche + cuori + fiori

    shuffle(mazzo)
    return mazzo



#funzione di briscola

def Briscola(mazzo, g1, g2):
    briscola = mazzo.pop(0)

    for carta in mazzo:
        if carta.seme == briscola.seme:
            carta.bri = 1
    for carta in g1:
        if carta.seme == briscola.seme:
            carta.bri = 1
    for carta in g2:
        if carta.seme == briscola.seme:
            carta.bri = 1

    mazzo.append(briscola)


#funzione changeCurr

def changeCurr(seme, gioc):
    if seme == 0:
        for i in range(len(gioc.mano)):
            gioc.mano[i].cambia_curr(0)
    else:
        for i in range(len(gioc.mano)):
            if seme == gioc.mano[i].seme:
                gioc.mano[i].cambia_curr(1)

#funzione iniz

def inizializzaPartita(mazzo, giocatore1, giocatore2, count):

    if count % 2 == 0:
        giocatore2.changeStarter(1)
        for i in range(3):
            giocatore2.mano.append(mazzo.pop(0))
            giocatore1.mano.append(mazzo.pop(0))
    else:
        giocatore1.changeStarter(1)
        for i in range(3):
            giocatore1.mano.append(mazzo.pop(0))
            giocatore1.mano.append(mazzo.pop(0))


    Briscola(mazzo, giocatore1.mano, giocatore2.mano)

#condizioniVittoria

def condizioniVittoria(carta1, carta2):
    if carta1.bri > carta2.bri:
        return True
    elif carta1.bri == carta2.bri:
        if carta1.bri == 1:
            if carta1.val > carta2.val:
                return True
            elif carta1.val == carta2.val:
                if carta1.num > carta2.num:
                    return True
        elif carta1.bri == 0:
            if carta1.curr == carta2.curr:
                if carta1.val > carta2.val:
                    return True
                elif carta1.val == carta2.val:
                    if carta1.num > carta2.num:
                        return True
            elif carta1.curr > carta2.curr:
                return True
    else:
        return False

#funzione gioca

def gioca(mazzo, gioc1, gioc2):

    if gioc1.ai == 0:
        if gioc2 == 0:
            print ('\n', gioc1.nome, 'In mano hai\n')
            for i in range(len(gioc1.mano)):
                print ('(',i+1,') ', gioc1.mano[i].num, 'di', gioc1.mano[i].seme)
            print('\n')
            num = 4
            while num > 3:
                num = int(input('Quale carta usi? (1/2/3) '))
            cartaScelta = gioc1.mano.pop(num-1)
            gioc1.tavolo.append(cartaScelta)
            gioc1.tavolo[0].cambia_curr(1)
        else:
            changeCurr(gioc2.tavolo[0].seme, gioc1)
            print ('\n', gioc1.nome, 'In mano hai\n')
            for i in range(len(gioc1.mano)):
                print ('(',i+1,') ', gioc1.mano[i].num, 'di', gioc1.mano[i].seme)
            print('\n')
            num = 4
            while num > 3:
                num = int(input('Quale carta usi? (1/2/3) '))
            cartaScelta = gioc1.mano.pop(num-1)
            gioc1.tavolo.append(cartaScelta)

    elif gioc1.ai == 1:
        if gioc2 != 0:
            changeCurr(gioc2.tavolo[0].seme, gioc1)

        AIscripted(gioc1, gioc2)



#funzione partita

def partita(giocatore1, giocatore2, count):

    mazzo = nuovoMazzo()

    inizializzaPartita(mazzo, giocatore1, giocatore2, count)
    pene = mazzo[len(mazzo)-1]

    while len(giocatore1.mano) > 0 and len(giocatore2.mano) > 0:

        seghe = int(len(mazzo)/2 + len(giocatore1.mano))
        print('\n############################################################\n')
        print('\nBriscola:', pene.num, 'di', pene.seme)
        print('Rimangono ancora', seghe, 'mani da giocare\n')

        if giocatore1.starter == 1:
            gioca(mazzo, giocatore1, 0)
            gioca(mazzo, giocatore2, giocatore1)
        elif giocatore2.starter == 1:
            gioca(mazzo, giocatore2, 0)
            gioca(mazzo, giocatore1, giocatore2)

        if condizioniVittoria(giocatore1.tavolo[0], giocatore2.tavolo[0]) == True:
            #mo qui ci devo mettere tutte le robe che succedono quando uno vince
            carta1 = giocatore1.tavolo.pop(0)
            carta2 = giocatore2.tavolo.pop(0)
            giocatore1.cambia_Punteggio(carta1.val, carta2.val)

            if len(mazzo) > 0:
                giocatore1.mano.append(mazzo.pop(0))
                giocatore2.mano.append(mazzo.pop(0))
            giocatore2.changeStarter(0)
            giocatore1.changeStarter(1)

            print('\nMano vinta da', giocatore1.nome, '\n')
            print('Si prosegue con la prossima mano\n')
        else:
            carta1 = giocatore1.tavolo.pop(0)
            carta2 = giocatore2.tavolo.pop(0)
            giocatore2.cambia_Punteggio(carta1.val, carta2.val)

            if len(mazzo) > 0:
                giocatore2.mano.append(mazzo.pop(0))
                giocatore1.mano.append(mazzo.pop(0))
            giocatore2.changeStarter(1)
            giocatore1.changeStarter(0)

            print('\nMano vinta da', giocatore2.nome, '\n')
            print('Si prosegue con la prossima mano\n')

        for i in range(len(giocatore1.tavolo)):
            giocatore1.tavolo.pop()
        for i in range(len(giocatore2.tavolo)):
            giocatore2.tavolo.pop()
        changeCurr(0, giocatore1)
        changeCurr(0, giocatore2)

    if giocatore1.punti > giocatore2.punti:
        print('\n\nVINCE IL MATCH', giocatore1.nome, '... COMPLIMENTI!\n')
        print('Punti:', giocatore1.punti, '/', giocatore2.punti)
    elif giocatore2.punti > giocatore1.punti:
        print('\n\nVINCE IL MATCH', giocatore2.nome, '... COMPLIMENTI!')
        print('Punti:', giocatore2.punti, '/', giocatore1.punti)
    else:
        print('Il match termina con un incredibile pareggio!')
