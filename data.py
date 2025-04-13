import csv
import numpy as np
import ast
import pandas as pd
import math
import random

OPOSITE = np.array([2, 3, 0, 1])

def saveData(data):
    """
    Enregistre les données en deux lignes :
    - Une ligne avec les données de data[4] (état du plateau par exemple)
    - Une ligne avec les données de data[5] (mouvement ou action)
    Si une ligne a moins de 1000 cellules, elle est complétée avec des cellules None jusqu'à la 1001e cellule.
    """
    with open("data.csv", "a+", newline="", encoding="utf-8") as fichier:
        fichier.seek(0)
        reader = csv.reader(fichier)
        line_count = sum(1 for _ in reader)-1  # Compte les lignes existantes pour attribuer un ID

        writer = csv.writer(fichier)

        # Les 4 premiers champs simples
        fixed_data = data[:3]

        # Convertir les champs 5 et 6 en listes si c'est des chaînes
        list1 = data[3]
        list2 = data[4]

        if isinstance(list1, str):
            list1 = ast.literal_eval(list1)
        if isinstance(list2, str):
            list2 = ast.literal_eval(list2)

        # Compléter les listes avec None jusqu'à 1001 cellules
        list1 = (list1 + [None] * 996)[:996]
        list2 = (list2 + [None] * 996)[:996]

        # Écrire la première ligne : data[4] (état)
        writer.writerow([line_count + 1, "state"] + fixed_data + list1)

        # Écrire la deuxième ligne : data[5] (mouvements)
        writer.writerow([line_count + 2, "move"] + fixed_data + list2)

    print("Deux lignes ajoutées avec succès !")

def loadData(filepath: str):
    import collections
    data = pd.read_csv(filepath, header=None, skiprows=1)

    index = collections.defaultdict(list)  # Mouvements indexés

    for i in range(0, len(data), 2):
        info_line = data.iloc[i, :5]
        state_line = data.iloc[i, 5:]
        move_line = data.iloc[i+1, 5:]

        try:
            move_clean = [ast.literal_eval(item) if isinstance(item, str) and item.startswith("(") and item.endswith(")") else item for item in state_line.dropna().tolist()]
            state_clean = [ast.literal_eval(item) if isinstance(item, str) and item.startswith("[") and item.endswith("]") else item for item in move_line.dropna().tolist()]
            info_line_clean = info_line.dropna().tolist()
            
            # ➔ Ajouter les mouvements dans l'index
            for j, mouv in enumerate(move_clean):
                if j == 0:
                    board2 = [[0, 0, 0, 0, 0], 
                              [0, 0, 0, 0, 0], 
                              [0, (0, -1), (0, -1), (0, -1), 0], 
                              [0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0]]
                else:
                    board2 = state_clean[j-1]
                index[mouv].append((info_line_clean, board2))

        except (SyntaxError, ValueError, TypeError) as e:
            print(f"Skipping invalid row at index {i}: {e}")

    return index

def addPoidData(index, dataMouv, board, joueur):
    dataPoid = {mouv: 0 for mouv in dataMouv}

    for mouv in dataMouv:
        #print((joueur, (mouv)) in index)
        if (joueur, (mouv)) in index:
            #print("Mouvement trouvé !", index[(joueur, (mouv))])
            for info_line, board2 in index[(joueur, (mouv))]:
                '''print("info_line : ", info_line)
                print("board2 : ", board2)
                print("board : ", board)
                print(mouv)'''
                if info_line[4] == joueur:
                    coef = 1
                else:
                    coef = -1
                #print("oui", board, board2)

                # Score normal basé sur la comparaison de board
                score = coef * compareBoard(board, board2) + 1

                # Détecter si un rocher a bougé ou a été expulsé
                #print(board[mouv[1] + OPOSITE[mouv[3]] if (mouv[3] == 0 or mouv[3] == 2) and 0 <= mouv[1] + OPOSITE[mouv[3]] < 5 else mouv[1]][mouv[2] + OPOSITE[mouv[3]] if (mouv[3] == 1 or mouv[3] == 3) and 0 <= mouv[2] + OPOSITE[mouv[3]] < 5 else mouv[2]] if mouv[0] == "m" else "no")
                if mouv[0] == "m" and board[mouv[1] + OPOSITE[mouv[3]] if (mouv[3] == 0 or mouv[3] == 2) and 0 <= mouv[1] + OPOSITE[mouv[3]] < 5 else mouv[1]][mouv[2] + OPOSITE[mouv[3]] if (mouv[3] == 1 or mouv[3] == 3) and 0 <= mouv[2] + OPOSITE[mouv[3]] < 5 else mouv[2]] == (0, -1):
                    print("Un rocher a bougé !")
                    print("info_line : ", info_line)
                    print("board2 : ", board2)
                    print("board : ", board)
                    print(mouv)
                    # Un rocher a bougé
                    score += 10  # Bonus important
                if detectRockExpulsion(board2):
                    #print("Un rocher a été expulsé !")
                    # Un rocher est sorti du plateau
                    score += 100  # Très gros bonus

                dataPoid[mouv] += score

    # Ajout de bruit léger pour varier
    for mouv in dataPoid:
        bruit = random.uniform(-0.01, 0.01)
        dataPoid[mouv] += bruit

    #print("dataPoid : ", dataPoid)
    return dataPoid

def compareBoard(board1, board2):
    """
    Compare deux états de plateau (board1 et board2) pour vérifier à quel point les 2 board sont identiques.
    """

    board1 = np.array(board1, dtype=object)
    board2 = np.array(board2, dtype=object)

    percent = 0
    # Vérifier si les dimensions des tableaux sont identiques
    if board1.shape != board2.shape:
        return percent

    # Comparer les éléments des deux tableaux
    for i in range(board1.shape[0]):
        for j in range(board1.shape[1]):
            if board1[i, j] == board2[i, j]:
                percent += 0.04
            else:
                percent -= 0.04

    return percent

def compareBoardRock(board1, board2):
    """
    Compare si les cellules contenant (0, -1) sont à la même position sur les deux boards.
    """
    board1 = np.array(board1, dtype=object)
    board2 = np.array(board2, dtype=object)

    # Vérifier si les dimensions des tableaux sont identiques
    if board1.shape != board2.shape:
        return False

    # Parcourir les tableaux pour trouver les positions de (0, -1)
    positions_board1 = [(i, j) for i in range(board1.shape[0]) for j in range(board1.shape[1]) if board1[i, j] == (0, -1)]
    positions_board2 = [(i, j) for i in range(board2.shape[0]) for j in range(board2.shape[1]) if board2[i, j] == (0, -1)]

    # Comparer les positions
    return positions_board1 == positions_board2

def cles_max(d):
    if not d:
        return []  # Dictionnaire vide ➔ retourne une liste vide
    max_val = max(d.values())  # Trouver la valeur maximale
    return [k for k, v in d.items() if v == max_val]  # Toutes les clés avec la valeur max

def softmax(d, temperature=1.0):
    exp_weights = {k: math.exp(v / temperature) for k, v in d.items()}
    total = sum(exp_weights.values())
    return {k: v / total for k, v in exp_weights.items()}

def get_number_of_lines(filepath):
    df = pd.read_csv(filepath, header=None)  # Lit le fichier CSV sans en-têtes
    return len(df)  # Renvoie le nombre de lignes

def get_fifth_column(filepath):
    df = pd.read_csv(filepath, header=None)  # Lit le fichier CSV sans en-têtes
    return df.iloc[:, 4].tolist()  # Retourne la 5ème colonne de toutes les lignes sous forme de liste

def detectRockExpulsion(board):
    """Retourne True si un rocher est expulsé du plateau (moins de 3 rochers)."""
    nb_rock = 0
    for i in range(5):
        for j in range(5):
            if board[i][j] == (0, -1):
                nb_rock += 1
    return nb_rock < 3  # Normalement il y a 3 rochers au début "Normalement 🤷‍♂️"