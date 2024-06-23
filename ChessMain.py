import pygame as p
from ChessEngine import *
from ChessAI import *
from ChessParams import *

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK",
              "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))
    

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #Only generate new valid moves after move is made

    loadImages()
    running = True
    sqSelected = () #Last clicked square, initially none
    playerClicks = [] #Keep track of player clicks, ex. [(6, 4), (4, 4)] = e2 -> e4
    gameOver = False

    drawGameState(screen, gs, validMoves, sqSelected)
    clock.tick(MAX_FPS)
    p.display.flip()

    while running:
        humanTurn = (gs.whiteToMove and isWhiteHuman) or (not gs.whiteToMove and isBlackHuman)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() #(x, y)
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE

                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []

                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                    if len(playerClicks) == 2: #That was 2nd click
                        move = Move(playerClicks[0], playerClicks[1], gs.board)
                        for validMove in validMoves:
                            if move == validMove:
                                gs.makeMove(validMove)
                                moveMade = True
                                sqSelected = () #reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    if not((gs.whiteToMove and isWhiteHuman) or (not gs.whiteToMove and isBlackHuman)):
                        gs.undoMove()
                    moveMade = True
                    gameOver = False

                if e.key == p.K_r:
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False

        #AI move finder logic
        if not gameOver and not humanTurn:
            AIMove = findBestMove(gs, validMoves)
            gs.makeMove(AIMove)
            moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False


        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.endGame():
            if gs.checkmate():
                if gs.whiteToMove:
                    drawEndGameText(screen, "Black wins by checkmate")
                else:
                    drawEndGameText(screen, "White wins by checkmate")
            elif gs.stalemate():
                drawEndGameText(screen, "Stalemate")
            else:
                drawEndGameText(screen, "Draw")
            gameOver = True

        clock.tick(MAX_FPS)
        p.display.flip()


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("sienna4")] #best sienna4
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row+col)%2]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"): #sqSelected is a piece that can be moved
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #Transparency value
            s.fill(p.Color("yellow"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    if gs.board[move.endRow][move.endCol] != "--":
                        p.draw.circle(screen, p.Color("gray50"),
                                      (move.endCol*SQ_SIZE + SQ_SIZE//2,
                                       move.endRow*SQ_SIZE + SQ_SIZE//2),
                                      radius=SQ_SIZE//2, width=SQ_SIZE//16)
                    else:
                        p.draw.circle(screen, p.Color(150, 150, 150, a=50),
                                      (move.endCol*SQ_SIZE + SQ_SIZE//2,
                                       move.endRow*SQ_SIZE + SQ_SIZE//2),
                                      radius=SQ_SIZE//5, width=0)

def highlightLastMove(screen, gs):
    if len(gs.moveLog) > 0:
        move = gs.moveLog[-1]
        startRow, startCol = move.startRow, move.startCol
        endRow, endCol = move.endRow, move.endCol
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color("yellow"))
        screen.blit(s, (startCol*SQ_SIZE, startRow*SQ_SIZE))
        screen.blit(s, (endCol*SQ_SIZE, endRow*SQ_SIZE))


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH//2 - textObject.get_width()//2, HEIGHT//2 - textObject.get_height()//2)
    screen.blit(textObject, textLocation)


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    highlightLastMove(screen, gs)
    drawPieces(screen, gs.board)


if __name__ == "__main__":
    main()