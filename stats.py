import csv
import matplotlib.pyplot as plt
import pygame
import io

# --- Lecture de data.csv et analyse statistique ---
def analyser_data_csv(file_path="data.csv"):
    stats = {
        "pvp": {"v1": 0, "v2": 0, "nuls": 0, "total": 0},
        "pvai": {"joueur": 0, "ia": 0, "nuls": 0, "total": 0},
        "aivai": {"ia1": 0, "ia2": 0, "nuls": 0, "total": 0}
    }

    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)

            # Boucle sur chaque partie (2 lignes par partie)
            for i in range(0, len(data), 2):
                if len(data[i]) < 5:
                    continue

                j1 = data[i][2].strip().lower()
                j2 = data[i][3].strip().lower()
                winner = data[i][4].strip()

                # === Partie PvP ===
                if j1 == "player" and j2 == "player":
                    stats["pvp"]["total"] += 1
                    if winner == "1":
                        stats["pvp"]["v1"] += 1
                    elif winner == "2":
                        stats["pvp"]["v2"] += 1
                    elif winner == "3":
                        stats["pvp"]["nuls"] += 1

                # === Partie PvAI ===
                elif (j1 == "player" and j2 == "ia") or (j1 == "ia" and j2 == "player"):
                    stats["pvai"]["total"] += 1
                    if winner == "1" and j1 == "player":
                        stats["pvai"]["joueur"] += 1
                    elif winner == "2" and j2 == "player":
                        stats["pvai"]["joueur"] += 1
                    elif winner == "1" and j1 == "ia":
                        stats["pvai"]["ia"] += 1
                    elif winner == "2" and j2 == "ia":
                        stats["pvai"]["ia"] += 1
                    elif winner == "3":
                        stats["pvai"]["nuls"] += 1

                # === Partie IA vs IA (IAvIA) ===
                elif j1 == "ia" and j2 == "ia":
                    if winner == "1":
                        stats["aivai"]["ia1"] += 1
                    elif winner == "2":
                        stats["aivai"]["ia2"] += 1
                    elif winner == "3":
                        stats["aivai"]["nuls"] += 1

            # Calcul du total pour aivai à la fin (car incrémenté manuellement)
            aivai = stats["aivai"]
            aivai["total"] = aivai["ia1"] + aivai["ia2"] + aivai["nuls"]

            # === Résultats pour les courbes ===
            aivai_resultats = []
            pvai_resultats = []
            pvai_camp = []

            for i in range(0, len(data), 2):
                if len(data[i]) < 5:
                    continue
                j1 = data[i][2].strip().lower()
                j2 = data[i][3].strip().lower()
                winner = data[i][4].strip()

                # IA vs IA
                if j1 == "ia" and j2 == "ia":
                    if winner in ["1", "2", "3"]:
                        aivai_resultats.append(int(winner))

                # PvIA
                elif (j1 == "player" and j2 == "ia") or (j1 == "ia" and j2 == "player"):
                    if winner in ["1", "2", "3"]:
                        pvai_resultats.append(int(winner))
                        if winner == "1":
                            pvai_camp.append(j1)
                        elif winner == "2":
                            pvai_camp.append(j2)
                        else:
                            pvai_camp.append("egalite")

            stats["aivai_resultats"] = aivai_resultats
            stats["pvai_resultats"] = pvai_resultats
            stats["pvai_camp"] = pvai_camp

    except Exception as e:
        print(f"[Erreur] analyse du CSV : {e}")

    return stats