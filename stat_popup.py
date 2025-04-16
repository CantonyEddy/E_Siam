import pygame
import sys
from stats_from_data import get_stats_from_data

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre popup
LARGEUR, HAUTEUR = 500, 400
fenetre_stats = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Statistiques E-SIAM")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Police
font = pygame.font.Font(None, 32)

def afficher_statistiques():
    stats = get_stats_from_data()
    lignes = [
        f"Parties jouées : {stats['parties_jouees']}",
        f"Victoires : {stats['victoires']}",
        f"Défaites : {stats['defaites']}",
        f"Taux de victoire : {stats['taux_victoire']}%"
    ]

    fenetre_stats.fill(BLANC)

    for i, ligne in enumerate(lignes):
        texte = font.render(ligne, True, NOIR)
        fenetre_stats.blit(texte, (40, 40 + i * 40))

    pygame.display.flip()

def fenetre_popup_stats():
    clock = pygame.time.Clock()
    afficher_statistiques()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        clock.tick(30)

    pygame.display.quit()

# Pour test manuel (à supprimer si intégré ailleurs)
if __name__ == "__main__":
    fenetre_popup_stats()
    pygame.quit()
    sys.exit()
