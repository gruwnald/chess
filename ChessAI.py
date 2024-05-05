import random
import math

DEPTH = 3
CHECKMATE = 1000
STALEMATE = 0

pieceValues = {
    "p": 1,
    "N": 3,
    "B": 3,
    "R": 5,
    "Q": 9,
    "K": 0
}

knightPositionScore = [[1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 2, 2, 2, 2, 2, 2, 1],
                       [1, 2, 3, 3, 3, 3, 2, 1],
                       [1, 2, 3, 4, 4, 3, 2, 1],
                       [1, 2, 3, 4, 4, 3, 2, 1],
                       [1, 2, 3, 3, 3, 3, 2, 1],
                       [1, 2, 2, 2, 2, 2, 2, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1]]

bishopPositionScore = [[3, 1, 1, 1, 1, 1, 1, 3],
                       [1, 4, 2, 3, 3, 2, 4, 1],
                       [2, 2, 4, 3, 3, 4, 2, 2],
                       [3, 4, 4, 5, 5, 4, 4, 3],
                       [3, 4, 4, 5, 5, 4, 4, 3],
                       [2, 2, 4, 3, 3, 4, 2, 2],
                       [1, 4, 2, 3, 3, 2, 4, 1],
                       [3, 1, 1, 1, 1, 1, 1, 3]]

rookPositionScore = [[2, 1, 4, 5, 5, 4, 1, 2],
                     [2, 1, 4, 5, 5, 4, 1, 2],
                     [2, 1, 2, 3, 3, 2, 1, 2],
                     [1, 1, 1, 2, 2, 1, 1, 1],
                     [1, 1, 1, 2, 2, 1, 1, 1],
                     [2, 1, 2, 3, 3, 2, 1, 2],
                     [2, 1, 4, 5, 5, 4, 1, 2],
                     [2, 1, 4, 5, 5, 4, 1, 2]]

queenPositionScore = [[1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 2, 3, 3, 3, 3, 2, 1],
                      [2, 5, 5, 4, 4, 5, 5, 2],
                      [2, 4, 4, 5, 5, 4, 4, 2],
                      [2, 4, 4, 5, 5, 4, 4, 2],
                      [1, 5, 5, 4, 4, 5, 5, 1],
                      [2, 2, 3, 3, 3, 3, 2, 2],
                      [1, 1, 1, 1, 1, 1, 1, 1]]

whitePawnPositionScore = [[8, 8, 8, 8, 8, 8, 8, 8],
                          [7, 7, 8, 8, 8, 8, 7, 7],
                          [4, 6, 7, 7, 7, 7, 6, 5],
                          [3, 4, 5, 5, 5, 5, 3, 3],
                          [2, 3, 4, 5, 5, 2, 2, 2],
                          [2, 3, 2, 3, 3, 1, 3, 3],
                          [1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1]]

blackPawnPositionScore = [[1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1],
                          [3, 3, 1, 3, 3, 2, 3, 2],
                          [2, 2, 2, 5, 5, 4, 3, 2],
                          [3, 3, 5, 5, 5, 5, 4, 3],
                          [5, 6, 7, 7, 7, 7, 6, 5],
                          [7, 7, 8, 8, 8, 8, 7, 7],
                          [8, 8, 8, 8, 8, 8, 8, 8]]

whiteKingEarlyPositionScore = [[1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [2, 2, 1, 1, 1, 1, 1, 2],
                              [3, 5, 5, 2, 2, 3, 5, 3]]

blackKingEarlyPositionScore = [[3, 5, 3, 2, 2, 5, 5, 3],
                              [2, 2, 1, 1, 1, 1, 1, 2],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1]]

whiteKingLatePositionScore = [[2, 2, 2, 2, 2, 2, 2, 2],
                              [5, 5, 5, 5, 5, 5, 5, 5],
                              [4, 5, 5, 5, 5, 5, 5, 4],
                              [2, 3, 4, 4, 4, 4, 3, 2],
                              [2, 2, 3, 3, 3, 3, 2, 2],
                              [1, 1, 2, 2, 2, 2, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 2, 2, 1, 1, 1, 2, 1]]

blackKingLatePositionScore = [[1, 2, 2, 1, 1, 1, 2, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 2, 2, 2, 2, 1, 1],
                              [2, 2, 3, 3, 3, 3, 2, 2],
                              [2, 3, 4, 4, 4, 4, 3, 2],
                              [4, 5, 5, 5, 5, 5, 5, 4],
                              [5, 5, 5, 5, 5, 5, 5, 5],
                              [2, 2, 2, 2, 2, 2, 2, 2]]

positionScores = {"N" : knightPositionScore,
                  "B" : bishopPositionScore,
                  "R" : rookPositionScore,
                  "Q" : queenPositionScore,
                  "wp" : whitePawnPositionScore,
                  "bp" : blackPawnPositionScore,
                  "wKe" : whiteKingEarlyPositionScore,
                  "bKe" : blackKingEarlyPositionScore,
                  "wKl" : whiteKingLatePositionScore,
                  "bKl" : blackKingLatePositionScore}

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def evaluate(gs):
    #Weights:
    checkWeight = 0.7
    kingSafetyWeight = 1
    positionWeight = 0.2

    lateGamePieceCount = 6


    board = gs.board
    if gs.endGame():
        if gs.checkmate():
            if gs.whiteToMove:
                return -CHECKMATE
            else:
                return CHECKMATE
        return STALEMATE


    whitePiecesCount = 0
    blackPiecesCount = 0

    whitePiecesValue = 0
    blackPiecesValue = 0
    for r, row in enumerate(board):
        for c, square in enumerate(row):
            pieceColor, piece = square[0], square[1]

            if piece not in ("-", "K"):
                #Count material
                if pieceColor == "w":
                    if piece != "p":
                        whitePiecesCount += 1
                        whitePiecesValue += pieceValues[piece] + positionScores[piece][r][c] * positionWeight
                    else:
                        whitePiecesValue += pieceValues[piece] + positionScores["wp"][r][c] * positionWeight

                else:
                    if piece != "p":
                        blackPiecesCount += 1
                        blackPiecesValue += pieceValues[piece] + positionScores[piece][r][c] * positionWeight
                    else:
                        blackPiecesValue += pieceValues[piece] + positionScores["bp"][r][c] * positionWeight

    evaluation = whitePiecesValue - blackPiecesValue

    #King safety
    piecesLeft = whitePiecesCount + blackPiecesCount
    for i in (1, -1):
        r, c = gs.whiteKingLocation if i == 1 else gs.blackKingLocation
        color = "w" if i == 1 else "b"
        if piecesLeft > lateGamePieceCount: #early game
            evaluation += i * positionScores[color + "Ke"][r][c] * kingSafetyWeight
        else:
            evaluation += i * positionScores[color + "Kl"][r][c] * positionWeight


    if gs.inCheck:
        #It's bad to be in check
        evaluation -= checkWeight * (1 if gs.whiteToMove else -1)

    return evaluation

def findBestMove(gs, validMoves):
    global counter
    counter = 0
    global nextMove
    nextMove = None
    turnMultiplier = 1 if gs.whiteToMove else -1
    #No iterative deepening
    ev = findMoveAlphaBeta(-CHECKMATE, CHECKMATE,
                     gs, validMoves, DEPTH, turnMultiplier)

    #Iterative deepening
    #
    print(f"Positions evaluated: {counter}. Best move: {nextMove}. Evaluation: {ev:.1f}")

    if nextMove is None:
        return findRandomMove(validMoves)
    return nextMove


def findMoveAlphaBeta(alpha, beta, gs, validMoves, depth, turnMultiplier):
    global nextMove
    global counter

    if depth == 0 or gs.endGame():
        counter += 1
        return turnMultiplier * evaluate(gs)

    maxEval = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        eval = -findMoveAlphaBeta(-beta, -alpha, gs, gs.getValidMoves(),
                                  depth - 1, -turnMultiplier)
        if eval > maxEval:
            maxEval = eval

            if depth == DEPTH:
                nextMove = move
                # validMoves.remove(move)
                # validMoves.insert(0, move)
        gs.undoMove()
        alpha = max(alpha, maxEval)
        if alpha >= beta:
            break
    if abs(maxEval) == CHECKMATE:
        maxEval -= depth #Find fastest mate
    return maxEval