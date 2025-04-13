import csv

def get_stats_from_data(file_path="data.csv"):
    stats = {
        "parties_jouees": 0,
        "victoires": 0,
        "defaites": 0,
        "taux_victoire": 0.0
    }

    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)

            nb_lignes = len(data)
            stats["parties_jouees"] = nb_lignes // 2  # Supposition : 2 lignes par partie

            # Supposition : la 5e colonne contient les résultats (1 pour victoire, -1 pour défaite)
            resultats = [int(row[4]) for row in data if len(row) > 4 and row[4] in ['1', '-1']]
            stats["victoires"] = resultats.count(1)
            stats["defaites"] = resultats.count(-1)

            if stats["parties_jouees"] > 0:
                stats["taux_victoire"] = round((stats["victoires"] / stats["parties_jouees"]) * 100, 2)

    except FileNotFoundError:
        print("[Erreur] Le fichier data.csv est introuvable.")
    except Exception as e:
        print(f"[Erreur] lors de la lecture de data.csv : {e}")

    return stats

# Exemple d'utilisation (à supprimer si importé ailleurs)
if __name__ == "__main__":
    stats = get_stats_from_data()
    print(stats)
