# Main File: Responsible for storing user input and representing game state.

import pygame as pg
import chessEnginePro
import chessMoveFinder

##################################################################################
# Initialize a global dictionary of images to be called once in main.

def loadImages():
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

##################################################################################
# Responsible for the graphics within a current game state

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    global colors
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

def highlightSquares(screen, gs, validMoves, sqSelected): 
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): 
            s = pg.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(pg.Color('yellow'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(pg.Color('green'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))

def animateMove(move, screen, board, clock):
    global colors
    rowDist = move.endRow - move.startRow
    colDist = move.endCol - move.startCol
    ''' Speed-fixed animation
    fpsquare = 10
    frameCount = (abs(rowDist) + abs(colDist)) * fpsquare
    for frame in range(frameCount + 1):
        r, c =(move.startRow + rowDist*frame/frameCount, move.startCol + colDist*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pg.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pg.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pg.display.flip()
        clock.tick(60) 
'''
    # Time-fixed animation
    moveDuration = .3
    moveFrames = int(60 * moveDuration)
    for frame in range(moveFrames+1):
        r, c = (move.startRow + rowDist*frame/moveFrames, move.startCol + colDist * frame/moveFrames)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pg.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pg.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--' and not move.isEnPassant: # En Passant weird capture fix
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        elif move.isEnPassant: 
            enSquare = pg.Rect(move.endCol*SQ_SIZE, move.startRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], enSquare)
        screen.blit(IMAGES[move.pieceMoved], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pg.display.flip()
        clock.tick(60) 

def drawText(screen, text):
    font = pg.font.SysFont("liberationsans", 48, True, True)
    textObject = font.render(text, 0, pg.Color('Gray'))
    textLocation = pg.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pg.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))


##################################################################################
# Main code driver; responsible for handling user input and updating graphics
WIDTH = HEIGHT = 713
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
    loadImages()
    running = True
    sqSelected = ()
    playerClicks =[]
    moveMade = False
    animate = False
    gameOver = False
    player1 = False # True if human, false if AI
    player2 = True

    while running:
        humanTurn = (gs.whiteToMove and player1) or (not gs.whiteToMove and player2)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            # Mouse handlers
            elif event.type == pg.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
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
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                                break
                        if not moveMade: # For choosing another piece with one click rather than having to waste click
                            playerClicks = [sqSelected]
            #  key handlers
            elif event.type == pg.KEYDOWN: 
                if event.key == pg.K_z: # undo
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if event.key == pg.K_r:
                    gs = chessEnginePro.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        # AI move finder logic
        if not gameOver and not humanTurn:
            # randAI = chessMoveFinder.getRandomMove(validMoves)
            # greedyAI = chessMoveFinder.getGreedyMove(gs, validMoves)
            # hardcodedMinMaxAI = chessMoveFinder.getManualMinMaxMove(gs, validMoves)
            recMinMaxAI = chessMoveFinder.getNegaMaxMoveABPRUNING(gs, validMoves, 3)
            gs.makeMove(recMinMaxAI)
            moveMade = True
            animate = True

        if moveMade: 
            validMoves = gs.getValidMoves()
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            moveMade = False
            animate = False
                    

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, "White wins by checkmate")
        elif gs.stalemate:
            gameOver = True
            drawText(screen, "Stalemate!!")            

        clock.tick(MAX_FPS)
        pg.display.flip()


if __name__ == "__main__":
    main() 