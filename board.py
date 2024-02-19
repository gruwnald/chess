from pieces import *
from copy import deepcopy
class Board:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]

        self.white_pieces = [
            Rook('white', 7, 0), Rook('white', 7, 7),
            Knight('white', 7, 1), Knight('white', 7, 6),
            Bishop('white', 7, 2), Bishop('white', 7, 5),
            Queen('white', 7, 3), King('white', 7, 4),
            Pawn('white', 6, 0), Pawn('white', 6, 1),
            Pawn('white', 6, 2), Pawn('white', 6, 3),
            Pawn('white', 6, 4), Pawn('white', 6, 5),
            Pawn('white', 6, 6), Pawn('white', 6, 7)
        ]
        self.black_pieces = [
            Rook('black', 0, 0), Rook('black', 0, 7),
            Knight('black', 0, 1), Knight('black', 0, 6),      
            Bishop('black', 0, 2), Bishop('black', 0, 5),
            Queen('black', 0, 3), King('black', 0, 4),
            Pawn('black', 1, 0), Pawn('black', 1, 1),
            Pawn('black', 1, 2), Pawn('black', 1, 3),
            Pawn('black', 1, 4), Pawn('black', 1, 5),
            Pawn('black', 1, 6), Pawn('black', 1, 7)
        ]

    def get_piece(self, row, col):
        return self.board[row][col]

    def set_piece(self, row, col, piece):
        self.board[row][col] = piece
    
    def starting_board(self):
        for piece in self.white_pieces:
            self.set_piece(piece.row, piece.col, piece)
        for piece in self.black_pieces:
            self.set_piece(piece.row, piece.col, piece)


    def is_valid_move(self, start_row, start_col, end_row, end_col):
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
    

    def in_check(self, color):
        if color == "white":
            # Find the white king
            for piece in self.white_pieces:
                if isinstance(piece, King):
                    white_king = piece
                    break
            
            for piece in self.black_pieces:
                if self.is_valid_move(piece.row, piece.col, white_king.row, white_king.col):
                    return True
            return False
        else:
            # Find the black king
            for piece in self.black_pieces:
                if isinstance(piece, King):
                    black_king = piece
                    break
            
            for piece in self.white_pieces:
                if self.is_valid_move(piece.row, piece.col, black_king.row, black_king.col):
                    return True
            return False


    def move_regardless(self, start_row, start_col, end_row, end_col):
        piece = self.get_piece(start_row, start_col)

        if self.is_valid_move(start_row, start_col, end_row, end_col):
            #Remove captured piece from list
            if self.get_piece(end_row, end_col) is not None:
                if self.get_piece(end_row, end_col).color == 'white':
                    self.white_pieces.remove(self.get_piece(end_row, end_col))
                else:
                    self.black_pieces.remove(self.get_piece(end_row, end_col))

            #Move piece
            self.set_piece(end_row, end_col, piece)
            self.set_piece(start_row, start_col, None)
            piece.row = end_row
            piece.col = end_col


    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.get_piece(start_row, start_col)
        if self.in_check(piece.color):
            temp_board = deepcopy(self)
            temp_board.move_regardless(start_row, start_col, end_row, end_col)
            if temp_board.in_check(piece.color):
                print(f"{piece.color} is still in check after that move")
                return False


        self.move_regardless(start_row, start_col, end_row, end_col)

    def print_board(self):
        for row in self.board:
            print(row)