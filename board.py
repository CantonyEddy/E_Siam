import pygame
import numpy as np
import math
from piece import Piece

OPOSITE = np.array([2, 3, 0, 1])

class Board:
    def __init__(self):
        self.width = 5
        self.height = 5
        self.board = np.zeros((self.height, self.width), dtype=object)
        self.board[2, 1] = Piece(0)
        self.board[2, 2] = Piece(0)
        self.board[2, 3] = Piece(0)
        #self.board[2, 0] = Piece(1)
        #self.board[2, 3] = Piece(1)
        self.player1Piece = np.array([Piece(1) for _ in range(5)], dtype=object)
        self.player2Piece = np.array([Piece(2) for _ in range(5)], dtype=object)
        self.winner = 0
        self.currentPlayerTurn = 2

    def __str__(self):
        return '\n'.join([' '.join([str(cell) for cell in row]) for row in self.board])
    
    def getWinner(self):
        return self.winner
    
    def getPieces(self, x, y):
        if self.board[y, x] == 0:
            return self.board[y, x]
        return self.board[y, x].getPieces()
    
    def getPiecesRotated(self, x, y):
        return self.board[y, x].getDirection()
    
    def getCurrentPlayerTurn(self):
        return self.currentPlayerTurn
    
    def nextPlayerTurn(self):
        self.currentPlayerTurn += 1
    
    def preplacePieces(self, x, y, fenetre, direction):
        localization = [[-1, -1], [1, -1], [2, -1], [3, -1], [5, -1], [5, 1], [5, 2], [5, 3], [5, 5], [3, 5], [2, 5], [1, 5], [-1, 5], [-1, 3], [-1, 2], [-1, 1]]
        if [x, y] in localization:
            pygame.draw.rect(fenetre, (0, 0, 0), (x*50+275, y*50+150, 50, 50), 1)
            if self.currentPlayerTurn%2 == 0:
                image_file = 'Rino.png'
            else:
                image_file = 'Eleph.png'
            rock_image = pygame.image.load(image_file)
            rock_image = pygame.transform.scale(rock_image, (50, 50))
            if direction == 1:
                rock_image = pygame.transform.rotate(rock_image, -90)
            elif direction == 2:
                rock_image = pygame.transform.rotate(rock_image, 180)
            elif direction == 3:
                rock_image = pygame.transform.rotate(rock_image, 90)
            #if 0 <= x <= 4 and 0 <= y <= 4 and self.board[y, x] == 0:
            #   fenetre.blit(rock_image, (x*50+275, y*50+150))
            fenetre.blit(rock_image, (x*50+275, y*50+150))

    def preplacePiecesCenterRotate(self, x, y, fenetre, direction):
        if (0 <= x <= 4) and (0 <= y <= 4):
            pygame.draw.rect(fenetre, (0, 0, 0), (x*50+275, y*50+150, 50, 50), 1)
            if self.getPieces(x, y) == 1 == self.currentPlayerTurn%2+1:
                image_file = 'Rino.png'
            elif self.getPieces(x, y) == 2 == self.currentPlayerTurn%2+1:
                image_file = 'Eleph.png'
            else:
                return
            direction = self.board[y, x].getDirection()+direction
            if direction > 3:
                direction = 0+direction-4
            elif direction < 0:
                direction = math.abs(direction)
            rock_image = pygame.image.load(image_file)
            rock_image = pygame.transform.scale(rock_image, (50, 50))
            if direction == 1:
                rock_image = pygame.transform.rotate(rock_image, -90)
            elif direction == 2:
                rock_image = pygame.transform.rotate(rock_image, 180)
            elif direction == 3:
                rock_image = pygame.transform.rotate(rock_image, 90)
            #if 0 <= x <= 4 and 0 <= y <= 4 and self.board[y, x] == 0:
            #   fenetre.blit(rock_image, (x*50+275, y*50+150))
            fond_gris = pygame.Surface((48, 48))
            fond_gris.fill((165, 170, 164))
            fenetre.blit(fond_gris, (x*50+276, y*50+151))
            fenetre.blit(rock_image, (x*50+275, y*50+150))
    
    def draw(self, fenetre):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(fenetre, (0, 0, 0), (j*50+275, i*50+150, 50, 50), 1)
                cell = self.board[i, j]
                if isinstance(cell, Piece):
                    piece_type = cell.getPieces()
                    if piece_type == 0:
                        image_file = 'Rock.png'
                    elif piece_type == 1:
                        image_file = 'Rino.png'
                    elif piece_type == 2:
                        image_file = 'Eleph.png'
                    else:
                        continue
                    rock_image = pygame.image.load(image_file)
                    rock_image = pygame.transform.scale(rock_image, (50, 50))
                    direction = cell.getDirection()
                    if direction == 1:
                        rock_image = pygame.transform.rotate(rock_image, -90)
                    elif direction == 2:
                        rock_image = pygame.transform.rotate(rock_image, 180)
                    elif direction == 3:
                        rock_image = pygame.transform.rotate(rock_image, 90)
                    fenetre.blit(rock_image, (j*50+275, i*50+150))

    def movePieces(self, x, y, direction, balanceOfPowerRock = 1, balanceOfPower = 0, directionPLus = -1):
        if isinstance(self.board[y, x], Piece):
            if direction == 0 and y - 1 >= 0:
                i = 0
                while y - i >= 0 and self.board[y - i, x] != 0:
                    if self.board[y - i, x].getPieces() == 0:
                        balanceOfPowerRock -= 1
                    elif (self.board[y - i, x].getDirection() == self.board[y, x].getDirection() or self.board[y, x].getPieces() == 0) and self.board[y - i, x].getDirection() == direction:
                        balanceOfPower += 1
                        balanceOfPowerRock += 1
                    elif self.board[y - i, x].getDirection() == OPOSITE[self.board[y, x].getDirection()] or (directionPLus != -1 and self.board[y - i, x].getDirection() == OPOSITE[directionPLus]):
                        balanceOfPower -= 1
                    i += 1
                    if not (balanceOfPower > 0 and balanceOfPowerRock > 0):
                        break
                if (balanceOfPower > 0 and balanceOfPowerRock > 0) or (i == 1 and self.board[y-1, x] == 0):
                    pieceOut = None
                    for k in range(-i, 0):
                        if y - abs(k) + 1 == 0:
                            pieceOut = self.board[y - abs(k) + 1, x]
                            coordinate = (y - abs(k) + 1, x)
                            self.board[y - abs(k) + 1, x] = 0
                        else:
                            self.board[y - abs(k), x] = self.board[y - abs(k) + 1, x]
                            self.board[y - abs(k) + 1, x] = 0
                    if isinstance(pieceOut, Piece) and pieceOut.getPieces() != 0:
                        if pieceOut.getPieces() == 1:
                            self.player1Piece = np.append(self.player1Piece, pieceOut)
                        elif pieceOut.getPieces() == 2:
                            self.player2Piece = np.append(self.player2Piece, pieceOut)
                    elif isinstance(pieceOut, Piece) and pieceOut.getPieces() == 0:
                        self.win(coordinate, direction)
            elif direction == 1 and x + 1 < self.width:
                i = 0
                while x + i < self.width and self.board[y, x + i] != 0:
                    if self.board[y, x + i].getPieces() == 0:
                        balanceOfPowerRock -= 1
                    elif (self.board[y, x + i].getDirection() == self.board[y, x].getDirection() or self.board[y, x].getPieces() == 0) and self.board[y, x + i].getDirection() == direction:
                        balanceOfPower += 1
                        balanceOfPowerRock += 1
                    elif self.board[y, x + i].getDirection() == OPOSITE[self.board[y, x].getDirection()] or (directionPLus != -1 and self.board[y, x + 1].getDirection() == OPOSITE[directionPLus]):
                        balanceOfPower -= 1
                    i += 1
                    if not (balanceOfPower > 0 and balanceOfPowerRock > 0):
                        break
                if (balanceOfPower > 0 and balanceOfPowerRock > 0) or (i == 1 and self.board[y, x+1] == 0):
                    pieceOut = None
                    for k in range(-i, 0):
                        if x + abs(k) - 1 == self.width - 1:
                            pieceOut = self.board[y, x + abs(k) - 1]
                            coordinate = (y, x + abs(k) - 1)
                            self.board[y, x + abs(k) - 1] = 0
                        else:
                            self.board[y, x + abs(k)] = self.board[y, x + abs(k) - 1]
                            self.board[y, x + abs(k) - 1] = 0
                    if isinstance(pieceOut, Piece) and pieceOut.getPieces() != 0:
                        if pieceOut.getPieces() == 1:
                            self.player1Piece = np.append(self.player1Piece, pieceOut)
                        elif pieceOut.getPieces() == 2:
                            self.player2Piece = np.append(self.player2Piece, pieceOut)
                    elif isinstance(pieceOut, Piece) and pieceOut.getPieces() == 0:
                        self.win(coordinate, direction)
            elif direction == 2 and y + 1 < self.height:
                i = 0
                while y + i < self.height and self.board[y + i, x] != 0:
                    if self.board[y + i, x].getPieces() == 0:
                        balanceOfPowerRock -= 1
                    elif (self.board[y + i, x].getDirection() == self.board[y, x].getDirection() or self.board[y, x].getPieces() == 0) and self.board[y + i, x].getDirection() == direction:
                        balanceOfPower += 1
                        balanceOfPowerRock += 1
                    elif self.board[y + i, x].getDirection() == OPOSITE[self.board[y, x].getDirection()] or (directionPLus != -1 and self.board[y + i, x].getDirection() == OPOSITE[directionPLus]):
                        balanceOfPower -= 1
                    i += 1
                    if not (balanceOfPower > 0 and balanceOfPowerRock > 0):
                        break
                if (balanceOfPower > 0 and balanceOfPowerRock > 0) or (i == 1 and self.board[y+1, x] == 0):
                    pieceOut = None
                    for k in range(-i, 0):
                        if y + abs(k) - 1 == self.width - 1:
                            pieceOut = self.board[y + abs(k) - 1, x]
                            coordinate = (y + abs(k) - 1, x)
                            self.board[y + abs(k) - 1, x] = 0
                        else:
                            self.board[y + abs(k), x] = self.board[y + abs(k) - 1, x]
                            self.board[y + abs(k) - 1, x] = 0
                    if isinstance(pieceOut, Piece) and pieceOut.getPieces() != 0:
                        if pieceOut.getPieces() == 1:
                            self.player1Piece = np.append(self.player1Piece, pieceOut)
                        elif pieceOut.getPieces() == 2:
                            self.player2Piece = np.append(self.player2Piece, pieceOut)
                    elif isinstance(pieceOut, Piece) and pieceOut.getPieces() == 0:
                        self.win(coordinate, direction)
            elif direction == 3 and x - 1 >= 0:
                i = 0
                while x - i >= 0 and self.board[y, x - i] != 0:
                    if self.board[y, x - i].getPieces() == 0:
                        balanceOfPowerRock -= 1
                    elif (self.board[y, x - i].getDirection() == self.board[y, x].getDirection() or self.board[y, x].getPieces() == 0) and self.board[y, x - i].getDirection() == direction:
                        balanceOfPower += 1
                        balanceOfPowerRock += 1
                    elif self.board[y, x - i].getDirection() == OPOSITE[self.board[y, x].getDirection()] or (directionPLus != -1 and self.board[y, x - i].getDirection() == OPOSITE[directionPLus]):
                        balanceOfPower -= 1
                    i += 1
                    if not (balanceOfPower > 0 and balanceOfPowerRock > 0):
                        break
                if (balanceOfPower > 0 and balanceOfPowerRock > 0) or (i == 1 and self.board[y, x-1] == 0):
                    pieceOut = None
                    for k in range(-i, 0):
                        if x - abs(k) + 1 == 0:
                            pieceOut = self.board[y, x - abs(k) + 1]
                            coordinate = (y, x - abs(k) + 1)
                            self.board[y, x - abs(k) + 1] = 0
                        else:
                            self.board[y, x - abs(k)] = self.board[y, x - abs(k) + 1]
                            self.board[y, x - abs(k) + 1] = 0
                    if isinstance(pieceOut, Piece) and pieceOut.getPieces() != 0:
                        if pieceOut.getPieces() == 1:
                            self.player1Piece = np.append(self.player1Piece, pieceOut)
                        elif pieceOut.getPieces() == 2:
                            self.player2Piece = np.append(self.player2Piece, pieceOut)
                    elif isinstance(pieceOut, Piece) and pieceOut.getPieces() == 0:
                        self.win(coordinate, direction)

    def enterPiece(self, joueur, x, y, direction):
        if joueur == 1 and len(self.player1Piece) > 0 and (x == 0 or x == self.width-1 or y == 0 or y == self.height-1):
            if self.board[y, x] != 0:
                if direction == 0 and y == 4:
                    self.movePieces(x, y, direction, 2, 1, direction)        
                elif direction == 1 and x == 0:
                    self.movePieces(x, y, direction, 2, 1, direction)
                elif direction == 2 and y == 0:
                    self.movePieces(x, y, direction, 2, 1, direction)
                elif direction == 3 and x == 4:
                    self.movePieces(x, y, direction, 2, 1, direction)
                if self.board[y, x] != 0:
                        return 1
            self.board[y, x] = self.player1Piece[-1]
            self.player1Piece = np.delete(self.player1Piece, -1)
            self.board[y, x].setDirection(direction)
            return 0
        elif joueur == 2 and len(self.player2Piece) > 0 and (x == 0 or x == self.width-1 or y == 0 or y == self.height-1):
            if self.board[y, x] != 0:
                if direction == 0 and y == 4:
                    self.movePieces(x, y, direction, 2, 1, direction)
                elif direction == 1 and x == 0:
                    self.movePieces(x, y, direction, 2, 1, direction)
                elif direction == 2 and y == 0:
                    self.movePieces(x, y, direction, 2, 1, direction)
                elif direction == 3 and x == 4:
                    self.movePieces(x, y, direction, 2, 1, direction)
                if self.board[y, x] != 0:
                        return 1
            self.board[y, x] = self.player2Piece[-1]
            self.player2Piece = np.delete(self.player2Piece, -1)
            self.board[y, x].setDirection(direction)
            return 0
        return 1

    def rotatePiece(self, x, y, direction):
        if isinstance(self.board[y, x], Piece) and self.board[y, x].getPieces() != 0:
            self.board[y, x].setDirection(direction)
    
    def win(self, coordinates, direction):
        directionBis = [1, -1, -1, 1]
        if direction == 0 or direction == 2:
            i = 0
            while self.board[coordinates[0] + (i*directionBis[direction]), coordinates[1]] != 0:
                if self.board[coordinates[0] + (i*directionBis[direction]), coordinates[1]].getDirection() == direction:
                    self.winner = self.board[coordinates[0] + (i*directionBis[direction]), coordinates[1]].getPieces()
                    break
                i += 1
        elif direction == 1 or direction == 3:
            i = 0
            while self.board[coordinates[0], coordinates[1] + (i*directionBis[direction])] != 0:
                if self.board[coordinates[0], coordinates[1] + (i*directionBis[direction])].getDirection() == direction:
                    self.winner = self.board[coordinates[0], coordinates[1] + (i*directionBis[direction])].getPieces()
                    break
                i += 1