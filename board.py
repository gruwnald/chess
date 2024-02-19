from pieces import *

class Board:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]

    def get_piece(self, row, col):
        return self.board[row][col]

    def set_piece(self, row, col, piece):
        self.board[row][col] = piece
    
    def starting_board(self):
        self.set_piece(0, 0, Rook('black', 0, 0))
        self.set_piece(0, 7, Rook('black', 0, 7))
        self.set_piece(7, 0, Rook('white', 7, 0))
        self.set_piece(7, 7, Rook('white', 7, 7))
        self.set_piece(0, 1, Knight('black', 0, 1))
        self.set_piece(0, 6, Knight('black', 0, 6))
        self.set_piece(7, 1, Knight('white', 7, 1))
        self.set_piece(7, 6, Knight('white', 7, 6))
        self.set_piece(0, 2, Bishop('black', 0, 2))
        self.set_piece(0, 5, Bishop('black', 0, 5))
        self.set_piece(7, 2, Bishop('white', 7, 2))
        self.set_piece(7, 5, Bishop('white', 7, 5))
        self.set_piece(0, 3, Queen('black', 0, 3))
        self.set_piece(7, 3, Queen('white', 7, 3))
        self.set_piece(0, 4, King('black', 0, 4))
        self.set_piece(7, 4, King('white', 7, 4))
        for i in range(8):
            self.set_piece(1, i, Pawn('black', 1, i))
            self.set_piece(6, i, Pawn('white', 6, i))
    
    def legal_moves(self, start_row, start_col, end_row, end_col):
        piece = self.get_piece(start_row, start_col)

        if piece is None:
            return False

        if self.get_piece(end_row, end_col) is not None:
            if self.get_piece(end_row, end_col).color == piece.color:
                return False
            potential_moves = piece.captures()
        else:
            potential_moves = piece.moves()

        if isinstance(piece, Knight) or isinstance(piece, King) or isinstance(piece, Pawn):
            return potential_moves[end_row][end_col] == 1
        
        elif isinstance(piece, Rook):
            if start_row == end_row:
                if start_col < end_col:
                    for i in range(start_col + 1, end_col):
                        if self.get_piece(start_row, i) is not None:
                            return False
                else:
                    for i in range(end_col + 1, start_col):
                        if self.get_piece(start_row, i) is not None:
                            return False
            elif start_col == end_col:
                if start_row < end_row:
                    for i in range(start_row + 1, end_row):
                        if self.get_piece(i, start_col) is not None:
                            return False
                else:
                    for i in range(end_row + 1, start_row):
                        if self.get_piece(i, start_col) is not None:
                            return False
            else:
                return False
            return True

        elif isinstance(piece, Bishop):
            if abs(start_row - end_row) != abs(start_col - end_col):
                return False
            if start_row < end_row:
                if start_col < end_col:
                    for i in range(1, abs(start_row - end_row)):
                        if self.get_piece(start_row + i, start_col + i) is not None:
                            return False
                else:
                    for i in range(1, abs(start_row - end_row)):
                        if self.get_piece(start_row + i, start_col - i) is not None:
                            return False
            else:
                if start_col < end_col:
                    for i in range(1, abs(start_row - end_row)):
                        if self.get_piece(start_row - i, start_col + i) is not None:
                            return False
                else:
                    for i in range(1, abs(start_row - end_row)):
                        if self.get_piece(start_row - i, start_col - i) is not None:
                            return False
            return True
        
        elif isinstance(piece, Queen):
            if start_row == end_row:
                if start_col < end_col:
                    for i in range(start_col + 1, end_col):
                        if self.get_piece(start_row, i) is not None:
                            return False
                else:
                    for i in range(end_col + 1, start_col):
                        if self.get_piece(start_row, i) is not None:
                            return False
            elif start_col == end_col:
                if start_row < end_row:
                    for i in range(start_row + 1, end_row):
                        if self.get_piece(i, start_col) is not None:
                            return False
                else:
                    for i in range(end_row + 1, start_row):
                        if self.get_piece(i, start_col) is not None:
                            return False
            elif abs(start_row - end_row) != abs(start_col - end_col):
                return False
            else:
                if start_row < end_row:
                    if start_col < end_col:
                        for i in range(1, abs(start_row - end_row)):
                            if self.get_piece(start_row + i, start_col + i) is not None:
                                return False
                    else:
                        for i in range(1, abs(start_row - end_row)):
                            if self.get_piece(start_row + i, start_col - i) is not None:
                                return False
                else:
                    if start_col < end_col:
                        for i in range(1, abs(start_row - end_row)):
                            if self.get_piece(start_row - i, start_col + i) is not None:
                                return False
                    else:
                        for i in range(1, abs(start_row - end_row)):
                            if self.get_piece(start_row - i, start_col - i) is not None:
                                return False
            return True

    
    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.get_piece(start_row, start_col)
        if self.legal_moves(start_row, start_col, end_row, end_col):
            self.set_piece(end_row, end_col, piece)
            self.set_piece(start_row, start_col, None)
            piece.row = end_row
            piece.col = end_col

    def print_board(self):
        for row in self.board:
            print(row)