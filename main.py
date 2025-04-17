import pygame
from time import sleep
from board import Board
from game import logicalGame
from stats import analyser_data_csv, generer_graphe_stats, get_all_moves
from stats_from_data import get_stats_from_data
from evolution_ia_graph import generer_courbe_evolution_ia
from evolution_pvia_graph import generer_courbe_evolution_pvai
from coup_plus_joue import plot_action_heatmap_filled

# Initialisation coucou
pygame.init()

# Dimensions
largeur, hauteur = 1000, 600
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

# Vue active : "jeu", "stats", "evo_ia", "evo_pvai"
vue_active = "pvia"

# Boutons
bouton_stats = pygame.Rect(850, 540, 120, 40)
bouton_retour = pygame.Rect(850, 540, 120, 40)
bouton_evo_ia = pygame.Rect(30, 540, 200, 40)
bouton_evo_pvai = pygame.Rect(250, 540, 220, 40)
bouton_evo_coup_joue = pygame.Rect(500, 540, 220, 40)
bouton_restart = pygame.Rect(775, 0, 50, 50)
bouton_pvia = pygame.Rect(775, 100, 100, 50)
bouton_iaia = pygame.Rect(775, 200, 100, 50)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if (vue_active == "jeu" or vue_active == "pvia") and bouton_stats.collidepoint(x, y):
                vue_active = "stats"
            elif vue_active == "jeu" and bouton_pvia.collidepoint(x, y):
                vue_active = "pvia"
            elif vue_active == "pvia" and bouton_iaia.collidepoint(x, y):
                vue_active = "jeu"
            elif vue_active == "stats":
                if bouton_retour.collidepoint(x, y):
                    vue_active = "jeu"
                elif bouton_evo_ia.collidepoint(x, y):
                    vue_active = "evo_ia"
                elif bouton_evo_pvai.collidepoint(x, y):
                    vue_active = "evo_pvai"
                elif bouton_evo_coup_joue.collidepoint(x, y):
                    plot_action_heatmap_filled(get_all_moves("data.csv"))
            elif vue_active in ["evo_ia", "evo_pvai"] and bouton_retour.collidepoint(x, y):
                vue_active = "stats"
        if vue_active == "pvia":
            # Fond
            fenetre.fill(gris)
            logicalGame(fenetre, board, event, True, False)
            pygame.draw.rect(fenetre, blanc, bouton_iaia)
            fenetre.blit(font.render("IaIa", True, noir), (bouton_iaia.x + 10, bouton_iaia.y + 10))
            pygame.draw.rect(fenetre, blanc, bouton_restart)
            fenetre.blit(font.render("restart", True, noir), (bouton_restart.x + 10, bouton_restart.y + 10))
            pygame.draw.rect(fenetre, bleu, bouton_stats)
            texte = font.render("📊 Stats", True, blanc)
            fenetre.blit(texte, (bouton_stats.x + 10, bouton_stats.y + 10))

    # === Vue JEU ===
    if vue_active == "jeu":
        fenetre.fill(gris)
        logicalGame(fenetre, board, event, False, True)

        # Bouton "Stats"
        pygame.draw.rect(fenetre, bleu, bouton_stats)
        texte = font.render("📊 Stats", True, blanc)
        fenetre.blit(texte, (bouton_stats.x + 10, bouton_stats.y + 10))
        pygame.draw.rect(fenetre, blanc, bouton_restart)
        fenetre.blit(font.render("restart", True, noir), (bouton_restart.x + 10, bouton_restart.y + 10))
        pygame.draw.rect(fenetre, blanc, bouton_pvia)
        fenetre.blit(font.render("PvIa", True, noir), (bouton_pvia.x + 10, bouton_pvia.y + 10))

    # === Vue STATS (barres générales) ===
    elif vue_active == "stats":
        fenetre.fill(gris)
        pygame.draw.rect(fenetre, blanc, (0, 0, largeur, hauteur))
        stats = analyser_data_csv("data.csv")
        graphe = generer_graphe_stats(stats)
        fenetre.fill(gris)
        fenetre.blit(graphe, ((largeur - graphe.get_width()) // 2, 50))

        # Boutons graphiques avancés
        pygame.draw.rect(fenetre, bleu, bouton_evo_ia)
        fenetre.blit(font.render("📈 IA vs IA", True, blanc), (bouton_evo_ia.x + 10, bouton_evo_ia.y + 10))

        pygame.draw.rect(fenetre, bleu, bouton_evo_pvai)
        fenetre.blit(font.render("🟢 Joueur vs IA", True, blanc), (bouton_evo_pvai.x + 10, bouton_evo_pvai.y + 10))
        pygame.draw.rect(fenetre, bleu, bouton_evo_coup_joue)
        fenetre.blit(font.render("🟢 Coups les plus joué", True, blanc), (bouton_evo_coup_joue.x + 10, bouton_evo_coup_joue.y + 10))

        pygame.draw.rect(fenetre, bleu, bouton_retour)
        fenetre.blit(font.render("⬅ Retour", True, blanc), (bouton_retour.x + 10, bouton_retour.y + 10))

    # === Vue EVOLUTION IA vs IA ===
    elif vue_active == "evo_ia":
        fenetre.fill(gris)
        stats = analyser_data_csv("data.csv")
        graphe = generer_courbe_evolution_ia(stats)
        fenetre.fill(gris)
        fenetre.blit(graphe, ((largeur - graphe.get_width()) // 2, 50))

        pygame.draw.rect(fenetre, bleu, bouton_retour)
        fenetre.blit(font.render("⬅ Retour", True, blanc), (bouton_retour.x + 10, bouton_retour.y + 10))

    # === Vue EVOLUTION PvAI ===
    elif vue_active == "evo_pvai":
        fenetre.fill(gris)
        stats = analyser_data_csv("data.csv")
        graphe = generer_courbe_evolution_pvai(stats)
        fenetre.fill(gris)
        fenetre.blit(graphe, ((largeur - graphe.get_width()) // 2, 50))

        pygame.draw.rect(fenetre, bleu, bouton_retour)
        fenetre.blit(font.render("⬅ Retour", True, blanc), (bouton_retour.x + 10, bouton_retour.y + 10))

    # Rafraîchissement
    pygame.display.flip()

# Fin
pygame.quit()