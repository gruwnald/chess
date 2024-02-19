from board import *
from pieces import *

class Game:
    def __init__(self):
        self.board = Board()
        self.board.starting_board()
        self.white_to_move = True
        self.white_in_check = False
        self.black_in_check = False
    
    
    def make_move(self, start_row, start_col, end_row, end_col):
        piece = self.board.get_piece(start_row, start_col)
        if piece is None:
            return False
        if piece.color == 'black' and self.white_to_move:
            return False
        if piece.color == 'white' and not self.white_to_move:
            return False
        if not self.board.is_valid_move(start_row, start_col, end_row, end_col):
            return False
        self.board.move_piece(start_row, start_col, end_row, end_col)
        self.white_to_move = not self.white_to_move
        return True

if __name__=="__main__":


    g = Game()
    g.make_move(6, 4, 4, 4)
    g.make_move(1, 4, 3, 4)
    g.make_move(6, 3, 4, 3)
    g.make_move(1, 3, 3, 3)
    g.make_move(4, 4, 3, 3)
    g.make_move(3, 4, 4, 3)
    g.make_move(7, 3, 6, 4)
    g.board.print_board()
    print("White in check: ", g.board.in_check("white"))
    print("black in check: ", g.board.in_check("black"))
    print("Qe7 is valid: ", g.board.is_valid_move(0, 3, 1, 4))
    #print(g.board.in_check("black"))
    g.make_move(0, 3, 1, 4)
    g.board.print_board()
    print("White in check: ", g.board.in_check("white"))
    print("black in check: ", g.board.in_check("black"))
    print("Qe7 is valid: ", g.board.is_valid_move(0, 3, 1, 4))
    # for piece in g.board.white_pieces:
    #     print(piece, piece.color, piece.row, piece.col)