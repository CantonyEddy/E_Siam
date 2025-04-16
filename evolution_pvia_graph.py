import numpy as np
import matplotlib.pyplot as plt
import io
import pygame

def generer_courbe_evolution_pvai(stats):

    resultats = stats.get("pvai_resultats", [])
    camps = stats.get("pvai_camp", [])

    # Sécurité : synchroniser, ignorer égalités, limiter aux 100 dernières
    filtered = [(r, c) for r, c in zip(resultats, camps) if r in [1, 2]][-100:]

    joueur_score = 0
    ia_score = 0
    matchs = []
    score_joueur = []
    score_ia = []

    for i, (gagnant, camp) in enumerate(filtered):
        if gagnant == 1 and camp == "joueur":
            joueur_score += 1
            ia_score -= 1
        elif gagnant == 2 and camp == "joueur":
            joueur_score -= 1
            ia_score += 1
        elif gagnant == 1 and camp == "ia":
            ia_score += 1
            joueur_score -= 1
        elif gagnant == 2 and camp == "ia":
            ia_score -= 1
            joueur_score += 1

        matchs.append(i + 1)
        score_joueur.append(joueur_score)
        score_ia.append(ia_score)

    fig, ax = plt.subplots(figsize=(7, 5))
    if matchs:  # afficher que si données
        ax.plot(matchs, score_joueur, marker='o', color='green', label="Joueur")
        ax.plot(matchs, score_ia, marker='o', color='purple', label="IA")

    ax.set_title("Score net - Joueur vs IA")
    ax.set_xlabel("Numéro de la partie PvIA")
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
