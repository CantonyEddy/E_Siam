import csv
import numpy as np
import ast
import pandas as pd

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
    """
    Charge les données à partir du fichier CSV.
    Chaque partie est stockée sur deux lignes :
    - la première : état du plateau
    - la deuxième : actions/mouvements

    Retourne X (états) et y (mouvements).
    """
    # Ignorer la première ligne d’en-tête non utilisée
    df = pd.read_csv(filepath, header=None, skiprows=1)

    # On suppose que les colonnes utiles commencent à l’index 5 (6e colonne)
    data = []

    # Parcours 2 lignes par 2 lignes
    for i in range(0, len(df), 2):
        info_line = df.iloc[i, :5]
        state_line = df.iloc[i, 5:]
        move_line = df.iloc[i + 1, 5:]

        try:
            # Nettoyage : suppression des NaN
            state_clean = [ast.literal_eval(item) if isinstance(item, str) and item.startswith("(") and item.endswith(")") else item for item in state_line.dropna().tolist()]
            move_clean = [ast.literal_eval(item) if isinstance(item, str) and item.startswith("[") and item.endswith("]") else item for item in move_line.dropna().tolist()]
            info_line_clean = info_line.dropna().tolist()
            data.append([info_line_clean, state_clean, move_clean])
        except (SyntaxError, ValueError) as e:
            print(f"Skipping invalid row at index {i}: {e}")

    # Transformer la liste en DataFrame pandas
    data = pd.DataFrame(data, columns=["Info", "Move", "State"])

    # Convertir les colonnes "State" et "Move" en chaînes pour éviter les problèmes d'hétérogénéité
    data["State"] = data["State"].apply(lambda x: np.array(x, dtype=object) if isinstance(x, list) else x)
    data["Move"] = data["Move"].apply(lambda x: np.array(x, dtype=object) if isinstance(x, list) else x)

    return data

def addPoidData(data, dataMouv, board):
    dataPoid = {}
    for mouv in dataMouv:
        dataPoid[mouv] = 0
        for i in range(len(data)):
            #print(data.iloc[i, 1])
            for j in range(data.iloc[i, 1].size//2):
                #print(data.iloc[i, 1][j, 1], mouv, i, j, data.iloc[i, 1].size//2)
                if data.iloc[i, 1][j, 1] == mouv:
                    if data.iloc[i, 0][4] == data.iloc[i, 1][j, 0]:
                        coef = 1
                    else:
                        coef = -1
                    if j == 0:
                        board2 = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, (0, -1), (0, -1), (0, -1), 0], [0, 0, 0, 0, 0]]
                    else:
                        board2 = data.iloc[i, 2][j-1]
                    dataPoid[mouv] += coef * (compareBoard(board, board2) + 1)
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