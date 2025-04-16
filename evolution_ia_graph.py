import numpy as np
import matplotlib.pyplot as plt
import io
import pygame

def generer_courbe_evolution_ia(stats):

    resultats = stats.get("aivai_resultats", [])
    resultats_filtrés = [r for r in resultats if r in [1, 2]][-100:]

    print("aivai_resultats filtrés =", resultats_filtrés)  # DEBUG

    ia1_score = 0
    ia2_score = 0
    matchs = []
    score_ia1 = []
    score_ia2 = []

    for i, gagnant in enumerate(resultats_filtrés):
        if gagnant == 1:
            ia1_score += 1
            ia2_score -= 1
        elif gagnant == 2:
            ia1_score -= 1
            ia2_score += 1
        matchs.append(i + 1)
        score_ia1.append(ia1_score)
        score_ia2.append(ia2_score)

    fig, ax = plt.subplots(figsize=(7, 5))
    if matchs:
        ax.plot(matchs, score_ia1, marker='o', color='blue', label="IA 1 (1er joueur)")
        ax.plot(matchs, score_ia2, marker='o', color='red', label="IA 2 (2e joueur)")

    ax.set_title("Score net des IA dans les parties IA vs IA")
    ax.set_xlabel("Numéro de la partie")
    ax.set_ylabel("Score net (victoires - défaites)")
    ax.axhline(0, color='gray', linestyle='--')
    ax.grid(True)
    ax.legend()

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='PNG')
    plt.close(fig)
    buf.seek(0)
    return pygame.image.load(buf)
