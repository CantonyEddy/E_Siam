class Piece:
    def __init__(self, piece_type):
        self.piece_type = piece_type
        if piece_type == 0:
            self.direction = -1
        else:
            self.direction = 0
        self.position = [-1, -1]

    def getPieces(self):
        return self.piece_type
    
    def setDirection(self, direction):
        self.direction = direction

    def getDirection(self):
        return self.direction