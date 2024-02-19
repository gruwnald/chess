from board import *
from pieces import *

class Game:
    def __init__(self):
        self.board = Board()
        self.board.starting_board()
        self.white_to_move = True

if __name__=="__main__":
    g = Game()
    g.board.move_piece(6, 4, 4, 4)
    g.board.move_piece(1, 4, 3, 4)
    g.board.move_piece(6, 3, 4, 3)
    g.board.move_piece(1, 3, 3, 3)
    g.board.move_piece(4, 4, 3, 3)
    g.board.move_piece(3, 3, 4, 4)
    g.board.print_board()