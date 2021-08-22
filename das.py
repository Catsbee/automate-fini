# -*- coding: utf-8 -*-
"""
Created on Tue May  5 18:55:46 2020

@author: lione
"""


class Af:
    """Classe définissant un automate fini caractérisé par :
    - son nbr de symboles dans l'alphabet
    - son nbr d'états initiaux suivis de ses états initiaux
    - son nbr d'états terminaux suivis de ses états terminaux
    - sa table de transition"""

    def __init__(self):  # Notre méthode constructeur
        """Constructeur de notre classe. Chaque attribut va être instancié
        avec une valeur par défaut"""
        self.nb_symboles = 0
        self.nb_etats = 0
        self.nb_etats_init = 0
        self.nb_etats_ter = 0
        self.etats_init = []
        self.etats_ter = []
        self.nb_transit = 0
        self.table_transit = [[]]

# ------------------------- FONCTION AFFICHAGE-------------------#
def display(t):
    for row in t:
        for element in row:
            print(element, "\t", end="")
        print("\n")


def nettoyage(liste):

    for i in range(0, len(liste)):
        liste[i] = liste[i].replace(" ", "")


def lire_automate_sur_fichier(nom_fichier):
    test = open(nom_fichier, "r")
    liste = test.read().splitlines()  # lis le fichier et enlève les \n
    test.close()

    i = 1
    cpt = 0
    nettoyage(liste)
    a = Af()
    for line in liste:  # on parcourt le tableau ligne par ligne
        # pour afficher les etats initiaux et terminaux comme nous connaissons deja leur place dans le fichier
        if i == 1:
            a.nb_symboles = int(line)
        if i == 2:
            a.nb_etats = int(line)
        if i == 3:
            a.nb_etats_init = int(line[0])  # nbr d'etats init tjrs en premiere place de la ligne
            cpt = 1
            while cpt <= a.nb_etats_init:
                a.etats_init += line[cpt]  # en fct du nbr d'etats init on fait tourner une boucle pour les stocker
                cpt += 1
        if i == 4:
            a.nb_etats_ter = int(line[0])  # nbr d'etats terminaux tjrs en premiere place de la ligne
            cpt = 1
            while cpt <= a.nb_etats_ter:
                a.etats_ter += line[cpt]
                cpt += 1

# ------------- CREATION ET INITIALISATION DE LA TABLE DES TRANSITIONS ---------------- #
        if i == 5:
            a.nb_transit = int(line)
            # creation de la table de transit
            a.table_transit = [[" "] * (a.nb_symboles+2) for i in range(a.nb_etats+1)]
            for y in range(a.nb_symboles):  # creation des noms de colonnes avec les composants de l'alphabet
                a.table_transit[0][y+1] = chr(y+ord('a'))
                a.table_transit[0][y+2] = '*'  # epsilon est mis en derniere colonne
            for y in range(a.nb_etats):
                a.table_transit[y+1][0] = str(y)  # creation de noms des colonnes avec les etats
        if i >= 6:  # quand i >= 6 on traite les transitions de l'automate
            chiffres = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # mise en place des valeurs dans la table
            etat1 = ""
            etat2 = ""
            symbole = ""
            x = 0
            while line[x] in chiffres:  # on regarde le premier etat de la transition
                etat1 += line[x]  # stockage dans etat1
                x += 1
            symbole = line[x]  # stockage du symbole dans symbole
            x += 1
            while (x < len(line)):  # on peut rentrer dans cette boucle uniquement si la ligne contient 3 'parties'
                if(line[x] in chiffres):  # on regarde quel est le dernier etat de la transition
                    etat2 += line[x]
                x += 1
            if line[1] != '*':  # si le symbole N'EST PAS epsilon
                if a.table_transit[int(etat1)+1][ord(symbole)-ord('a')+1] == " ":
                    a.table_transit[int(etat1)+1][ord(symbole)-ord('a')+1] = etat2
                else:
                    a.table_transit[int(etat1)+1][ord(symbole)-ord('a')+1] += ',' + etat2
            else:  # si le symbole EST epsilon
                if a.table_transit[int(etat1)+1][a.nb_symboles+1] == " ":
                    a.table_transit[int(etat1)+1][a.nb_symboles+1] = etat2
                else:
                    a.table_transit[int(etat1)+1][a.nb_symboles+1] += ',' + etat2
        i += 1
    for i in range(a.nb_etats+1):  # quand case est vide permet d'avoir un '_'
        for j in range(a.nb_symboles+1):
            if a.table_transit[i][j+1] == " ":  # on traite j+1 car j represente le nom des lignes et colonnes
                a.table_transit[i][j+1] = '-'  # premiere ligne du tableau de toute façon

    return a


def afficher_automate(a):
    print(a.nb_etats_init, "etat(s) initial(aux):\n\tI =", a.etats_init)
    print(a.nb_etats_ter, "etat(s) terminal(aux):\n\tI =", a.etats_ter)
    print(a.nb_transit, "transition(s) dont voici la table de transition :\n")
    display(a.table_transit)


# ------------------------ FONCTION DE DETERMINISATION ------------------------ #
def est_un_automate_asynchrone(AF):  
    tab_eps = []
    for transition in AF.table_transit[1:]:
        if (transition[-1] != '-'):
            tab_eps.append(transition[0])
    if tab_eps:
        print("L'automate est asynchrone pour les états :")
        print(tab_eps)
        return True
    else:
        print("L'automate est synchrone")
        return False

def determinisation_et_completion_automate_asynchrone(a):
    print()
    return a


def est_un_automate_deterministe(a):
    b = 0
    i = 1
    print('nombre état initiale', a.etats_init)
    if a.nb_etats_init > 1:
        print('Non deterministe car il y a', a.nb_etats_init, 'etats initiaux')
        return False
    else:
        while i < a.nb_etats+1 and b == 0:
            j = 1
            while j < a.nb_symboles+1 and b == 0:
                temp = a.table_transit[i][j]
                if len(temp) > 1:
                    b = 1
                j += 1
            i += 1
    if b == 1:
        print('Non determinsite car il y a plus d une transtion sur état', a.nb_états-1)
        return False
    else:
        print("deterministe")
        return True


def est_un_automate_complet(AF):
    trans_incompletes = []
    for transition in AF.table_transit[1:]:
        print(transition)
        for symbol in transition[1:-1]:
            print(symbol)
            if symbol == '-':
                trans_incompletes.append(transition[0])
                break
    if trans_incompletes:
        print("L'automate est incomplet aux etats :")
        print(trans_incompletes)
        return False
    else:
        print("L'automate est complet")
        return True


def completion(a):
    print()
    if (est_un_automate_complet(a) is False):
        last_etat = a.nb_etats+1  # rajoute etat poubelle
        j = 0
        while j < a.nb_symboles+1:  # on parcours le tableau horizontalement
            a.table_transit.extend([last_etat][last_etat])  # création nouvelle état poubelle (c'est le dernier état)
            # on fait pointer chaque transtion de l'état poublelle vers lui meme
            a.table_transit[last_etat][j] = last_etat
            j = j+1
            print(a.table_transit[last_etat][1])


def determinisation_et_completion_automate_synchrone(AF):
    new_tab = []
    temp = []
    comp = 0
    temp = AF.table_transit[0]
    new_tab = n
    while (comp != 1):
        print()
    return AF


def afficher_automate_deterministe_complet(AFDC):
    return AF


'''
def determinisation(AF):
    if (est_un_automate_asynchrone(AF) == True):
        determinisation_et_completion_automate_asynchrone(AF)
    elif: (est_un_automate_deterministe(AF) == True):
        if (est_un_automate_complet(AF) == True):
            AFDC = AF
        else:
            AFDC = completion(AF)
    else:
        AFDC = determinisation_automate_deterministe_complet(AFDC)
'''

af1 = lire_automate_sur_fichier("B10-3-synchrone.txt")

afficher_automate(af1)

print("Exemple d'appel")
#print(est_un_automate_asynchrone(af1))
#print(est_un_automate_complet(af1))


def recherche_etat_determinisation(AF, etat_nos):  # toruve les etat de sortie par rapport aux etats d'entrés pour tous les symboles
    tab_symbol = []
    
    for symbol in range(1, AF.nb_symboles+1):  # parce que c'est indente dans le tableau
        etats_sortie = []
        
        for etat_no in etat_nos:  # recherche dans les etat a traité pour le symbole
            etats_tmp = AF.table_transit[int(etat_no)+1][symbol].split(",")
            
            for etat_tmp in etats_tmp:
               if etat_tmp not in etats_sortie and etat_tmp != '-':
                   etats_sortie.append(etat_tmp)
                     
        tab_symbol.append(etats_sortie)
    return tab_symbol
    

etats_traite = []
etats_non_traite = [af1.etats_init]
print(etats_non_traite)

AFD_synchrone = []
print(af1.table_transit)
'''
while etats_non_traite:
    AFD_element = []
    for etat in etats_non_traite:
        print('tot')
        print(etat)
        etats_sorties = recherche_etat_determinisation(af1, etat)
        
        etats_non_traite.remove(etat)
        etats_non_traite.extend(etats_sorties)
        
        AFD_element.append(etat)
        for etat_sortie in etats_sorties:
            
            AFD_element.append("+".join(etat_sortie))  # prend chacun des etat sortie et met des plus
            
        AFD_synchrone.append(AFD_element)
'''    
        
        
        
print(AFD_synchrone)

    




