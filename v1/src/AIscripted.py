from classi import *


def popCard(gioc, carta):
    num = len(gioc.mano)
    for i in range(num):
        if carta == gioc.mano[i-1]:
            gioc.mano.pop(i-1)
    gioc.tavolo.append(carta)

#funzione carta piu` bassa

def cartaBassa(mazzo):
    possibili = sorted(mazzo, key = lambda x: (x.val, x.bri, x.num))
    return possibili[0]

#funzione strozza

def strozza (gioc1, gioc2):
    possibili = []
    for i in range(len(gioc1.mano)):
        if gioc1.mano[i].val > gioc2.tavolo[0].val and gioc1.mano[i].seme == gioc2.tavolo[0].seme:
            possibili.append(gioc1.mano[i])
    sorted(possibili, key = lambda x: x.val)
    return possibili

#funzione stronzo

def stronzo (mazzo):
    possibili = []
    for i in mazzo:
        if i.val <= 4 and i.bri ==1:
            possibili.append(i)
    sorted(possibili, key = lambda x: x.val)
    return possibili

#funzione AIscripted

def AIscripted(gioc1, gioc2):
    if gioc2 == 0 or (0 < gioc2.tavolo[0].val <=4 and gioc2.tavolo[0].bri == 1):
        carta = cartaBassa(gioc1.mano)
        popCard(gioc1, carta)
        if gioc2 == 0:
            gioc1.tavolo[0].cambia_curr(1)

    elif (gioc2.tavolo[0].val == 0 and gioc2.tavolo[0].bri == 0):
        carte = strozza(gioc1, gioc2)
        if len(carte) > 0:
            popCard(gioc1, carte[0])
        else:
            carta = cartaBassa(gioc1.mano)
            popCard(gioc1, carta)

    elif 0 < gioc2.tavolo[0].val <= 4 and gioc2.tavolo[0].bri == 0:
        carte = strozza(gioc1, gioc2)
        if len(carte) > 0:
            popCard(gioc1, carte[0])
        else:
            carte2 = stronzo(gioc1.mano)
            if len(carte) > 0:
                popCard(gioc1, carte2[0])
            else:
                carta = cartaBassa(gioc1.mano)
                popCard(gioc1, carta)

    elif gioc2.tavolo[0].val > 4:
        carte = strozza(gioc1, gioc2)
        if len(carte) > 0:
            popCard(gioc1, carte[0])
        else:
            for i in range(len(gioc1.mano)):
                if gioc1.mano[i].bri > gioc2.tavolo[0].bri:
                    gioc1.tavolo.append(gioc1.mano[i])
            sorted(gioc1.tavolo, key = lambda x: x.val)
            if len(gioc1.tavolo) >= 1:
                while len(gioc1.tavolo) > 1:
                    gioc1.tavolo.pop()
            else:
                carta = cartaBassa(gioc1.mano)
                popCard(gioc1, carta)

    print(gioc1.nome, 'gioca un', gioc1.tavolo[0].num, 'di', gioc1.tavolo[0].seme)
