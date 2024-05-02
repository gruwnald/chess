class GameState:
    def __init__(self) -> None:
        """
        Board is a 2D 8x8 list, each element has 2 characters
        1st character represents the color of the piece, "b" or "w"
        2nd character represents the type of the piece, "K", "Q", "R", "B", "N" or "p"
        "--" represents an empty space
        """
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.getPieceMoves = {"p" : self.getPawnMoves, "R" : self.getRookMoves, "N" : self.getKnightMoves,
                              "B" : self.getBishopMoves, "Q" : self.getQueenMoves, "K" : self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []

        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = () #coordinates for the square where en passant capture is possible
    

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"

        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"

        #update enpassantPossible
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

        self.whiteToMove = not self.whiteToMove
    

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()
            self.whiteToMove = not self.whiteToMove


    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow, kingCol = self.whiteKingLocation
        else:
            kingRow, kingCol = self.blackKingLocation
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow, checkCol = check[0], check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != "K":
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()
        return moves


    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            startRow, startCol = self.whiteKingLocation
            allyColor, enemyColor = "w", "b"
        else:
            startRow, startCol = self.blackKingLocation
            allyColor, enemyColor = "b", "w"
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j, d in enumerate(directions):
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != "K":
                        if possiblePin == ():#1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: #2nd allied piece, no pin or check from this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == "R") or \
                            (4 <= j <= 7 and type == "B") or \
                            (i == 1 and type == "p" and
                            ((enemyColor == "w" and j in (6, 7)) or
                            (enemyColor == "b" and j in (4, 5)))) or \
                            (type == "Q") or (i == 1 and type == "K"):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else: #enemy piece not applying check
                            break
                else: #off board
                    break
        #check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == "N":
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks


    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0] #w, b or "-"
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove ):
                    piece = self.board[row][col][1]
                    self.getPieceMoves[piece](row, col, moves)
                    
        return moves


    def getPawnMoves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            #moves forward
            if self.board[row-1][col] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((row, col), (row-1, col), self.board))
                    if row == 6 and self.board[row-2][col] == "--":
                        moves.append(Move((row, col), (row-2, col), self.board))
            #Captures
            if col - 1 >= 0:
                if self.board[row-1][col-1][0] == "b":
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((row, col), (row-1, col-1), self.board))
                elif (row-1, col-1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row-1, col-1), self.board, isEnpassantMove=True))
            if col + 1 <= 7:
                if self.board[row-1][col+1][0] == "b":
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((row, col), (row-1, col+1), self.board))
                elif (row-1, col+1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row-1, col+1), self.board, isEnpassantMove=True))
        
        elif not self.whiteToMove:
            #moves forward
            if self.board[row+1][col] == "--":
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((row, col), (row+1, col), self.board))
                    if row == 1 and self.board[row+2][col] == "--":
                        moves.append(Move((row, col), (row+2, col), self.board))
            #Captures
            if col - 1 >= 0:
                if self.board[row+1][col-1][0] == "w":
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((row, col), (row+1, col-1), self.board))
                elif (row+1, col-1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row+1, col-1), self.board, isEnpassantMove=True))
            if col + 1 <= 7:
                if self.board[row+1][col+1][0] == "w":
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((row, col), (row+1, col+1), self.board))
                elif (row+1, col+1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row+1, col+1), self.board, isEnpassantMove=True))
            

    def getRookMoves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0]*i
                endCol = col + d[1]*i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                            break
                        else:
                            break #friendly piece in front
                else: #off board, change direction
                    break
        

    def getKnightMoves(self, row, col, moves):
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        enemyColor = "b" if self.whiteToMove else "w"
        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i) + abs(j) == 3:
                    endRow = row + i
                    endCol = col + j
                    if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                        if not piecePinned:
                            endPiece = self.board[endRow][endCol]
                            if endPiece[0] in ("-", enemyColor):
                                moves.append(Move((row, col), (endRow, endCol), self.board))


    def getBishopMoves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0]*i
                endCol = col + d[1]*i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                            break
                        else:
                            break #friendly piece in front
                else: #off board, change direction
                    break

    def getQueenMoves(self, row, col, moves):
        self.getRookMoves(row, col, moves)
        self.getBishopMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):
        enemyColor = "b" if self.whiteToMove else "w"
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                endRow, endCol = row + i, col + j
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] in ("-", enemyColor):
                        if enemyColor == "b":
                            self.whiteKingLocation = (endRow, endCol)
                        else:
                            self.blackKingLocation = (endRow, endCol)
                        inCheck, pins, checks = self.checkForPinsAndChecks()
                        if not inCheck:
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                        if enemyColor == "b":
                            self.whiteKingLocation = (row, col)
                        else:
                            self.blackKingLocation = (row, col)


    def checkmate(self):
        if self.inCheck:
            moves = self.getValidMoves()
            if len(moves) == 0:
                return True
        return False


    def stalemate(self):
        if not self.inCheck:
            moves = self.getValidMoves()
            if len(moves) == 0:
                return True
        return False
    def evaluate(self):
        pieceValue = {"p" : 1, "N" : 3, "B" : 3, "R" : 5, "Q" : 9}
        whiteScore = 0
        blackScore = 0
        if self.checkmate():
            return -1000 if self.whiteToMove else 1000
        elif self.stalemate():
            return 0
        for row in self.board:
            for piece in row:
                if piece[1] == "K":
                    continue
                if piece[0] == "w":
                    whiteScore += pieceValue[piece[1]]
                elif piece[0] == "b":
                    blackScore += pieceValue[piece[1]]

        return whiteScore - blackScore


    def AlphaBetaMin(self, alpha, beta, depth):
        if depth == 0:
            return self.evaluate()

        validMoves = self.getValidMoves()
        bestMove = validMoves[0] if len(validMoves) > 0 else None
        for move in self.getValidMoves():
            self.makeMove(move)
            score = self.AlphaBetaMax(alpha, beta, depth - 1)
            self.undoMove()
            if score <= alpha:
                return alpha
            if score < beta:
                beta = score
                bestMove = move
        print(bestMove.getChessNotation() if bestMove is not None else None)
        return beta


    def AlphaBetaMax(self, alpha, beta, depth):
        if depth == 0:
            return self.evaluate()
        validMoves = self.getValidMoves()
        bestMove = validMoves[0] if len(validMoves) > 0 else None
        for move in validMoves:
            self.makeMove(move)
            score = self.AlphaBetaMin(alpha, beta, depth - 1)
            self.undoMove()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
                bestMove = move
        return alpha


    def AlphaBetaPruning(self, depth):
        if self.whiteToMove:
            return self.AlphaBetaMax(-10000, 10000, depth)
        else:
            return self.AlphaBetaMin(-10000, 10000, depth)


class Move:
    ranksToRows = {"1":7, "2":6, "3":5, "4":4,
                   "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a":0, "b":1, "c":2, "d":3,
                   "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board, isEnpassantMove = False) -> None:
        self.startRow, self.startCol = startSq
        self.endRow, self.endCol = endSq
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = ((self.pieceMoved == "wp" and
                                self.endRow == 0) or
                               (self.pieceMoved == "bp" and
                                self.endRow == 7))
        self.isEnpassantMove = isEnpassantMove
        self.moveID = self.startRow * 10**3 + self.startCol * 10**2 + self.endRow * 10 + self.endCol
        if self.isEnpassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
