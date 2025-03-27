import pygame
import math
import random
from data import saveData

pygame.font.init()  # Initialize the font module

direction = 0
directionBis = 0
x, y = 0, 0
xtemp, ytemp = 0, 0
clicked = False
localization = {(-1, -1): [0, 0], (1, -1): [1, 0], (2, -1): [2, 0], (3, -1): [3, 0], (5, -1): [4, 0], (5, 1): [4, 1], (5, 2): [4, 2], (5, 3): [4, 3], (5, 5): [4, 4], (3, 5): [3, 4], (2, 5): [2, 4], (1, 5): [1, 4], (-1, 5): [0, 4], (-1, 3): [0, 3], (-1, 2): [0, 2], (-1, 1): [0, 1]}
stopAction = True
data, mouvData = [], []
font = pygame.font.Font(None, 50)

def logicalGame(fenetre, board, event, ia = False):
    global direction
    global directionBis
    global x, y
    x1, y1 = x, y
    global xtemp, ytemp
    global clicked
    global localization
    global stopAction
    global data, mouvData
    # Dessiner le plateau
    if board.getWinner() == 0 and ((ia and board.getCurrentPlayerTurn()%2+1 == 1) or not ia):
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
                            mouvData.append(board.getBoard())
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
                            mouvData.append(board.getBoard())
                            board.nextPlayerTurn()                    
                elif (-1 <= xtemp <= 5) and (-1 <= ytemp <= 5):
                        validAddMouvInDataBase = True
                        if (x == xtemp+1 and y == ytemp and board.getPieces(xtemp, ytemp) == board.getCurrentPlayerTurn()%2+1):
                            if x == 5:
                                board.remouvePiece(xtemp, ytemp)
                                mouvData.append((board.getCurrentPlayerTurn()%2+1, ("a", xtemp, ytemp)))
                                mouvData.append(board.getBoard())
                                validAddMouvInDataBase = False
                            else:
                                board.movePieces(xtemp, ytemp, 1)
                            if board.getPieces(xtemp, ytemp) == 0:
                                if validAddMouvInDataBase:
                                    mouvData.append((board.getCurrentPlayerTurn()%2+1, ("m", xtemp, ytemp, 1)))
                                    mouvData.append(board.getBoard())
                                board.nextPlayerTurn()
                        elif (x == xtemp-1 and y == ytemp and board.getPieces(xtemp, ytemp) == board.getCurrentPlayerTurn()%2+1):
                            if x == -1:
                                board.remouvePiece(xtemp, ytemp)
                                mouvData.append((board.getCurrentPlayerTurn()%2+1, ("a", xtemp, ytemp)))
                                mouvData.append(board.getBoard())
                                validAddMouvInDataBase = False
                            else:
                                board.movePieces(xtemp, ytemp, 3)
                            if board.getPieces(xtemp, ytemp) == 0:
                                if validAddMouvInDataBase:
                                    mouvData.append((board.getCurrentPlayerTurn()%2+1, ("m", xtemp, ytemp, 3)))
                                    mouvData.append(board.getBoard())
                                board.nextPlayerTurn()
                        elif (y == ytemp+1 and x == xtemp and board.getPieces(xtemp, ytemp) == board.getCurrentPlayerTurn()%2+1):
                            if y == 5:
                                board.remouvePiece(xtemp, ytemp)
                                mouvData.append((board.getCurrentPlayerTurn()%2+1, ("a", xtemp, ytemp)))
                                mouvData.append(board.getBoard())
                                validAddMouvInDataBase = False
                            else:
                                board.movePieces(xtemp, ytemp, 2)
                            if board.getPieces(xtemp, ytemp) == 0:
                                if validAddMouvInDataBase:
                                    mouvData.append((board.getCurrentPlayerTurn()%2+1, ("m", xtemp, ytemp, 2)))
                                    mouvData.append(board.getBoard())
                                board.nextPlayerTurn()
                        elif (y == ytemp-1 and x == xtemp and board.getPieces(xtemp, ytemp) == board.getCurrentPlayerTurn()%2+1):
                            if y == -1:
                                board.remouvePiece(xtemp, ytemp)
                                mouvData.append((board.getCurrentPlayerTurn()%2+1, ("a", xtemp, ytemp)))
                                mouvData.append(board.getBoard())
                                validAddMouvInDataBase = False
                            else:
                                board.movePieces(xtemp, ytemp, 0)
                            if board.getPieces(xtemp, ytemp) == 0:
                                if validAddMouvInDataBase:
                                    mouvData.append((board.getCurrentPlayerTurn()%2+1, ("m", xtemp, ytemp, 0)))
                                    mouvData.append(board.getBoard())
                                board.nextPlayerTurn()
            #print(board.listMoves(board.getCurrentPlayerTurn()%2+1))
    elif board.getWinner() == 0 and (ia and board.getCurrentPlayerTurn()%2+1 == 2):
        mouv = board.listMoves(board.getCurrentPlayerTurn()%2+1)
        if len(mouv) > 0:
            mouvement = mouv[random.randint(0, len(mouv)-1)]
            if mouvement[0] == "e":
                board.enterPiece(board.getCurrentPlayerTurn()%2+1, mouvement[2], mouvement[1], mouvement[3])
                mouvData.append((board.getCurrentPlayerTurn()%2+1, mouvement))
                mouvData.append(board.getBoard())
            elif mouvement[0] == "m":
                board.movePieces(mouvement[2], mouvement[1], mouvement[3])
                mouvData.append((board.getCurrentPlayerTurn()%2+1, mouvement))
                mouvData.append(board.getBoard())
            elif mouvement[0] == "a":
                board.remouvePiece(mouvement[2], mouvement[1])
                mouvData.append((board.getCurrentPlayerTurn()%2+1, mouvement))
                mouvData.append(board.getBoard())
            elif mouvement[0] == "t":
                board.rotatePiece(mouvement[2], mouvement[1], mouvement[3])
                mouvData.append((board.getCurrentPlayerTurn()%2+1, mouvement))
                mouvData.append(board.getBoard())
            board.nextPlayerTurn()
    elif board.getWinner() == 1:
        texte = font.render("Player 1 wins", True, (255, 255, 255))
        fenetre.blit(texte, (300, 300))
        if stopAction:
            data.append("player")
            if ia:
                data.append("ia")
            else:
                data.append("player")
            data.append(1)
            data.append(mouvData)
            saveData(data)
            stopAction = False
    elif board.getWinner() == 2:
        texte = font.render("Player 2 wins", True, (255, 255, 255))
        fenetre.blit(texte, (300, 300))
        if stopAction:
            data.append("player")
            if ia:
                data.append("ia")
            else:
                data.append("player")
            data.append(2)
            data.append(mouvData)
            saveData(data)
            stopAction = False
    board.draw(fenetre)
    board.preplacePiecesCenterRotate(x, y, fenetre, directionBis)
    texte = font.render(str(board.getLenPlayers(1)) + " X", True, (255, 255, 255))
    texte2 = font.render(str(board.getLenPlayers(2)) + " X", True, (255, 255, 255))
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
    