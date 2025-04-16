import csv
import matplotlib.pyplot as plt
import pygame
import io
import os

# --- Lecture de data.csv et analyse statistique ---
def analyser_data_csv(file_path="data.csv"):
    # Validate the file_path
    if not isinstance(file_path, (str, os.PathLike)):
        print(f"[Erreur] Le chemin du fichier est invalide : {file_path}")
        return {}

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

def generer_graphe_stats(stats):
    import numpy as np

    categories = ["PvP", "PvAI", "AIvAI"]
    values_a = []
    values_b = []
    values_nul = []

    # === PvP ===
    total = stats["pvp"]["total"]
    v1 = stats["pvp"]["v1"]
    v2 = stats["pvp"]["v2"]
    nuls = stats["pvp"]["nuls"]
    values_a.append((v1 / total) * 100 if total else 0)
    values_b.append((v2 / total) * 100 if total else 0)
    values_nul.append((nuls / total) * 100 if total else 0)

    # === PvAI ===
    total = stats["pvai"]["total"]
    vj = stats["pvai"]["joueur"]
    via = stats["pvai"]["ia"]
    nuls = stats["pvai"]["nuls"]
    values_a.append((vj / total) * 100 if total else 0)
    values_b.append((via / total) * 100 if total else 0)
    values_nul.append((nuls / total) * 100 if total else 0)

    # === AIvAI ===
    total = stats["aivai"]["total"]
    ia1 = stats["aivai"]["ia1"]
    ia2 = stats["aivai"]["ia2"]
    nuls = stats["aivai"]["nuls"]
    values_a.append((ia1 / total) * 100 if total else 0)
    values_b.append((ia2 / total) * 100 if total else 0)
    values_nul.append((nuls / total) * 100 if total else 0)

    x = np.arange(len(categories))
    width = 0.2  # 3 barres par groupe

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(x - width, values_a, width, label='Camp A', color='blue')
    ax.bar(x, values_nul, width, label='Match nul', color='gold')
    ax.bar(x + width, values_b, width, label='Camp B', color='red')

    ax.set_ylabel('Winrate (%)')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 110)
    ax.legend()

    # Titre manuel bien plus haut
    fig.suptitle('Winrate par camp et matchs nuls', fontsize=14, y=0.97)

    # Affichage des pourcentages bien espacÃ©s et des totaux
    for i in range(len(x)):
        ax.text(x[i] - width, values_a[i] + 2, f"{values_a[i]:.1f}%", ha='center', fontsize=9)
        ax.text(x[i], values_nul[i] + 2, f"{values_nul[i]:.1f}%", ha='center', fontsize=9)
        ax.text(x[i] + width, values_b[i] + 2, f"{values_b[i]:.1f}%", ha='center', fontsize=9)

        if i == 0:
            total = stats["pvp"]["total"]
        elif i == 1:
            total = stats["pvai"]["total"]
        else:
            total = stats["aivai"]["total"]

        max_val = max(values_a[i], values_b[i], values_nul[i])
        ax.text(x[i], max_val + 10, f"Total : {total} parties", ha='center', fontsize=9, color='gray')

    buf = io.BytesIO()
    plt.tight_layout(pad=3.0)
    plt.savefig(buf, format='PNG')
    plt.close(fig)
    buf.seek(0)
    return pygame.image.load(buf)