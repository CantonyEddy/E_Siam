import pygame
from time import sleep
from board import Board
from game import logicalGame

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
largeur, hauteur = 800, 600

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("E Siam")

# Couleur de fond (R, G, B)
gris = (165, 170, 164)

# Initialiser le plateau
board = Board()

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Remplir l'écran avec la couleur de fond
        fenetre.fill(gris)
        logicalGame(fenetre, board, event, True, False)
     
        # Mettre à jour l'affichage
        pygame.display.flip()

# Quitter pygame
pygame.quit()
