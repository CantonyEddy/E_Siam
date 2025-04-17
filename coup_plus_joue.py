import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_action_heatmap_filled(moves):
    """
    Affiche une heatmap 5x5 des mouvements 'm'.
    """

    # Grille 5x5 vide
    grid = np.zeros((5, 5), dtype=int)

    # Remplissage de la grille
    for _, move in moves:
        if move[0] == 'm':
            x, y = move[1], move[2]
            if 0 <= x <= 4 and 0 <= y <= 4:
                grid[y, x] += 1  # y ligne, x colonne

    # Rotation à 90° dans le sens horaire
    grid_rotated = np.rot90(grid, k=1)

    plt.figure(figsize=(6, 5))
    ax = sns.heatmap(grid_rotated, cmap="mako", linewidths=0.5, linecolor='black', square=True,
                     annot=True, fmt="d", cbar=True)

    plt.title("Heatmap des mouvements 'm'")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.gca().invert_yaxis()
    plt.show()
