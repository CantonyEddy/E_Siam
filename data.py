import csv
import numpy as np
import pandas as pd

def saveData(data):
    with open("data.csv", "a+", newline="", encoding="utf-8") as fichier:
        fichier.seek(0)
        reader = csv.reader(fichier)
        line_count = sum(1 for _ in reader)  # Compter les lignes existantes

        writer = csv.writer(fichier)
        
        # Flatten the nested list for proper CSV formatting
        flattened_data = []
        for item in data:
                flattened_data.append(item)
        
        writer.writerow([line_count + 1] + flattened_data)  # Ajouter le numéro de ligne au début

    print("Nouvelle ligne ajoutée avec succès !")

def loadData():
        data = pd.read_csv('data.csv', sep=',', header=None)
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