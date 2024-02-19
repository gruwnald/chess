class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col


class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.value = 1

    def moves(self):
        m = [[0] * 8 for _ in range(8)]
        if self.color == 'white':
            if self.row == 6:
                m[self.row - 2][self.col] = 1
            m[self.row - 1][self.col] = 1
        else:
            if self.row == 1:
                m[self.row + 2][self.col] = 1
            m[self.row + 1][self.col] = 1
        return m
    
    def captures(self):
        m = [[0] * 8 for _ in range(8)]
        if self.color == 'white':
            if self.row - 1 >= 0 and self.col - 1 >= 0:
                m[self.row - 1][self.col - 1] = 1
            if self.row - 1 >= 0 and self.col + 1 < 8:
                m[self.row - 1][self.col + 1] = 1
        else:
            if self.row + 1 < 8 and self.col - 1 >= 0:
                m[self.row + 1][self.col - 1] = 1
            if self.row + 1 < 8 and self.col + 1 < 8:
                m[self.row + 1][self.col + 1] = 1
        return m

    def __repr__(self) -> str:
        return 'p'


class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.value = 3

    def moves(self):
        m = [[0] * 8 for _ in range(8)]
        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i) + abs(j) == 3:
                    if 0 <= self.row + i < 8 and 0 <= self.col + j < 8:
                        m[self.row + i][self.col + j] = 1
        return m
    
    def captures(self):
        return self.moves()

    def __repr__(self) -> str:
        return 'N'


class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.value = 3

    def moves(self):
        m = [[0] * 8 for _ in range(8)]
        for i in range(8):
            if 0 <= self.row + i < 8 and 0 <= self.col + i < 8:
                m[self.row + i][self.col + i] = 1
            if 0 <= self.row - i < 8 and 0 <= self.col + i < 8:
                m[self.row - i][self.col + i] = 1
            if 0 <= self.row + i < 8 and 0 <= self.col - i < 8:
                m[self.row + i][self.col - i] = 1
            if 0 <= self.row - i < 8 and 0 <= self.col - i < 8:
                m[self.row - i][self.col - i] = 1
        return m

    def captures(self):
        return self.moves()
    
    def __repr__(self) -> str:
        return 'B'


class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.value = 5

    def moves(self):
        m = [[0] * 8 for _ in range(8)]
        for i in range(8):
            m[i][self.col] = 1
            m[self.row][i] = 1
        return m

    def captures(self):
        return self.moves()
    
    def __repr__(self) -> str:
        return 'R'


class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.value = 9

    def moves(self):
        m = [[0] * 8 for _ in range(8)]
        for i in range(8):
            m[i][self.col] = 1
            m[self.row][i] = 1
            if 0 <= self.row + i < 8 and 0 <= self.col + i < 8:
                m[self.row + i][self.col + i] = 1
            if 0 <= self.row - i < 8 and 0 <= self.col + i < 8:
                m[self.row - i][self.col + i] = 1
            if 0 <= self.row + i < 8 and 0 <= self.col - i < 8:
                m[self.row + i][self.col - i] = 1
            if 0 <= self.row - i < 8 and 0 <= self.col - i < 8:
                m[self.row - i][self.col - i] = 1
        return m
    
    def captures(self):
        return self.moves()
    
    def __repr__(self) -> str:
        return 'Q'


class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

    def moves(self):
        m = [[0] * 8 for _ in range(8)]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= self.row + i < 8 and 0 <= self.col + j < 8:
                    m[self.row + i][self.col + j] = 1
        return m

    def captures(self):
        return self.moves()
    
    def __repr__(self) -> str:
        return 'K'