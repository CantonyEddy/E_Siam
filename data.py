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
        move_line = df.iloc[i+1, 5:]

        # Nettoyage : suppression des NaN
        state_clean = [ast.literal_eval(item) if isinstance(item, str) and item.startswith("(") and item.endswith(")") else item for item in state_line.dropna().tolist()]
        move_clean = [ast.literal_eval(item) if isinstance(item, str) and item.startswith("[") and item.endswith("]") else item for item in move_line.dropna().tolist()]
        info_line_clean = info_line.dropna().tolist()
        data.append([info_line_clean, state_clean, move_clean])

    return data

def addPoidData(data, dataMouv, board):
    # Serialize the board to a string for comparison
    serialized_board = str(board)

    # Ensure column 4 is treated as strings for comparison
    data[4] = data[4].astype(str)

    # Find positions where the serialized board matches column 4
    positions = data[data[4] == serialized_board].index.tolist()

    # Print the positions found
    print("Positions trouvées :", positions)