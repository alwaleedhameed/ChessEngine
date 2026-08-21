import random

pieceScore = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1}
CHECKMATE = 1000
STALEMATE = 0

def getRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]

def getGreedyMove(gs, validMoves): 
    turnPrefix = 1 if gs.whiteToMove else -1
    maxScore = -CHECKMATE
    bestMove = None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        gs.getValidMoves()
        if gs.checkmate:
            score = CHECKMATE
        elif gs.stalemate:
            score = STALEMATE
        else:
            score = scoreMaterial(gs.board) * turnPrefix
        if score > maxScore: 
            maxScore = score
            bestMove = playerMove
        gs.undoMove()
    return bestMove

def getMinMaxMove(gs, validMoves):
    turnPrefix = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = -CHECKMATE
    bestMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if len(opponentsMoves) == 0:
            if gs.checkmate:
                gs.undoMove()
                return playerMove
            else:
                gs.undoMove(  )
                continue
        moveMinMax = CHECKMATE
        for opponentMove in opponentsMoves:
            gs.makeMove(opponentMove)
            gs.getValidMoves()
            if gs.checkmate:
                score = CHECKMATE
            elif gs.stalemate: 
                score = STALEMATE
            else:
                score = scoreMaterial(gs.board) * -turnPrefix
            if score < moveMinMax:
                moveMinMax = score
            gs.undoMove()
        if moveMinMax > opponentMinMaxScore:
            opponentMinMaxScore = moveMinMax
            bestMove = playerMove
        gs.undoMove()
    return bestMove

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score
