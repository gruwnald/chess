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
    
    def generate_pseudovalid_moves(self, start_row, start_col):
        piece = self.get_piece(start_row, start_col)
        m = [[0] * 8 for _ in range(8)]

        if isinstance(piece, Pawn):
            if piece.color == "white":
                #move forward if possible
                if self.get_piece(start_row - 1, start_col) is None:
                    m[start_row - 1][start_col] = 1
                    if start_row == 6 and self.get_piece(start_row - 2, start_col) is None:
                        m[start_row - 2][start_col] = 1
                #capture if possible
                if start_row - 1 >= 0 and start_col - 1 >= 0:
                    piece_to_capture = self.get_piece(start_row - 1, start_col - 1)
                    if isinstance(piece_to_capture, Piece) and piece_to_capture.color == "black":
                        m[start_row - 1][start_col - 1] = 1
                if start_row - 1 >= 0 and start_col + 1 <= 7:
                    piece_to_capture = self.get_piece(start_row - 1, start_col + 1)
                    if isinstance(piece_to_capture, Piece) and piece_to_capture.color == "black":
                        m[start_row - 1][start_col + 1] = 1
            else:
                #move forward if possible
                if self.get_piece(start_row + 1, start_col) is None:
                    m[start_row + 1][start_col] = 1
                    if start_row == 1 and self.get_piece(start_row + 2, start_col) is None:
                        m[start_row + 2][start_col] = 1
                #capture if possible
                if start_row + 1 <= 7 and start_col - 1 >= 0:
                    piece_to_capture = self.get_piece(start_row + 1, start_col - 1)
                    if isinstance(piece_to_capture, Piece) and piece_to_capture.color == "white":
                        m[start_row + 1][start_col - 1] = 1
                if start_row + 1 <= 7 and start_col + 1 <= 7:
                    piece_to_capture = self.get_piece(start_row + 1, start_col + 1)
                    if isinstance(piece_to_capture, Piece) and piece_to_capture.color == "white":
                        m[start_row + 1][start_col + 1] = 1
        

        elif isinstance(piece, Knight):
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if abs(i) + abs(j) == 3:
                        if 0 <= start_row + i < 8 and 0 <= start_col + j < 8:
                            piece_to_capture = self.get_piece(start_row + i, start_col + j)
                            if (not isinstance(piece_to_capture, Piece)) or \
                                piece_to_capture.color != piece.color:
                                m[start_row + i][start_col + j] = 1
        

        elif isinstance(piece, Bishop):
            for dir1 in (-1, 1):
                for dir2 in (-1, 1):
                    for i in range(1, 8):
                        row = start_row + dir1 * i
                        col = start_col + dir2 * i
                        if 0 <= row < 8 and 0 <= col < 8:
                            piece2 = self.get_piece(row, col)

                            if isinstance(piece2, Piece):
                                #capture opposite color, dont capture own
                                m[row][col] = int(piece2.color != piece.color)
                                break #dont look further in that direction
                            else:
                                m[row][col] = 1
        

        elif isinstance(piece, Rook):
            #Check vertical up
            if start_row != 0:
                for i in range(1, start_row + 1):
                    row = start_row - i
                    piece2 = self.get_piece(row, start_col)
                    if isinstance(piece2, Piece):
                        #capture opposite color, dont capture own
                        m[row][start_col] = int(piece2.color != piece.color)
                        break #dont look further in that direction
                    else:
                        m[row][start_col] = 1
            
            #Check vertical down
            if start_row != 7:
                for row in range(start_row + 1, 8):
                    piece2 = self.get_piece(row, start_col)
                    if isinstance(piece2, Piece):
                        #capture opposite color, dont capture own
                        m[row][start_col] = int(piece2.color != piece.color)
                        break #dont look further in that direction
                    else:
                        m[row][start_col] = 1
            
            #Check horizontal left
            if start_col != 0:
                for i in range(1, start_col+1):
                    col = start_col - i
                    piece2 = self.get_piece(start_row, col)
                    if isinstance(piece2, Piece):
                        #capture opposite color, dont capture own
                        m[start_row][col] = int(piece2.color != piece.color)
                        break #dont look further in that direction
                    else:
                        m[start_row][col] = 1
            
            #Check horizontal right
            if start_col != 7:
                for col in range(start_col + 1, 8):
                    piece2 = self.get_piece(start_row, col)
                    if isinstance(piece2, Piece):
                        #capture opposite color, dont capture own
                        m[start_row][col] = int(piece2.color != piece.color)
                        break #dont look further in that direction
                    else:
                        m[start_row][col] = 1
        

        elif isinstance(piece, Queen):
            for dir1 in (-1, 1):
                for dir2 in (-1, 1):
                    for i in range(1, 8):
                        row = start_row + dir1 * i
                        col = start_col + dir2 * i
                        if 0 <= row < 8 and 0 <= col < 8:
                            piece2 = self.get_piece(row, col)
                            if isinstance(piece2, Piece):
                                #capture opposite color, dont capture own
                                m[row][col] = int(piece2.color != piece.color)
                                break #dont look further in that direction
                            else:
                                m[row][col] = 1
            
            #Check vertical up
            if start_row != 0:
                for i in range(1, start_row + 1):
                    row = start_row - i
                    piece2 = self.get_piece(row, start_col)
                    if isinstance(piece2, Piece):
                        #capture opposite color, dont capture own
                        m[row][start_col] = int(piece2.color != piece.color)
                        break #dont look further in that direction
                    else:
                        m[row][start_col] = 1
            
            #Check vertical down
            if start_row != 7:
                for row in range(start_row + 1, 8):
                    piece2 = self.get_piece(row, start_col)
                    if isinstance(piece2, Piece):
                        #capture opposite color, dont capture own
                        m[row][start_col] = int(piece2.color != piece.color)
                        break #dont look further in that direction
                    else:
                        m[row][start_col] = 1
            
            #Check horizontal left
            if start_col != 0:
                for i in range(1, start_col+1):
                    col = start_col - i
                    piece2 = self.get_piece(start_row, col)
                    if isinstance(piece2, Piece):
                        #capture opposite color, dont capture own
                        m[start_row][col] = int(piece2.color != piece.color)
                        break #dont look further in that direction
                    else:
                        m[start_row][col] = 1
            
            #Check horizontal right
            if start_col != 7:
                for col in range(start_col + 1, 8):
                    piece2 = self.get_piece(start_row, col)
                    if isinstance(piece2, Piece):
                        #capture opposite color, dont capture own
                        m[start_row][col] = int(piece2.color != piece.color)
                        break #dont look further in that direction
                    else:
                        m[start_row][col] = 1
        

        elif isinstance(piece, King):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    row, col = start_row + i, start_col + j
                    if 0 <= row < 8 and 0 <= col < 8:
                        piece2 = self.get_piece(row, col)
                        if isinstance(piece2, Piece):
                            #capture opposite color, dont capture own
                            m[row][col] = int(piece2.color != piece.color)
                        else:
                            m[row][col] = 1
        
        return m


    def is_pseudovalid_move(self, start_row, start_col, end_row, end_col):
        return self.generate_pseudovalid_moves(start_row, start_col)[end_row][end_col]
    

    def in_check(self, color):
        if color == "white":
            # Find the white king
            for piece in self.white_pieces:
                if isinstance(piece, King):
                    white_king = piece
                    break
            
            for piece in self.black_pieces:
                if self.is_pseudovalid_move(piece.row, piece.col, white_king.row, white_king.col):
                    return True
            return False
        else:
            # Find the black king
            for piece in self.black_pieces:
                if isinstance(piece, King):
                    black_king = piece
                    break
            
            for piece in self.white_pieces:
                if self.is_pseudovalid_move(piece.row, piece.col, black_king.row, black_king.col):
                    return True
            return False


    def move_regardless(self, start_row, start_col, end_row, end_col):
        piece = self.get_piece(start_row, start_col)

        if self.is_pseudovalid_move(start_row, start_col, end_row, end_col):
            #Remove captured piece from list
            piece2 = self.get_piece(end_row, end_col)

            if isinstance(piece2, Piece):
                if piece2.color == 'white':
                    self.white_pieces.remove(piece2)
                else:
                    self.black_pieces.remove(piece2)

            #Move piece
            self.set_piece(end_row, end_col, piece)
            self.set_piece(start_row, start_col, None)
            #update piece position
            piece.row = end_row
            piece.col = end_col


    def generate_valid_moves(self, start_row, start_col):
        piece = self.get_piece(start_row, start_col)
        valid_moves = self.generate_pseudovalid_moves(start_row, start_col)

        for row in range(8):
            for col in range(8):
                if valid_moves[row][col]:
                    temp_board = deepcopy(self)
                    temp_board.move_regardless(start_row, start_col, row, col)
                    if temp_board.in_check(piece.color):
                        valid_moves[row][col] = 0
        return valid_moves
                    

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        return self.generate_valid_moves(start_row, start_col)[end_row][end_col]
    

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