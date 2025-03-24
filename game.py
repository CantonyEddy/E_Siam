import pygame
import math
direction = 0
directionBis = 0
x, y = 0, 0
xtemp, ytemp = 0, 0
clicked = False
localization = {(-1, -1): [0, 0], (1, -1): [1, 0], (2, -1): [2, 0], (3, -1): [3, 0], (5, -1): [4, 0], (5, 1): [4, 1], (5, 2): [4, 2], (5, 3): [4, 3], (5, 5): [4, 4], (3, 5): [3, 4], (2, 5): [2, 4], (1, 5): [1, 4], (-1, 5): [0, 4], (-1, 3): [0, 3], (-1, 2): [0, 2], (-1, 1): [0, 1]}

def logicalGame(fenetre, board, event):
    global direction
    global directionBis
    global x, y
    x1, y1 = x, y
    global xtemp, ytemp
    global clicked
    global localization
    # Dessiner le plateau
    if board.getWinner() == 0:
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
                            board.nextPlayerTurn()
                    elif (0 <= x <= 4) and (0 <= y <= 4):
                        if ((board.getPieces(x, y) == 1 == board.getCurrentPlayerTurn()%2+1) or (board.getPieces(x, y) == 2 == board.getCurrentPlayerTurn()%2+1) and directionBis != 0):
                            directionTemp = board.getPiecesRotated(x, y)+directionBis
                            if directionTemp > 3:
                                directionTemp = 0+directionTemp-4
                            elif directionTemp < 0:
                                directionTemp = math.abs(directionTemp)
                            board.rotatePiece(x, y, directionTemp)
                            board.nextPlayerTurn()                    
                elif (0 <= xtemp <= 4) and (0 <= ytemp <= 4):
                        if (x == xtemp+1 and y == ytemp and board.getPieces(xtemp, ytemp) == board.getCurrentPlayerTurn()%2+1):
                            board.movePieces(xtemp, ytemp, 1)
                            if board.getPieces(xtemp, ytemp) == 0:
                                board.nextPlayerTurn()
                        elif (x == xtemp-1 and y == ytemp and board.getPieces(xtemp, ytemp) == board.getCurrentPlayerTurn()%2+1):
                            board.movePieces(xtemp, ytemp, 3)
                            if board.getPieces(xtemp, ytemp) == 0:
                                board.nextPlayerTurn()
                        elif (y == ytemp+1 and x == xtemp and board.getPieces(xtemp, ytemp) == board.getCurrentPlayerTurn()%2+1):
                            board.movePieces(xtemp, ytemp, 2)
                            if board.getPieces(xtemp, ytemp) == 0:
                                board.nextPlayerTurn()
                        elif (y == ytemp-1 and x == xtemp and board.getPieces(xtemp, ytemp) == board.getCurrentPlayerTurn()%2+1):
                            board.movePieces(xtemp, ytemp, 0)
                            if board.getPieces(xtemp, ytemp) == 0:
                                board.nextPlayerTurn()

    board.draw(fenetre)
    board.preplacePiecesCenterRotate(x, y, fenetre, directionBis)
