# Main File: Responsible for storing user input and representing game state.

import pygame as pg
import chessEnginePro

##################################################################################
# Initialize a global dictionary of images to be called once in main.

def loadImages():
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

##################################################################################
# Responsible for the graphics within a current game state

def drawGameState(screen, board):
    drawBoard(screen)
    drawPieces(screen, board)

def drawBoard(screen):
    colors = [pg.Color("white"), pg.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            pg.draw.rect(screen, color, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

##################################################################################
# Main code driver; responsible for handling user input and updating graphics
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # For animations later on
IMAGES = {}

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = chessEnginePro.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages()
    running = True
    sqSelected = ()
    playerClicks =[]

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            # Mouse handlers
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos() 
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = chessEnginePro.Move(playerClicks[0], playerClicks[1], gs.board)

                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            print(move.getChessNotation())
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                            break
                    if not moveMade: # For choosing another piece with one click rather than having to waste click
                        playerClicks = [sqSelected]
            #  key handlers
            elif e.type == pg.KEYDOWN: 
                if e.key == pg.K_z:
                    gs.undoMove()
                    moveMade = True


        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
                    

        drawGameState(screen, gs.board)
        clock.tick(MAX_FPS)
        pg.display.flip()


if __name__ == "__main__":
    main() 