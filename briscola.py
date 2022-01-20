
from funzioni import *
from classi import *


#main
print('\n\nBenvenuto! Qui puoi giocare a briscola direttamente da terminale, pensa che figo!')

gioco = input('Allora, vuoi giocare? (Y/N) ')

if gioco.lower() == 'y':
    print('Magnifico!')
    print('\nSi gioca in 2, anche contro il PC! Ti bastera` infatti nominare uno dei due giocatori \'PC\'')
    print('\nBuon divertimento!\n\n')

    nome1 = input('Inserisci il nome del Giocatore 1: ')
    nome2 = input ('Inserisci il nome del Giocatore 2: ')

    giocatore1 = Giocatore(nome1)
    giocatore2 = Giocatore(nome2)


    print('Gli sfidanti sono', giocatore1.nome, 'e', giocatore2.nome, '\n')

    count = 1

    while gioco.lower() == 'y':
        count += 1
        partita(giocatore1, giocatore2, count)
        print("\n")
        gioco = input('Vuoi giocare ancora? (Y/N) ')

print('A presto!!')
