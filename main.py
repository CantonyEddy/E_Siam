import pygame
from time import sleep
from board import Board
from game import logicalGame
from stats import afficher_stats_avancees

# Initialisation de pygame
pygame.init()

# Dimensions
largeur, hauteur = 1000, 600

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("E Siam")

# Couleurs
gris = (165, 170, 164)
blanc = (255, 255, 255)
noir = (0, 0, 0)
bleu = (60, 120, 200)

# Police
font = pygame.font.Font(None, 32)

# Plateau
board = Board()

# Vue active : "jeu" ou "stats"
vue_active = "jeu"

# Définir les rectangles des boutons
bouton_stats = pygame.Rect(850, 540, 120, 40)
bouton_retour = pygame.Rect(850, 540, 120, 40)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if vue_active == "jeu" and bouton_stats.collidepoint(x, y):
                vue_active = "stats"
            elif vue_active == "stats" and bouton_retour.collidepoint(x, y):
                vue_active = "jeu"

    # Fond
    fenetre.fill(gris)

    # === Vue JEU ===
    if vue_active == "jeu":
        logicalGame(fenetre, board, event, True, False)

        # Afficher le bouton "Stats"
        pygame.draw.rect(fenetre, bleu, bouton_stats)
        texte = font.render("📊 Stats", True, blanc)
        fenetre.blit(texte, (bouton_stats.x + 10, bouton_stats.y + 10))

    # === Vue STATISTIQUES ===
    elif vue_active == "stats":
        pygame.draw.rect(fenetre, blanc, (0, 0, largeur, hauteur))
        afficher_stats_avancees(fenetre)

        # Afficher le bouton "Retour"
        pygame.draw.rect(fenetre, bleu, bouton_retour)
        texte = font.render("⬅ Retour", True, blanc)
        fenetre.blit(texte, (bouton_retour.x + 10, bouton_retour.y + 10))

    # Rafraîchissement
    pygame.display.flip()

# Quitter pygame
pygame.quit()