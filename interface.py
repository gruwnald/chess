from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt
from board import Board
from game import Game
from pieces import Piece

class Chessboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chessboard")
        self.setGeometry(100, 100, 800, 800)

        self.game = Game()
        self.board = self.game.board

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout(central_widget)
        grid_layout.setSpacing(0)

        self.buttons = [[None for _ in range(8)] for _ in range(8)]

        for row in range(8):
            for col in range(8):
                button = QPushButton()
                button.setFixedSize(100, 100)
                button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                if (row + col) % 2 == 0:
                    button.setStyleSheet("background-color: white")
                else:
                    button.setStyleSheet("background-color: gray")
                #button.clicked.connect(self.make_move(row, col)) TODO
                grid_layout.addWidget(button, row, col)
                self.buttons[row][col] = button

        #self.update_board()

if __name__ == "__main__":
    app = QApplication([])
    chessboard = Chessboard()
    chessboard.show()
    app.exec_()