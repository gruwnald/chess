from board import *
from pieces import *

class Game:
    def __init__(self):
        self.board = Board()
        self.board.starting_board()
        self.white_to_move = True

if __name__=="__main__":
    g = Game()
    g.board.print_board()