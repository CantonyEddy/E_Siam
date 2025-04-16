import pygame
import math
import random
from data import *
from board import *

pygame.font.init()  # Initialize the font module

direction = 0
directionBis = 0
x, y = 0, 0
xtemp, ytemp = 0, 0
clicked = False
localization = {(-1, -1): [0, 0], (1, -1): [1, 0], (2, -1): [2, 0], (3, -1): [3, 0], (5, -1): [4, 0], (5, 1): [4, 1], (5, 2): [4, 2], (5, 3): [4, 3], (5, 5): [4, 4], (3, 5): [3, 4], (2, 5): [2, 4], (1, 5): [1, 4], (-1, 5): [0, 4], (-1, 3): [0, 3], (-1, 2): [0, 2], (-1, 1): [0, 1]}
stopAction = True
data, mouvData, gridData = [], [], []
nbMouv = 0
nbTurnRockDontMouv = 0
font = pygame.font.Font(None, 50)
data_loaded = loadData("data.csv")
# Variables pour l'exploration contrôlée
epsilon = 0.2  # Au début 20% du temps, l'IA joue un coup totalement au hasard
epsilon_decay = 0.995  # Diminution progressive
epsilon_min = 0.05     # Ne pas descendre en dessous de 5%
games_played = get_number_of_lines("data.csv")//2       # Compteur de parties jouées
dataWin = get_fifth_column("data.csv")[1:] # Liste des résultats de chaque partie

def logicalGame(fenetre, board, event, ia = False, ia_vs_ia = False):
    global direction
    global directionBis
    global x, y
    x1, y1 = x, y
    global xtemp, ytemp
    global clicked
    global localization
    global stopAction
    global data, mouvData, gridData
    global nbMouv
    global nbTurnRockDontMouv
    global data_loaded
    #print(data_loaded.__len__())
    global games_played
    global epsilon
    global epsilon_decay
    global epsilon_min
    global dataWin
    tempBoard = board.getBoard()
    tempNbMouv = nbMouv
    # Dessiner le plateau
    if board.getWinner() == 0 and ((ia and board.getCurrentPlayerTurn()%2+1 == 1) or not ia) and not ia_vs_ia:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (x, y) in localization:
                if event.button == 4:
                    if direction == 0:
                        direction = 3
                    else:
                        direction -= 1
                elif event.button == 5:
                    if direction == 3:
                        direction = 0
                    else:
                        direction += 1
            elif (0 <= x <= 4) and (0 <= y <= 4):
                if event.button == 4:
                    if directionBis == 0:
                        directionBis = 3
                    else:
                        directionBis -= 1
                elif event.button == 5:
                    if directionBis == 3:
                        directionBis = 0
                    else:
                        directionBis += 1
        if event.type == pygame.MOUSEMOTION:
            x, y = (event.pos[0]-275)//50, (event.pos[1]-150)//50
            if x1 != x or y1 != y:
                x1, y1 = x, y
                directionBis = 0
        board.preplacePieces(x, y, fenetre, direction)
        if event.type == pygame.MOUSEBUTTONDOWN:  # Un clic a été effectué
            if event.button == 1:
                clicked = True
                xtemp, ytemp = (event.pos[0]-275)//50, (event.pos[1]-150)//50
        if event.type == pygame.MOUSEBUTTONUP and clicked:  # Bouton de souris relâché
            if event.button == 1:
                clicked = False
                x, y = (event.pos[0]-275)//50, (event.pos[1]-150)//50
                if x == xtemp and y == ytemp:
                    if (x, y) in localization:
                        err = board.enterPiece(board.getCurrentPlayerTurn()%2+1, localization[(x, y)][0], localization[(x, y)][1], direction)
                        if err == 0:
                            mouvData.append((board.getCurrentPlayerTurn()%2+1, ("e", localization[(x, y)][0], localization[(x, y)][1], direction)))
                            gridData.append(board.getBoard())
                            nbMouv += 1
                            board.nextPlayerTurn()
                    elif (0 <= x <= 4) and (0 <= y <= 4):
                        if ((board.getPieces(x, y) == 1 == board.getCurrentPlayerTurn()%2+1) or (board.getPieces(x, y) == 2 == board.getCurrentPlayerTurn()%2+1) and directionBis != 0):
                            directionTemp = board.getPiecesRotated(x, y)+directionBis
                            if directionTemp > 3:
                                directionTemp = 0+directionTemp-4
                            elif directionTemp < 0:
                                directionTemp = math.abs(directionTemp)
                            board.rotatePiece(x, y, directionTemp)
                            mouvData.append((board.getCurrentPlayerTurn()%2+1, ("t", x, y, directionTemp)))
                            gridData.append(board.getBoard())
                            nbMouv += 1
                            board.nextPlayerTurn()                    
                elif (-1 <= xtemp <= 5) and (-1 <= ytemp <= 5):
                        validAddMouvInDataBase = True
                        if (x == xtemp+1 and y == ytemp and board.getPieces(xtemp, ytemp) == board.getCurrentPlayerTurn()%2+1):
                            if x == 5:
                                board.remouvePiece(xtemp, ytemp)
                                mouvData.append((board.getCurrentPlayerTurn()%2+1, ("a", xtemp, ytemp)))
                                gridData.append(board.getBoard())
                                nbMouv += 1
                                validAddMouvInDataBase = False
                            else:
                                board.movePieces(xtemp, ytemp, 1)
                            if board.getPieces(xtemp, ytemp) == 0:
                                if validAddMouvInDataBase:
                                    mouvData.append((board.getCurrentPlayerTurn()%2+1, ("m", xtemp, ytemp, 1)))
                                    gridData.append(board.getBoard())
                                    nbMouv += 1
                                board.nextPlayerTurn()
                        elif (x == xtemp-1 and y == ytemp and board.getPieces(xtemp, ytemp) == board.getCurrentPlayerTurn()%2+1):
                            if x == -1:
                                board.remouvePiece(xtemp, ytemp)
                                mouvData.append((board.getCurrentPlayerTurn()%2+1, ("a", xtemp, ytemp)))
                                gridData.append(board.getBoard())
                                nbMouv += 1
                                validAddMouvInDataBase = False
                            else:
                                board.movePieces(xtemp, ytemp, 3)
                            if board.getPieces(xtemp, ytemp) == 0:
                                if validAddMouvInDataBase:
                                    mouvData.append((board.getCurrentPlayerTurn()%2+1, ("m", xtemp, ytemp, 3)))
                                    gridData.append(board.getBoard())
                                    nbMouv += 1
                                board.nextPlayerTurn()
                        elif (y == ytemp+1 and x == xtemp and board.getPieces(xtemp, ytemp) == board.getCurrentPlayerTurn()%2+1):
                            if y == 5:
                                board.remouvePiece(xtemp, ytemp)
                                mouvData.append((board.getCurrentPlayerTurn()%2+1, ("a", xtemp, ytemp)))
                                gridData.append(board.getBoard())
                                nbMouv += 1
                                validAddMouvInDataBase = False
                            else:
                                board.movePieces(xtemp, ytemp, 2)
                            if board.getPieces(xtemp, ytemp) == 0:
                                if validAddMouvInDataBase:
                                    mouvData.append((board.getCurrentPlayerTurn()%2+1, ("m", xtemp, ytemp, 2)))
                                    gridData.append(board.getBoard())
                                    nbMouv += 1
                                board.nextPlayerTurn()
                        elif (y == ytemp-1 and x == xtemp and board.getPieces(xtemp, ytemp) == board.getCurrentPlayerTurn()%2+1):
                            if y == -1:
                                board.remouvePiece(xtemp, ytemp)
                                mouvData.append((board.getCurrentPlayerTurn()%2+1, ("a", xtemp, ytemp)))
                                gridData.append(board.getBoard())
                                nbMouv += 1
                                validAddMouvInDataBase = False
                            else:
                                board.movePieces(xtemp, ytemp, 0)
                            if board.getPieces(xtemp, ytemp) == 0:
                                if validAddMouvInDataBase:
                                    mouvData.append((board.getCurrentPlayerTurn()%2+1, ("m", xtemp, ytemp, 0)))
                                    gridData.append(board.getBoard())
                                    nbMouv += 1
                                board.nextPlayerTurn()
            #print(board.listMoves(board.getCurrentPlayerTurn()%2+1))
    elif board.getWinner() == 0 and ((ia and board.getCurrentPlayerTurn()%2+1 == 2) or ia_vs_ia):
        mouv = board.listMoves(board.getCurrentPlayerTurn()%2+1)
        if isinstance(mouv, dict):
            mouv = list(mouv.keys())  # Convert dictionary keys to a list
        if len(mouv) > 0:
            d = addPoidData(data_loaded, mouv, board.getBoard(), board.getCurrentPlayerTurn()%2+1)
            d = softmax(d, temperature=1.5)

            # Choix du mouvement avec exploration contrôlée
            if random.random() < epsilon:
                mouvement = random.choice(mouv)  # ➔ Coup totalement aléatoire (exploration)
            else:
                total_weight = sum(d.values())
                weighted_choices = [(key, weight / total_weight) for key, weight in d.items()]
                random_value = random.uniform(0, 1)
                cumulative_probability = 0
                for key, probability in weighted_choices:
                    cumulative_probability += probability
                    if random_value <= cumulative_probability:
                        mouvement = key
                        break

            if mouvement[0] == "e":
                board.enterPiece(board.getCurrentPlayerTurn()%2+1, mouvement[2], mouvement[1], mouvement[3])
                mouvData.append((board.getCurrentPlayerTurn()%2+1, mouvement))
                gridData.append(board.getBoard())
                nbMouv += 1
            elif mouvement[0] == "m":
                board.movePieces(mouvement[2], mouvement[1], mouvement[3])
                mouvData.append((board.getCurrentPlayerTurn()%2+1, mouvement))
                gridData.append(board.getBoard())
                nbMouv += 1
            elif mouvement[0] == "a":
                board.remouvePiece(mouvement[2], mouvement[1])
                mouvData.append((board.getCurrentPlayerTurn()%2+1, mouvement))
                gridData.append(board.getBoard())
                nbMouv += 1
            elif mouvement[0] == "t":
                board.rotatePiece(mouvement[2], mouvement[1], mouvement[3])
                mouvData.append((board.getCurrentPlayerTurn()%2+1, mouvement))
                gridData.append(board.getBoard())
                nbMouv += 1
            board.nextPlayerTurn()
        else:
            print("No valid moves available.")
    elif board.getWinner() == 1:
        texte = font.render("Player 1 wins", True, (255, 255, 255))
        fenetre.blit(texte, (300, 300))
        if stopAction:
            if ia_vs_ia:
                data.append("ia")
            else:
                data.append("player")
            if ia or ia_vs_ia:
                data.append("ia")
            else:
                data.append("player")
            data.append(1)
            data.append(mouvData)
            data.append(gridData)
            saveData(data)
            stopAction = False
            #data_pure = data_loaded
            #print(data_pure)
            games_played += 1
            epsilon = max(epsilon_min, epsilon * epsilon_decay)
            print(f"Epsilon mis à jour : {epsilon:.4f} après {games_played} parties")

    elif board.getWinner() == 2:
        texte = font.render("Player 2 wins", True, (255, 255, 255))
        fenetre.blit(texte, (300, 300))
        if stopAction:
            if ia_vs_ia:
                data.append("ia")
            else:
                data.append("player")
            if ia or ia_vs_ia:
                data.append("ia")
            else:
                data.append("player")
            data.append(2)
            data.append(mouvData)
            data.append(gridData)
            saveData(data)
            stopAction = False
            #data_pure = data_loaded
            #print(data_pure)
            games_played += 1
            epsilon = max(epsilon_min, epsilon * epsilon_decay)
            print(f"Epsilon mis à jour : {epsilon:.4f} après {games_played} parties")
    elif board.getWinner() == 3:
        texte = font.render("Tie", True, (255, 255, 255))
        fenetre.blit(texte, (300, 300))
        if stopAction:
            if ia_vs_ia:
                data.append("ia")
            else:
                data.append("player")
            if ia or ia_vs_ia:
                data.append("ia")
            else:
                data.append("player")
            data.append(3)
            data.append(mouvData)
            data.append(gridData)
            saveData(data)
            stopAction = False
            #data_pure = data_loaded
            #print(data_pure)
            #lst = get_fifth_column("data.csv")[1:]
            #print(lst,lst.count(1),lst.count(2), lst.count(3))
            games_played += 1
            epsilon = max(epsilon_min, epsilon * epsilon_decay)
            print(f"Epsilon mis à jour : {epsilon:.4f} après {games_played} parties")
    board.draw(fenetre)
    board.preplacePiecesCenterRotate(x, y, fenetre, directionBis)
    texte = font.render(str(board.getLenPlayers(1)) + " X", True, (255, 255, 255))
    texte2 = font.render(str(board.getLenPlayers(2)) + " X", True, (255, 255, 255))
    texte3 = font.render("J1 : " + str(dataWin.count(1)//2) + " J2 : " + str(dataWin.count(2)//2) + " TIE : " + str(dataWin.count(3)//2), True, (0, 255, 255))
    image_rino = 'Rino.png'
    image_eleph = 'Eleph.png'
    rino_image = pygame.image.load(image_rino)
    rino_image = pygame.transform.scale(rino_image, (50, 50))
    eleph_image = pygame.image.load(image_eleph)
    eleph_image = pygame.transform.scale(eleph_image, (50, 50))
    fenetre.blit(rino_image, (350, 50))
    fenetre.blit(eleph_image, (350, 500))
    fenetre.blit(texte, (300, 50))
    fenetre.blit(texte2, (300, 500))
    fenetre.blit(texte3, (10, 10))
    if nbMouv > 990:
        print("Trop de mouvements")
        board.tie()
    print(nbTurnRockDontMouv)
    if compareBoardRock(tempBoard, board.getBoard()) and tempNbMouv != nbMouv:
        nbTurnRockDontMouv += 1
    else:
        nbTurnRockDontMouv = 0
    if nbTurnRockDontMouv >= 40:
        print("Trop de mouvements rock")
        board.tie()
    if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = (event.pos[0]-275)//50, (event.pos[1]-150)//50
            if x == 10 or y == -3:
                board.__init__()
                stopAction = True
                nbTurnRockDontMouv = 0
                nbMouv = 0
                data, mouvData, gridData = [], [], []
                data_loaded = loadData("data.csv")
                dataWin = get_fifth_column("data.csv")[1:]
    if ia_vs_ia and board.getWinner() != 0 and not stopAction:
        board.__init__()
        stopAction = True
        nbTurnRockDontMouv = 0
        nbMouv = 0
        data, mouvData, gridData = [], [], []
        data_loaded = loadData("data.csv")
        dataWin = get_fifth_column("data.csv")[1:]

# Vérifiez si analyser_data_csv est appelée ici
# Exemple :
# stats = analyser_data_csv("data.csv")