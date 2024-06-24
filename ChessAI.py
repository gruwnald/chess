import time
from ChessParams import *
from TranspositionTable import *
from PositionScores import *

CHECKMATE = 1_000_000
STALEMATE = 0

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
    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece != "--":
                if piece[0] == 'w':
                    evaluationEarly += pieceValuesEarly[piece[1]] + positionScoresEarly[piece][r][c]
                    evaluationLate += pieceValuesLate[piece[1]] + positionScoresLate[piece][r][c]
                else:
                    evaluationEarly -= pieceValuesEarly[piece[1]] + positionScoresEarly[piece][r][c]
                    evaluationLate -= pieceValuesLate[piece[1]] + positionScoresLate[piece][r][c]

    piecesLeft = min(gs.piecesLeft, 14) #in case of early promotion
    evaluation = (piecesLeft * evaluationEarly + (14 - piecesLeft) * evaluationLate)/14

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

    global evalTime
    evalTime = 0

    turnMultiplier = 1 if gs.whiteToMove else -1

    moveToPlay = None
    d = 1
    while not endProgram:
        ev = findMoveAlphaBeta(-CHECKMATE, CHECKMATE,
                               gs, validMoves, d, turnMultiplier, maxDepth=d)
        if ev == CHECKMATE-d: #Found forced mate
            break
        if depthLimited:
            endProgram = (d == DEPTH)
            moveToPlay = nextMove
            print(f"Best move on depth {d}: {moveToPlay}, time used: {time.time() - startTime:.1f}s, positions evaluated: {counter}, eval: {ev * turnMultiplier:.1f}")

        else:
            if time.time() - startTime > timePerMove: #Search was interrupted, discard nextMove found
                endProgram = True
                print(f"Time limit reached on depth {d}.")
            else:
                moveToPlay = nextMove
                print(f"Best move on depth {d}: {moveToPlay}, time used: {time.time() - startTime:.1f}s, positions evaluated: {counter}, eval: {ev * turnMultiplier:.1f}")
        d += 1
    if moveToPlay is None:
        moveToPlay = validMoves[0] #No good move was found, position is lost, can play anything
    return moveToPlay


def findMoveAlphaBeta(alpha, beta, gs, validMoves, depth, turnMultiplier, maxDepth):
    global nextMove, counter, transpositionTable, startTime, endProgram

    if depth == 0 or gs.endGame():
        counter += 1
        return turnMultiplier * evaluate(gs)

    alphaOrig = alpha
    entry = transpositionTable.lookup(gs)
    if entry is not None: #This position has been visited before
        if entry['depth'] >= depth:
            if entry['flag'] == "EXACT":
                return entry['value']
            elif entry['flag'] == "LOWERBOUND":
                alpha = max(alpha, entry['value'])
            elif entry['flag'] == "UPPERBOUND":
                beta = min(beta, entry['value'])
            if alpha >= beta:
                return entry['value']

        validMoves.insert(0, validMoves.pop(validMoves.index(entry['move']))) #Order moves by transposition table

    maxEval = -CHECKMATE
    bestMove = validMoves[0] #best move found so far
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
    if (entry is None) or (entry['depth'] < depth):
        if maxEval <= alphaOrig:
            flag = "UPPERBOUND"
        elif maxEval >= beta:
            flag = "LOWERBOUND"
        else:
            flag = "EXACT"
        transpositionTable.store(
            gs=gs,
            depth=depth,
            move=bestMove,
            value=maxEval,
            flag=flag
        )
    return maxEval