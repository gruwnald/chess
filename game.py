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
        # Update in_check status
        self.white_in_check = self.board.in_check("white")
        self.black_in_check = self.board.in_check("black")
        return True

if __name__=="__main__":


    g = Game()
    g.make_move(6, 4, 4, 4)
    g.make_move(1, 4, 3, 4)
    g.make_move(6, 3, 4, 3)
    g.board.print_board()
    #g.make_move(3, 4, 4, 3)
    # g.board.print_board()
    # for piece in g.board.white_pieces:
    #     print(piece, piece.color, piece.row, piece.col)