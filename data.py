import csv
import numpy as np

def saveData(data):
    with open("data.csv", "a+", newline="", encoding="utf-8") as fichier:
        fichier.seek(0)
        reader = csv.reader(fichier)
        line_count = sum(1 for _ in reader)  # Compter les lignes existantes

        writer = csv.writer(fichier)
        
        # Flatten the nested list for proper CSV formatting
        flattened_data = []
        for item in data:
            if isinstance(item, list):
                flattened_data.extend(item)
            else:
                flattened_data.append(item)
        
        writer.writerow([line_count + 1] + flattened_data)  # Ajouter le numéro de ligne au début

    print("Nouvelle ligne ajoutée avec succès !")