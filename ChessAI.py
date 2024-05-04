import random
import math

pieceValues = {
    "p": 1,
    "N": 3,
    "B": 3,
    "R": 5,
    "Q": 9,
    "K": 0
}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def evaluate(gs):
    board = gs.board
    if gs.endGame():
        if gs.checkmate():
            if gs.whiteToMove:
                return -CHECKMATE
            else:
                return CHECKMATE
        return STALEMATE

    evaluation = 0
    for r, row in enumerate(board):
        for c, square in enumerate(row):
            pieceColor, piece = square[0], square[1]
            colorMultiplier = 1 if pieceColor == "w" else -1
            startRow = 7 if pieceColor == "w" else 0
            if piece not in ("-", "K"):
                #Count material
                pieceValue = pieceValues[piece]
                evaluation += pieceValue * colorMultiplier

                centerControlWeight = 0.1
                evaluation -= centerControlWeight * math.sqrt((r - 3.5)**2 + (c - 3.5)**2) * colorMultiplier

                #Push pawns
                pushPawnsWeight = 0.1
                if piece == "p":
                    evaluation += pushPawnsWeight * abs(r - startRow) * colorMultiplier

            #King safety
            kingSafetyWeight = 0.5 * (1 - len(gs.moveLog)/40)
            if piece == "K":
                #King safety decreases when king far from starting row
                evaluation -= kingSafetyWeight * abs(r - startRow) * colorMultiplier
                evaluation -= kingSafetyWeight * abs(c - 3.5) * colorMultiplier






    return evaluation

def findBestMove(gs, validMoves):
    global counter
    counter = 0
    global nextMove
    nextMove = None
    turnMultiplier = 1 if gs.whiteToMove else -1
    #No iterative deepening
    findMoveAlphaBeta(-CHECKMATE, CHECKMATE,
                     gs, validMoves, DEPTH, turnMultiplier)

    #Iterative deepening
    #
    print(f"Positions evaluated: {counter}")

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