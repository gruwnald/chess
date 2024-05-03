import random

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
DEPTH = 3

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def evaluate(gs):
    board = gs.board
    if gs.checkmate():
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate():
        return STALEMATE

    evaluation = 0
    for row in board:
        for piece in row:
            if piece != "--":
                pieceValue = pieceValues[piece[1]]
                evaluation += pieceValue if piece[0] == "w" else -pieceValue

    return evaluation

def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    if nextMove is None:
        return findRandomMove(validMoves)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    nextMove = None
    if depth == 0 or gs.checkmate() or gs.stalemate():
        return evaluate(gs)

    if whiteToMove:
        maxEval = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            eval = findMoveMinMax(gs, gs.getValidMoves(), depth - 1, False)
            if eval > maxEval:
                maxEval = eval
                print(depth)
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxEval
    else:
        minEval = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            eval = findMoveMinMax(gs, gs.getValidMoves(), depth - 1, True)
            if eval < minEval:
                minEval = eval
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minEval