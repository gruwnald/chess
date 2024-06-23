import random
import time
from ChessParams import *
from TranspositionTable import *

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

            #Count pieces and values
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
    global startTime
    startTime = time.time()

    global transpositionTable #Stores positions that have been visited before
    transpositionTable = TranspositionTable()

    global counter #Number of positions evaluated
    counter = 0

    global nextMove #Best move found
    nextMove = None

    global endProgram #End program flag for iterative deepening
    endProgram = False
    turnMultiplier = 1 if gs.whiteToMove else -1

    d = 1
    while not endProgram:
        ev = findMoveAlphaBeta(-CHECKMATE, CHECKMATE,
                               gs, validMoves, d, turnMultiplier, maxDepth=d)
        if ev == CHECKMATE-d: #Found forced mate
            break
        if depthLimited:
            endProgram = (d == DEPTH)
            moveToPlay = nextMove
        else:
            if time.time() - startTime < timePerMove: #Search was completed, nextMove is the best move on depth d
                moveToPlay = nextMove
            else:
                endProgram = True
        print(f"Best move on depth {d}: {moveToPlay}, eval: {ev * turnMultiplier:.1f}")
        d += 1

    print(f"Positions evaluated: {counter}. Time used: {time.time() - startTime:.1f}s. Best move: {moveToPlay}. Evaluation: {ev * turnMultiplier:.1f}")

    if moveToPlay is None:
        return findRandomMove(validMoves)
    return moveToPlay

    # if depthLimited:
    #     for d in range(1, DEPTH+1):
    #         ev = findMoveAlphaBeta(-CHECKMATE, CHECKMATE,
    #                                gs, validMoves, d, turnMultiplier, maxDepth=DEPTH)
    #         print(f"Best move on depth {d}: {nextMove}, eval: {ev * turnMultiplier:.1f}")
    #         if ev == CHECKMATE-d:
    #             break
    #     moveToPlay = nextMove
    #
    # else:
    #     d = 1
    #     moveToPlay = None
    #     while not endProgram:
    #         ev = findMoveAlphaBeta(-CHECKMATE, CHECKMATE,
    #                                gs, validMoves, d, turnMultiplier, maxDepth=d)
    #         if time.time() - startTime < timePerMove: #Search was completed, nextMove is the best move on depth d
    #             moveToPlay = nextMove
    #             print(f"Best move on depth {d}: {moveToPlay}, eval: {ev*turnMultiplier:.1f}")
    #             if  ev == CHECKMATE-d:
    #                 break
    #         d += 1



def findMoveAlphaBeta(alpha, beta, gs, validMoves, depth, turnMultiplier, maxDepth):
    global nextMove, counter, transpositionTable, startTime, endProgram

    alphaOrig = alpha
    entry = transpositionTable.lookup(gs)
    if entry is not None: #This position has been visited before
        if entry['depth'] >= depth:
            if entry['flag'] == 'EXACT':
                return entry['value']
            elif entry['flag'] == 'LOWERBOUND':
                alpha = max(alpha, entry['value'])
            elif entry['flag'] == 'UPPERBOUND':
                beta = min(beta, entry['value'])
            if alpha >= beta:
                return entry['value']

        validMoves.insert(0, validMoves.pop(validMoves.index(entry['move']))) #Order moves by transposition table

    if depth == 0 or gs.endGame():
        counter += 1
        return turnMultiplier * evaluate(gs)

    maxEval = -CHECKMATE
    bestMove = validMoves[0]
    for move in validMoves:
        if not depthLimited:
            if time.time() - startTime > timePerMove:
                endProgram = True
                break

        gs.makeMove(move)
        eval = -findMoveAlphaBeta(-beta, -alpha, gs, gs.getValidMoves(),
                                  depth - 1, -turnMultiplier, maxDepth=maxDepth)
        gs.undoMove()

        if eval > maxEval:
            maxEval = eval
            bestMove = move
            if depth == maxDepth:
                nextMove = move

        alpha = max(alpha, maxEval)
        if alpha >= beta:
            break

    if abs(maxEval) == CHECKMATE:
        maxEval -= depth #Find the fastest mate

    #Store in transposition table if position not seen or better depth
    update = False
    if entry is None:
        update = True
    elif entry['depth'] < depth:
        update = True

    if update:
        if maxEval <= alphaOrig:
            flag = 'upperbound'
        elif maxEval >= beta:
            flag = 'lowerbound'
        else:
            flag = 'exact'
        transpositionTable.store(
            gs=gs,
            depth=depth,
            value=maxEval,
            move=bestMove,
            flag=flag
        )
    return maxEval