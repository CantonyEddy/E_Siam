import pygame
from time import sleep
from board import Board
from game import logicalGame
from stats_from_data import get_stats_from_data  # ✅ Ajout
# Pas besoin d'importer stat_popup

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre (agrandie pour accueillir le panneau stats)
largeur, hauteur = 1000, 600  # ✅ Avant : 800, maintenant on a de la place à droite

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("E Siam")

# Couleurs
gris = (165, 170, 164)
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Police
font = pygame.font.Font(None, 32)

# Initialiser le plateau
board = Board()

# Panneau de stats toggle
afficher_stats = False  # ✅ Nouvelle variable

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:  # ✅ Toggle du panneau
                afficher_stats = not afficher_stats

    # Fond de la fenêtre
    fenetre.fill(gris)

    # Lancer le jeu
    logicalGame(fenetre, board, event, False, False)

    # ✅ Affichage du panneau latéral de statistiques
    if afficher_stats:
        stats = get_stats_from_data()
        panneau_x = 800  # Début du panneau à droite du plateau
        pygame.draw.rect(fenetre, blanc, (panneau_x, 0, 200, hauteur))  # Panneau blanc

        lignes = [
            f"Parties : {stats['parties_jouees']}",
            f"Victoires : {stats['victoires']}",
            f"Défaites : {stats['defaites']}",
            f"Winrate : {stats['taux_victoire']}%"
        ]

        for i, ligne in enumerate(lignes):
            texte = font.render(ligne, True, noir)
            fenetre.blit(texte, (panneau_x + 10, 30 + i * 40))

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter pygame
pygame.quit()
