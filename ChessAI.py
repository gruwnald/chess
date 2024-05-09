import random
from ChessParams import *

CHECKMATE = 1_000_000
STALEMATE = 0

pieceValues = {
    "p": 100,
    "N": 320,
    "B": 330,
    "R": 500,
    "Q": 900,
    "K": 0
}

PawnPositionScore = [[0,  0,  0,  0,  0,  0,  0,  0],
                     [50, 50, 50, 50, 50, 50, 50, 50],
                     [10, 10, 20, 30, 30, 20, 10, 10],
                     [5,  5,  10, 25, 25, 10,  5,  5],
                     [0,  0,  0,  20,  20,  0, 0,  0],
                     [5, -5, -10,  0,  0, -10, -5, 5],
                     [5, 10, 10, -20, -20, 10, 10, 10],
                     [0,  0,  0,  0,  0,  0,  0,  0]]

knightPositionScore = [[-50, -40, -30, -30, -30, -30, -40, -50],
                       [-40, -20, 0, 5, 5, 0, -20, -40],
                       [-30, 5, 10, 15, 15, 10, 5, -30],
                       [-30, 0, 15, 20, 20, 15, 0, -30],
                       [-30, 0, 15, 20, 20, 15, 0, -30],
                       [-30, 5, 10, 15, 15, 10, 5, -30],
                       [-40, -20, 0, 5, 5, 0, -20, -40],
                       [-50, -40, -30, -30, -30, -30, -40, -50]]

bishopPositionScore = [[-20, -10, -10, -10, -10, -10, -10, -20],
                       [-10, 0, 0, 0, 0, 0, 0, -10],
                       [-10, 0, 5, 10, 10, 5, 0, -10],
                       [-10, 5, 5, 10, 10, 5, 5, -10],
                       [-10, 0, 10, 10, 10, 10, 0, -10],
                       [-10, 10, 10, 10, 10, 10, 10, -10],
                       [-10, 5, 0, 0, 0, 0, 5, -10],
                       [-20, -10, -10, -10, -10, -10, -10, -20]]

rookPositionScore = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [5, 10, 10, 10, 10, 10, 10, 5],
                     [-5, 0, 0, 0, 0, 0, 0, -5],
                     [-5, 0, 0, 0, 0, 0, 0, -5],
                     [-5, 0, 0, 0, 0, 0, 0, -5],
                     [-5, 0, 0, 0, 0, 0, 0, -5],
                     [-5, 0, 0, 0, 0, 0, 0, -5],
                     [0, 0, 0, 5, 5, 0, 0, 0]]

queenPositionScore = [[-20, -10, -10, -5, -5, -10, -10, -20],
                      [-10, 0, 0, 0, 0, 0, 0, -10],
                      [-10, 0, 5, 5, 5, 5, 0, -10],
                      [-5, 0, 5, 5, 5, 5, 0, -5],
                      [0, 0, 5, 5, 5, 5, 0, -5],
                      [-10, 5, 5, 5, 5, 5, 0, -10],
                      [-10, 0, 5, 0, 0, 0, 0, -10],
                      [-20, -10, -10, -5, -5, -10, -10, -20]]

kingEarlyPositionScore = [[-30, -40, -40, -50, -50, -40, -40, -30],
                          [-30, -40, -40, -50, -50, -40, -40, -30],
                          [-30, -40, -40, -50, -50, -40, -40, -30],
                          [-30, -40, -40, -50, -50, -40, -40, -30],
                          [-20, -30, -30, -40, -40, -30, -30, -20],
                          [-10, -20, -20, -20, -20, -20, -20, -10],
                          [20, 20, 0, 0, 0, 0, 20, 20],
                          [20, 30, 10, 0, 0, 10, 30, 20]]

kingLatePositionScore = [[-50, -40, -30, -20, -20, -30, -40, -50],
                         [-30, -20, -10, 0, 0, -10, -20, -30],
                         [-30, -10, 20, 30, 30, 20, -10, -30],
                         [-30, -10, 30, 40, 40, 30, -10, -30],
                         [-30, -10, 30, 40, 40, 30, -10, -30],
                         [-30, -10, 20, 30, 30, 20, -10, -30],
                         [-30, -30, 0, 0, 0, 0, -30, -30],
                         [-50, -30, -30, -30, -30, -30, -30, -50]]

positionScores = {"wp" : PawnPositionScore,
                  "wN" : knightPositionScore,
                  "wB" : bishopPositionScore,
                  "wR" : rookPositionScore,
                  "wQ" : queenPositionScore,
                  "wKe" : kingEarlyPositionScore,
                  "wKl" : kingLatePositionScore,
                  "bp" : PawnPositionScore[::-1],
                  "bN" : knightPositionScore[::-1],
                  "bB" : bishopPositionScore[::-1],
                  "bR" : rookPositionScore[::-1],
                  "bQ" : queenPositionScore[::-1],
                  "bKe" : kingEarlyPositionScore[::-1],
                  "bKl" : kingLatePositionScore[::-1]}

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def evaluate(gs):
    #Weights:
    checkWeight = 0.5
    kingSafetyWeight = 1
    positionWeight = 1

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
                    whitePiecesValue += pieceValues[piece] + positionScores[square][r][c] * positionWeight
                    if piece != "p":
                        whitePiecesCount += 1
                else:
                    blackPiecesValue += pieceValues[piece] + positionScores[square][r][c] * positionWeight
                    if piece != "p":
                        blackPiecesCount += 1

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

    return evaluation/100

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
    print(f"Positions evaluated: {counter}. Best move: {nextMove}. Evaluation: {ev * turnMultiplier:.1f}")

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
    validMoves = orderMoves(validMoves)
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
        maxEval -= depth #Find the fastest mate
    return maxEval

def orderMoves(validMoves):
    for i, move in enumerate(validMoves):
        if move.pieceCaptured != "--":
            score = pieceValues[move.pieceCaptured[1]] - pieceValues[move.pieceMoved[1]]
            validMoves[i].score += score
        elif move.isPawnPromotion:
            validMoves[i].score += pieceValues["Q"] - pieceValues["p"]
        if move.pieceMoved[1] != "K":
            positionScore = positionScores[move.pieceMoved][move.endRow][move.endCol] - \
                        positionScores[move.pieceMoved][move.startRow][move.startCol]
        else:
            positionScore = positionScores[move.pieceMoved + "e"][move.endRow][move.endCol] - \
                            positionScores[move.pieceMoved + "e"][move.startRow][move.startCol]
        validMoves[i].score += positionScore
    validMoves.sort(key=lambda x: x.score, reverse=True)
    return validMoves
