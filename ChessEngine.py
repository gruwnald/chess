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
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]
    

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

        #castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] #move the rook
                self.board[move.endRow][move.endCol + 1] = "--"
            else: #queenside castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]  # move the rook
                self.board[move.endRow][move.endCol - 2] = "--"


        #update castling rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                                 self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))

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

            #undo castling rights
            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRights = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"

            self.whiteToMove = not self.whiteToMove


    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.bks = False
        if move.pieceCaptured == "wR":
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceCaptured == "bR":
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.bks = False


    def getValidMoves(self):
        moves = []
        if self.whiteToMove:
            kingRow, kingCol = self.whiteKingLocation
        else:
            kingRow, kingCol = self.blackKingLocation
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks(kingRow, kingCol)
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
            self.getCastleMoves(kingRow, kingCol, moves)
        return moves


    def checkForPinsAndChecks(self, r, c):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            allyColor, enemyColor = "w", "b"
        else:
            allyColor, enemyColor = "b", "w"
        startRow, startCol = r, c
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
                        #r, c = self.whiteKingLocation if self.whiteToMove else self.blackKingLocation
                        inCheck, pins, checks = self.checkForPinsAndChecks(endRow, endCol)
                        if not inCheck:
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                        if enemyColor == "b":
                            self.whiteKingLocation = (row, col)
                        else:
                            self.blackKingLocation = (row, col)



    def getCastleMoves(self, row, col, moves):
        if self.inCheck:
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingSideCastleMoves(row, col, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueenSideCastleMoves(row, col, moves)


    def getKingSideCastleMoves(self, row, col, moves):
        if self.board[row][col+1] == "--" and self.board[row][col+2] == "--":
            inCheck1, pins1, checks1 = self.checkForPinsAndChecks(row, col+1)
            inCheck2, pins2, checks2 = self.checkForPinsAndChecks(row, col+2)
            if not inCheck1 and not inCheck2:
                moves.append(Move((row, col), (row, col+2), self.board, isCastleMove=True))


    def getQueenSideCastleMoves(self, row, col, moves):
        if self.board[row][col-1] == "--" and self.board[row][col-2] == "--" and self.board[row][col-3] == "--":
            inCheck1, pins1, checks1 = self.checkForPinsAndChecks(row, col - 1)
            inCheck2, pins2, checks2 = self.checkForPinsAndChecks(row, col - 2)
            if not inCheck1 and not inCheck2:
                moves.append(Move((row, col), (row, col-2), self.board, isCastleMove=True))


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


class Move:
    ranksToRows = {"1":7, "2":6, "3":5, "4":4,
                   "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a":0, "b":1, "c":2, "d":3,
                   "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False) -> None:
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

        self.isCastleMove = isCastleMove
        if self.isCastleMove:
            if self.endCol - self.startCol == 2:
                self.castleRookStart = (self.startRow, self.startCol + 3)
                self.castleRookEnd = (self.startRow, self.startCol + 1)
            else:
                self.castleRookStart = (self.startRow, self.startCol - 4)
                self.castleRookEnd = (self.startRow, self.startCol - 1)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs) -> None:
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


    def __str__(self) -> str:
        return ("K" if self.wks else "") + ("Q" if self.wqs else "") + \
               ("k" if self.bks else "") + ("q" if self.bqs else "")


    def __eq__(self, other):
        if isinstance(other, CastleRights):
            return self.wks == other.wks and self.bks == other.bks and self.wqs == other.wqs and self.bqs == other.bqs
        return False