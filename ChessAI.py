import time
from ChessParams import *
from TranspositionTable import *
from PositionScores import *

CHECKMATE = 1_000_000
STALEMATE = 0
drawnPositions = (["wN", "bN"], ["wN", "wN"], ["bN", "bN"], ["wN"], ["bN"], ["wB"], ["bB"])

def evaluate(gs):
    checkWeight = 50

    if gs.endGame():
        if gs.checkmate():
            if gs.whiteToMove:
                return -CHECKMATE
            else:
                return CHECKMATE
        return STALEMATE

    evaluationEarly = 0
    evaluationLate = 0
    board = gs.board

    piecesLeftExactly = []
    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece != "--":
                if gs.piecesLeft <= 2: #possible forced draw by insufficient material
                    if piece[1] != 'K':
                        piecesLeftExactly.append(piece)

                if piece[0] == 'w':
                    evaluationEarly += pieceValuesEarly[piece[1]] + positionScoresEarly[piece][r][c]
                    evaluationLate += pieceValuesLate[piece[1]] + positionScoresLate[piece][r][c]
                else:
                    evaluationEarly -= pieceValuesEarly[piece[1]] + positionScoresEarly[piece][r][c]
                    evaluationLate -= pieceValuesLate[piece[1]] + positionScoresLate[piece][r][c]
    if gs.piecesLeft <= 2 and piecesLeftExactly in drawnPositions:
        return STALEMATE

    piecesLeft = min(gs.piecesLeft, 14) #in case of early promotion
    evaluation = (piecesLeft * evaluationEarly + (14 - piecesLeft) * evaluationLate)/14

    if gs.inCheck:
        #It's bad to be in check
        evaluation -= checkWeight * (1 if gs.whiteToMove else -1)
    return evaluation/100


def alphaBeta(alpha, beta, validMoves, gs, depth, maximizingPlayer, maxDepth):
    global nextMove, transpositionTable, positionsEvaluated, startTime, endProgram

    if not depthLimited and time.time() - startTime > timePerMove:
        endProgram = True
        return 0


    if depth == 0 or gs.endGame():
        positionsEvaluated += 1
        return evaluate(gs)

    entry = transpositionTable.lookup(gs)
    if entry is not None:
        if entry['depth'] >= depth:
            if entry['flag'] == 'exact':
                return entry['eval']
            elif entry['flag'] == 'lowerbound':
                alpha = max(alpha, entry['eval'])
            elif entry['flag'] == 'upperbound':
                beta = min(beta, entry['eval'])
            if alpha >= beta:
                return entry['eval']

        for move in entry['moves']:
            moveToMove = validMoves.pop(validMoves.index(move))
            validMoves.insert(0, moveToMove)

    bestMovesHere = []
    if maximizingPlayer:
        maxValue = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            value = alphaBeta(alpha, beta, gs.getValidMoves(), gs, depth-1, False, maxDepth)
            gs.undoMove()
            if value > maxValue:
                maxValue = value
                bestMovesHere.append(move)
                if depth == maxDepth:
                    nextMove = move
            if maxValue >= beta:
                break
            alpha = max(alpha, maxValue)
        if maxValue == CHECKMATE: #Found forced mate
            maxValue = maxValue - (maxDepth - depth)

        if maxValue >= beta:
            flag = 'lowerbound'
        else:
            flag = 'exact'
        if bestMovesHere == []:
            bestMovesHere = [validMoves[0]]
        transpositionTable.store(gs=gs, moves=bestMovesHere, depth=depth, flag=flag, eval=maxValue)

        return maxValue
    else:
        minValue = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            value = alphaBeta(alpha, beta, gs.getValidMoves(), gs, depth-1, True, maxDepth)
            gs.undoMove()
            if value < minValue:
                minValue = value
                bestMovesHere.append(move)
                if depth == maxDepth:
                    nextMove = move
            if minValue <= alpha:
                break
            beta = min(beta, minValue)
        if minValue == -CHECKMATE:
            minValue = minValue + (maxDepth - depth)

        if minValue <= alpha:
            flag = 'upperbound'
        else:
            flag = 'exact'
        if bestMovesHere == []:
            bestMovesHere = [validMoves[0]]
        transpositionTable.store(gs=gs, moves=bestMovesHere, depth=depth, flag=flag, eval=minValue)

        return minValue


def findBestMove(gs, validMoves):
    global nextMove, transpositionTable, positionsEvaluated, startTime, endProgram

    if len(validMoves) == 1:
        return validMoves[0]

    nextMove = validMoves[0]
    transpositionTable = TranspositionTable()
    positionsEvaluated = 0
    startTime = time.time()

    if depthLimited:
        for d in range(1, DEPTH+1):
            ev = alphaBeta(-CHECKMATE, CHECKMATE, validMoves, gs, d, gs.whiteToMove, d)
            print(f"Best move on depth {d} for {'white' if gs.whiteToMove else 'black'}: {nextMove}, eval: {ev:.2f}, time used: {time.time() - startTime:.2f}s, positions evaluated: {positionsEvaluated}")
            if abs(ev) >= 0.9*CHECKMATE:
                break
        print(f"{25*'#'} Move chosen: {nextMove} {25*'#'}")
        return nextMove
    else:
        endProgram = False
        d = 1
        while not endProgram:
            ev = alphaBeta(-CHECKMATE, CHECKMATE, validMoves, gs, d, gs.whiteToMove, d)
            if not endProgram:
                moveToPlay = nextMove
                evaluation = ev
                print(f"Best move on depth {d} for {'white' if gs.whiteToMove else 'black'}: {nextMove}, eval: {ev:.2f}, time used: {time.time() - startTime:.2f}s, positions evaluated: {positionsEvaluated}")
            else: #Search was interrupted, discard nextMove found
                print(f"Time limit reached on depth {d}.")
            if abs(evaluation) >= 0.9*CHECKMATE or d == 12: #Found forced mate or reached sufficient depth
                break
            d += 1
        print(f"{25*'#'} Move chosen: {moveToPlay} {25*'#'}")
        return moveToPlay